import argparse
import json

import requests
from tabulate import tabulate

import utils
from search_uid import get_uid
from web_interface_single import Wbi


def search_req(mid, keyword):

    params = {
        'keyword': keyword,
        'pn': 1,
        'ps': 30,
        'mid': mid,
        'order': 'pubdate',
    }

    header = {
        'Cookie': utils.read_env('cookie'),
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
        c = {
            'author': v['author'],
            'title': v['title'],
            'play': utils.num_shorten(v['play']),
            'url': 'https://www.bilibili.com/video/'+v['bvid'],
        }
        res_list.append(c)
    return res_list

def work(args):
    uname = args.u
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
    print(tabulate(res_list, tablefmt="plain"))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', type=str, default='', help='up主名字')
    parser.add_argument('-k', type=str, default='', help='搜索关键词')
    parser.add_argument('-id', type=str, default='', help='指定up主mid')

    args = parser.parse_args()

    work(args)
