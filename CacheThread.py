import threading


class CacheThread(threading.Thread):
    def __init__(self, feed, type, url_page_num):
        super().__init__()
        self.feed = feed
        self.type = type
        self.url_page_num = url_page_num

    def run(self):
        html_data = self.feed.get_data_by_type(self.type, self.url_page_num)
        data = self.feed.parse_data_by_type(self.type, html_data)
        self.feed.cache = data
