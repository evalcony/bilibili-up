import argparse
import json
import urllib

import pyparsing
import requests
from tabulate import tabulate

import utils


def favor_list_req(mid):
    params = {
        'up_mid': mid,
    }

    header = {
        'Cookie': utils.read_env('BILI_COOKIE'),
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    query = urllib.parse.urlencode(params)
    url = 'https://api.bilibili.com/x/v3/fav/folder/created/list-all?'+query
    print(url)

    resp = requests.get(url, headers=header)
    return resp.text

def parse_favor_list(html_data):
    json_data = json.loads(html_data)
    data_list = json_data['data']['list']

    res_list = []
    for v in data_list:
        c = {
            'title': v['title'],
            'id': v['id'],
            'media_count': v['media_count'],
        }
        res_list.append(c)

    print(tabulate(res_list, tablefmt="plain"))

    return res_list

def favor_req(media_id):
    params = {
        'media_id': media_id,
        'pn': 1,
        'ps': 20,
        'order': 'mtime',
    }

    header = {
        'Cookie': utils.read_env('BILI_COOKIE'),
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    query = urllib.parse.urlencode(params)

    url = 'https://api.bilibili.com/x/v3/fav/resource/list?'+query
    resp = requests.get(url, headers=header)
    return resp.text

def parse_favor(html_data):
    json_data = json.loads(html_data)
    medias_list = json_data['data']['medias']

    res_list = []
    for m in medias_list:
        c = {
            'upper-name': m['upper']['name'],
            'pubtime': utils.timestamp_2_date(m['pubtime']),
            'title': m['title'],
            'url': 'https://www.bilibili.com/video/' + m['bvid'],
        }
        res_list.append(c)

    print(tabulate(res_list, tablefmt="plain"))

    return res_list

def works(args):
    mid = utils.read_env('BILI_MID')
    if args.l:
        html_text = favor_list_req(mid)
        parse_favor_list(html_text)
    if args.f != '':
        media_id = args.f
        html_text = favor_req(media_id)
        parse_favor(html_text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', action='store_true', help='查看收藏夹列表')
    parser.add_argument('-f', type=str, default='', help='根据收藏夹id查看收藏夹')
    args = parser.parse_args()

    works(args)
