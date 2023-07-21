import argparse
import json
import threading

import requests
from tabulate import tabulate

import utils
from colorize_output import Colorize
from web_interface_single import Wbi

# read config
config = utils.read_config('config.ini')
follow = config['bilibili-follow']
follow_map = dict(follow.items())
DEFAULT_TITLE_LEN = int(config['cfg']['default_title_len'])
DEFAULT_D = int(config['cfg']['default_d'])
DEFAULT_N = int(config['cfg']['default_n'])

colorizer = Colorize()

class HttpThread(threading.Thread):
    def __init__(self, name, args):
        threading.Thread.__init__(self)
        self.name = name
        self.args = args

    def run(self):
        res = get_data(follow_map.get(self.name))
        self.args.name = self.name
        bilibili_json_process(res, self.args)

def get_data(mid):
    query = Wbi.generate_url({
        'mid':mid,
        'ps':30,
        'tid':0,
    })

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45",
    }
    response = requests.get('https://api.bilibili.com/x/space/wbi/arc/search?'+query, headers=header)
    return response.text

def bilibili_json_process(str_data, args):
    nickname = args.name
    num = args.n
    before_day_delta = args.d
    title_show_all_flag = args.a

    html_json = json.loads(str_data)
    vlist = html_json['data']['list']['vlist']

    # 参数处理
    size = len(vlist)
    if num != -1:
        size = num if len(vlist) > num else len(vlist)

    before_day_switch = False if before_day_delta == -1 else True

    res = []
    before_date = utils.before_date_from_now(delta=before_day_delta).strftime("%Y-%m-%d")
    for idx in range(size):
        v = vlist[idx]
        author = v['author']
        create_date = utils.timestamp_2_date(v['created'])

        if not before_day_switch or before_date < create_date:
            url = 'https://www.bilibili.com/video/' + v['bvid']
            play = v['play']
            title = v['title']
            title = title.replace(" ", "")
            if not title_show_all_flag:
                max_title_len = len(title) if len(title) < DEFAULT_TITLE_LEN else DEFAULT_TITLE_LEN
                title = title[:max_title_len]
            r = {
                'create_date': create_date,
                'play': utils.num_shorten(play),
                'title': title,
                'url': url,
            }
            res.append(r)
        else:
            break
    if len(res):
        print(colorizer.colorize_text(author, 'author') + '(' + colorizer.colorize_text(nickname, 'nickname') + ')')
        colorizer.colorize_list(res)
        print(tabulate(res, tablefmt="plain"))
        print('')

def print_all_nickname():
    name_list = follow_map.keys()
    i = 1
    for name in name_list:
        print('{}.{}'.format(i, colorizer.colorize_text(name, 'name')))
        i += 1

def work(args):

    if args.l:
        print_all_nickname()
        return

    if args.name != '':
        mid = follow_map.get(args.name)
        if mid == None:
            print('参数错误 and 未找到数据')
            return
        res = get_data(mid)
        if args.n == DEFAULT_N:
            args.n = -1
        if args.d == DEFAULT_D:
            args.d = -1
        bilibili_json_process(res, args)

    else:
        for name in follow_map.keys():
            thread = HttpThread(name, args)
            thread.start()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', type=int, default=DEFAULT_D, help='忽略n天以前的内容，默认'+str(DEFAULT_D)+'天; -1 关闭此功能')
    parser.add_argument('-n', type=int, default=DEFAULT_N, help='打印最近的n条数据，默认'+str(DEFAULT_N)+'条; -1 关闭此功能')
    parser.add_argument('-name', type=str, default='', help='获得特定nickname用户的视频列表')

    parser.add_argument('-a', action='store_true', help='标题缩略,长度默认'+str(DEFAULT_TITLE_LEN))
    parser.add_argument('-l', action='store_true', help='查看所有的 nickname')
    args = parser.parse_args()

    work(args)
