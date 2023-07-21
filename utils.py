import configparser
from datetime import datetime, timedelta
import os


def read_config(name):
    # 创建 ConfigParser 对象
    config = configparser.RawConfigParser()
    # 读取配置文件
    config.read(file_path(name))
    return config

# 读取系统环境变量
def read_env(keyname):
    if keyname in os.environ:
        value = os.environ[keyname]
        return value

def file_path(name):
    # 获取当前文件所在的根路径
    root_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(root_dir, name)
    return file_path

def timestamp_2_date(timestamp):
    date = datetime.fromtimestamp(timestamp)
    formatted_date = date.strftime("%Y-%m-%d")
    return formatted_date

def before_date_from_now(delta=10):
    date = datetime.now()
    d = timedelta(delta)
    r = date - d
    return r.date()

def num_shorten(num):
    if num < 10000:
        return str(num)
    if num < 1e8:
        return str(int(num / 10000)) + '万'
    e = int(num / 1e8)
    w = int((num - e * 1e8)/10000)
    return str(e)+'亿'+str(w)+'万'

def total_page(count, page_size):
    if count % page_size != 0:
        total_page = int(count / page_size) + 1
    else:
        total_page = int(count / page_size)
    return total_page

def remove_highlight_html(text):
    pattern = '<em class=\"keyword\">'
    while True:
        pos = text.find(pattern)
        if pos == -1:
            break
        text = text[:pos]+text[pos+len(pattern):]

    pattern = '</em>'
    while True:
        pos = text.find(pattern)
        if pos == -1:
            break
        text = text[:pos] + text[pos + len(pattern):]
    return text
