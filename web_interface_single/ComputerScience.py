import json

import requests


class ComputerScience:

    def set_url(self, url):
        self.url = url

    def page_param(self, page_num):
        return {
            "num": page_num
        }

    def make_request(self, *param):
        url = self.url.replace("%page", str(param[0]['num']))
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

            res_list.append(owner + ' ' + str(view) + ' ' + title + ' ' + uri)

        return res_list