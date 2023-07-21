import argparse
import json

import requests
from tabulate import tabulate

import utils
from colorize_output import Colorize
from web_interface_single import Wbi


# read config
config = utils.read_config('config.ini')
DEFAULT_TITLE_LEN = int(config['cfg']['default_title_len'])

def search_req(keyword):
    params = {
        'keyword': keyword,
        'pn': 1,
        'page_size': 42,
        '__refresh__': 'true',

        # 'order': 'pubdate',
    }

    header = {
        'Cookie': utils.read_env('BILI_COOKIE'),
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    query = Wbi.generate_url(params)
    url = 'https://api.bilibili.com/x/web-interface/wbi/search/all/v2?' + query
    resp = requests.get(url, headers=header)
    return resp.text

def parse_result(html_text):
    json_data = json.loads(html_text)
    data = json_data['data']
    result = data['result'][-1]
    result_data = result['data']

    res_list = []
    for v in result_data:
        title = utils.remove_highlight_html(v['title'])
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
    keyword = args.k
    if keyword == '':
        return

    html_text = search_req(keyword)
    res_list = parse_result(html_text)

    # 颜色输出
    colorizer = Colorize()
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
    parser.add_argument('-k', type=str, default='', help='搜索关键词')
    args = parser.parse_args()

    work(args)