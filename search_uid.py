import json

import requests
from tabulate import tabulate

import utils
from web_interface_single import Wbi

def search_uid_req(uname):
    url = 'https://api.bilibili.com/x/web-interface/wbi/search/type'
    params = {
        'page': 1,
        'page_size': int(utils.read_config('config.ini')['cfg']['search_u_page_size']),
        'keyword': uname,
        'search_type': 'bili_user',
        'order': 'fans',
    }

    header = {
        'Cookie': utils.read_env('BILI_COOKIE'),
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45",
    }

    query = Wbi.generate_url(params)
    resp = requests.get(url+'?'+query, headers=header)
    return resp.text

def parse_text(html_text):
    json_data = json.loads(html_text)
    data = json_data['data']
    res = data['result'][0]

    res_list = []
    for r in data['result']:
        d = {
            'uname': r['uname'],
            'mid': r['mid'],
            'fans': utils.num_shorten(r['fans']),
        }
        res_list.append(d)

    print(tabulate(res_list, tablefmt="plain"))

    return res['mid']

def get_uid(uname):
    html_text = search_uid_req(uname)
    id = parse_text(html_text)
    return id