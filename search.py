import argparse
import json

import requests
from tabulate import tabulate

import utils
from colorize_output import Colorize
from search_uid import get_uid
from web_interface_single import Wbi


# 读取配置
config = utils.read_config('config.ini')
DEFAULT_TITLE_LEN = int(config['cfg']['default_title_len'])
# 输出颜色
colorizer = Colorize()

def search_req(mid, keyword):

    params = {
        'keyword': keyword,
        'pn': 1,
        'ps': 30,
        'mid': mid,
        'order': 'pubdate',
    }

    header = {
        'Cookie': utils.read_env('BILI_COOKIE'),
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    query = Wbi.generate_url(params)
    url = 'https://api.bilibili.com/x/space/wbi/arc/search?'+query
    resp = requests.get(url, headers=header)
    return resp.text

def parse_result(html_text):
    json_data = json.loads(html_text)
    data = json_data['data']
    vlist = data['list']['vlist']

    res_list = []
    for v in vlist:

        title = v['title']
        max_title_len = len(title) if len(title) < DEFAULT_TITLE_LEN else DEFAULT_TITLE_LEN
        title = title[:max_title_len]

        c = {
            'author': v['author'],
            'title': title,
            'play': utils.num_shorten(v['play']),
            'url': 'https://www.bilibili.com/video/'+v['bvid'],
        }
        res_list.append(c)
    return res_list

def work(args):
    uname = args.name
    keyword = args.k
    mid = args.id

    if mid != '':
        mid = mid
    elif mid == '' and uname != '':
        mid = get_uid(uname)
    else:
        return
    if keyword == '':
        return

    html_text = search_req(mid, keyword)
    res_list = parse_result(html_text)

    # 颜色输出
    colorizer.colorize_list(res_list)
    # 格式化输出
    headers = {
        'author': 'author',
        'title': 'title',
        'play': '播放量',
        'url': 'url',
    }
    print(tabulate(res_list, headers=headers, tablefmt="plaint"))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-name', type=str, default='', help='up主名字')
    parser.add_argument('-k', type=str, default='', help='搜索关键词')
    parser.add_argument('-id', type=str, default='', help='指定up主mid')

    args = parser.parse_args()

    work(args)
