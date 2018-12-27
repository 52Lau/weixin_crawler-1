import requests
from datetime import datetime


class RequestReadingData():
    """
    使用requests模块实现文章阅读数据的请求
    """
    def __init__(self, url_str, header_dict, body_dict, proxy=None):
        """
        :param url_str:带有参数的url 字符串格式
        :param header_dict:请求头的字典
        :param body_dict:请求体字典
        :param proxy:代理ip
        """
        self.url_str = url_str
        self.header_dict = header_dict
        self.body_dict = body_dict
        self.proxy = proxy
        self.rj = None
        self.read_data = {}

    def act_request(self):
        """
        :return:执行请求
        """
        try:
            r = requests.post(
                url     = self.url_str,
                data    = self.body_dict,
                headers = self.header_dict,
                timeout = 1,
                # proxies = self.proxy,
                verify  = False)
            self.rj = r.json()
            return r
        except Exception as e:
            print("request 请求阅读数据失败",e)

    def extract_data(self):
        """
        :return:提取数据
        """
        read_data = {}
        if "read_num" not in self.rj.get("appmsgstat"):
            print(self.rj,"请求频繁 被限制 等待5分钟")
        read_data['read_num'] = self.rj.get("appmsgstat").get("read_num")
        read_data['like_num'] = self.rj.get("appmsgstat").get("like_num")
        read_data['reward_num'] = self.rj.get("reward_total_count")
        read_data['nick_name'] = self.rj.get("nick_name")#  已登陆的微信名称
        if read_data['reward_num'] is None:
            read_data['reward_num'] = -1
        read_data['c_date'] = datetime.now()
        read_data['comment_num'] = self.rj.get("comment_count")
        if read_data['comment_num'] is None:
            read_data['comment_num'] = -1
        self.read_data = read_data

    def act(self):
        """
        :return: 调用各个子方法
        """
        self.act_request()
        self.extract_data()
        return self.read_data
