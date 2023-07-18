import utils
from web_interface_single.GeekDIY import GeekDIY
from web_interface_single.HomeFeed import HomeFeed
from web_interface_single.SoftApp import SoftApp
from web_interface_single.TechDigit import TechDigit
from web_interface_single.ComputerScience import ComputerScience
from web_interface_single.TechEngineer import TechEngineer


class WebInterface:
    def __init__(self):
        self.bilibili_feed_map = utils.read_config('config.ini')['bilibili-feed']

        self._init_service()

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
        if name == '数码区':
            return TechDigit()
        if name == '软件应用':
            return SoftApp()
        if name == '计算机技术':
            return ComputerScience()
        if name == '科工机械':
            return TechEngineer()
        if name == '极客DIY':
            return GeekDIY()
        return None

    def get_data_by_type(self, type, page_num):
        if type in self.serv_map.keys():
            serv = self.serv_map[type]
            if serv == None:
                return ''
            if type == '':
                print('')
            return serv.make_request(serv.page_param(page_num))
        return ''

    def get_serv_by_type(self, type):
        return self.serv_map[type]

    def parse_data_by_type(self, type, html_data):
        return self.serv_map[type].parse(html_data)

    def get_type_list(self):
        return self.serv_map.keys()

if __name__ == '__main__':
    wi = WebInterface()
    types = wi.get_type_list()
    # for type in types:
    #     html_data = wi.get_data_by_type(type, 1)
    #     res = wi.parse_data_by_type(type, html_data)
    type = '首页'
    for page in range(3):
        html_data = wi.get_data_by_type(type, page)
        res = wi.parse_data_by_type(type, html_data)
        for v in res:
            print(v)
        print()
        print('*' * 20)

