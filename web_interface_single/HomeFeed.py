import json

import requests

import utils
from web_interface_single.Wbi import generate_url


class HomeFeed:
    def __init__(self):
        config = utils.read_config('config.ini')
        self.feed_page_size = int(config['cfg']['feed_page_size'])

    def set_url(self, url):
        self.url = url

    def page_param(self, type, page_num):
        self.page_num = page_num
        return {
            'web_location':1430650,
            'fresh_idx':page_num,
            'brush':page_num,
            'ps':self.feed_page_size,
            'uniq_id':1171486254368,
        }

    def make_request(self, *param):
        query = generate_url(param[0])
        url = self.url+'?'+query
        print(url)
        response = requests.get(url)
        return response.text

    def parse(self, html_data):
        # print(html_data)
        html_json = json.loads(html_data)
        item_list = html_json['data']['item']
        res_list = []

        for item in item_list:
            uri = item['uri']
            title = item['title']
            owner = item['owner']['name']
            view = item['stat']['view']

            res_list.append({
                'owner': owner,
                'view': utils.num_shorten(view),
                'title': title,
                'uri': uri,
            })

        data = {
            'list': res_list,
            'num': self.page_num,
            'total_page': -1,
        }

        return data