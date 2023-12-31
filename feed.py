import sys

from tabulate import tabulate

import utils
from CacheThread import CacheThread
from colorize_output import Colorize
from web_interface_single.HomeFeed import HomeFeed
from web_interface_single.TechArea import TechArea


# 输出颜色
colorizer = Colorize()

class Feed:
    def __init__(self):
        self.bilibili_feed_map = utils.read_config('config.ini')['bilibili-feed']

        self._init_service()
        # 缓存
        self.cache = {}

    def _init_service(self):
        serv_map = {}
        for name in self.bilibili_feed_map.keys():
            serv = self._serv_builder(name)
            if serv == None:
                continue
            serv.set_url(self.bilibili_feed_map.get(name))
            serv_map[name] = serv
        self.serv_map = serv_map

    def _serv_builder(self, name):
        if name == '首页':
            return HomeFeed()
        if name == '数码区' or name == '软件应用' or name == '计算机技术' or name == '科工机械' or name == '极客DIY':
            return TechArea()
        return None

    def get_data_by_type(self, type, page_num):
        if type in self.serv_map.keys():
            serv = self.serv_map[type]
            if serv == None:
                return ''
            if type == '':
                print('')
            return serv.make_request(serv.page_param(type=type, page_num=page_num))
        return ''

    def get_serv_by_type(self, type):
        return self.serv_map[type]

    def parse_data_by_type(self, type, html_data):
        return self.serv_map[type].parse(html_data)

    def print_types(self):
        i = 1
        for type in self.serv_map.keys():
            print('{}.{}'.format(i, type))
            i += 1

    def do_pre_cache(self, type, url_page_num):
        cache_thead = CacheThread(self, type, url_page_num)
        cache_thead.start()

def processor(feed, type, url_page_num):

    # 直接读取缓存
    if type not in feed.cache.keys() or feed.cache[type] == None:
        html_data = feed.get_data_by_type(type, url_page_num)
        data = feed.parse_data_by_type(type, html_data)
    else:
        data = feed.cache[type]
    # 缓存预读 异步读取数据，缓存入 feed.cache 中
    feed.do_pre_cache(type=type, url_page_num=url_page_num+1)

    for i in range(len(data['list'])):
        title = data['list'][i]['title']
        title = title[:30] if len(title) > 30 else title
        data['list'][i]['title'] = title

    # # 输出颜色
    # colorizer.colorize_list(data['list'])
    #
    # # 格式化输出
    # print(tabulate(data['list'], tablefmt="plain"))
    # print('['+ str(data['num'])+'/'+str(data['total_page']) +']')
    # print()

    # 颜色输出
    colorizer.colorize_list(data['list'])
    # 格式化输出
    headers = {
        'name': 'name',
        'view': '播放量',
        'title': 'title',
        'url': 'url',
    }
    print(tabulate(data['list'], headers=headers, tablefmt="plaint"))
    print('[' + str(data['num']) + '/' + str(data['total_page']) + ']')
    print()

def chose_mode():
    feed = Feed()

    while True:
        params = cmd_lv1()

        if params[0] == '-q':
            print('bye bye')
            return
        elif params[0] == '-l':
            feed.print_types()
        elif params[0] == '-name' and params[1] != '':
            type = params[1]
            url_page_num = 1
            while True:
                processor(feed, type, url_page_num)
                url_page_num += 1

                params = cmd_lv2()
                if params[0] == '-n':
                    continue
                if params[0] == '-q':
                    print('bye bye')
                    return
                if params[0] == '-r':
                    break


def cmd_lv1():
    while True:
        print()
        print('press -l 查看各视频区name')
        print('press -name 选择视频区')
        print('press -q 退出')
        print('(press 其他字符则忽略)')

        params = sys.stdin.readline().split()

        if params[0] == '-l' or params[0] == '-name' or params[0] == '-q':
            return params

def cmd_lv2():
    while True:
        print()
        print('press -l 查看各视频区name')
        print('press -r 回到上一级')
        print('press -n 下一页')
        print('press -q 退出')
        print('(press 其他字符则忽略)')

        params = sys.stdin.readline().split()

        if len(params) == 0:
            continue
        if params[0] == '-l' or params[0] == '-q' or params[0] == '-r' or params[0] == '-n':
            return params



if __name__ == '__main__':
    chose_mode()