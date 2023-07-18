import json
import urllib

import requests

import utils


class TechArea:
    def __init__(self):
        config = utils.read_config('config.ini')
        self.feed_page_size = int(config['cfg']['feed_page_size'])

    def set_url(self, url):
        self.url = url
        self.total_page = -1

    def page_param(self, type, page_num):
        # 边界限制
        if self.total_page != -1 and page_num > self.total_page:
            page_num = self.total_page
        return {
            "pn": page_num,
            "ps": self.feed_page_size,
            "rid": self._get_rid_by_type(type),
        }

    def _get_rid_by_type(self, type):
        if type =='数码区':
            return 95
        if type == '软件应用':
            return 230
        if type == '计算机技术':
            return 231
        if type == '科工机械':
            return 232
        if type == '极客DIY':
            return 233
        return 0

    def make_request(self, *param):
        url = self.url+'?'+urllib.parse.urlencode(param[0])
        print(url)
        response = requests.get(url)
        return response.text

    def parse(self, html_data):
        # print(html_data)
        html_json = json.loads(html_data)
        archives = html_json['data']['archives']
        res_list = []

        for item in archives:
            uri = item['short_link_v2']
            title = item['title']
            owner = item['owner']['name']
            view = item['stat']['view']

            res_list.append({
                'owner': owner,
                'view': utils.num_shorten(view),
                'title': title,
                'uri': uri,
            })

        page = html_json['data']['page']
        self.total_page = utils.total_page(page['count'], page['size'])

        data = {
            'list': res_list,
            'num': page['num'],
            'total_page': self.total_page,
        }

        return data
