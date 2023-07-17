import configparser
from datetime import datetime, timedelta
import os


def read_config(name):
    # 创建 ConfigParser 对象
    config = configparser.RawConfigParser()
    # 读取配置文件
    config.read(file_path(name))
    return config
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