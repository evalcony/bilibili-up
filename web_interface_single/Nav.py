import json

import requests


def get_cur_token():
    img_tuple = make_request()

    token1 = _get_token(img_tuple[0])
    token2 = _get_token(img_tuple[1])

    print(token1)
    print(token2)
def make_request():
    response = requests.get('https://api.bilibili.com/x/web-interface/nav')
    html_data = response.text

    json_data = json.loads(html_data)
    wbi_img = json_data['data']['wbi_img']
    img_url = wbi_img['img_url']
    sub_url = wbi_img['sub_url']

    return (img_url, sub_url)

def _get_token(wbi_url):
    left = wbi_url.find('wbi/')
    right = wbi_url.find('.png')
    return wbi_url[left+4:right]


if __name__ == '__main__':
    get_cur_token()