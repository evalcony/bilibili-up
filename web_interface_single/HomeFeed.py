import json

import requests

from web_interface_single.Wbi import generate_url


class HomeFeed:

    def set_url(self, url):
        self.url = url

    def page_param(self, page_num):
        return {
            'web_location':1430650,
            'fresh_idx':page_num,
            'brush':1,
            'ps':20,
            'uniq_id':1171486254368,
        }

    def make_request(self, *param):
        query = generate_url(param[0])
        response = requests.get(self.url+'?'+query)
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

            res_list.append(owner + ' ' + str(view) + ' ' + title + ' ' + uri)

        return res_list