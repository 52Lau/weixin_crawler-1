from scrapy import signals
from scrapy.http import Response
from crawler_assist.tidy_req_data import TidyReqData
from crawler_assist.decode_response import DecodeArticle
from copy import copy
from tools.utils import str_to_dict
import time


class CrawlArticleMiddleware():
    counter = 0
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        current_req_data = self.req_data_list[self.counter%self.wx_num]
        req_data = TidyReqData.req_to_dict(current_req_data['content']['req_data'])
        url = request._get_url()
        raw_url = copy(url)
        if "https" in raw_url:
            raw_url = raw_url.replace("https","http")
        request.set_ext_data({"raw_url":raw_url})
        if "https" not in url:
            url = url.replace("http","https")
        request._set_url(url)
        request.set_method(req_data['method'])
        if "Cookie" in req_data['headers']:
            req_data['headers'].pop("Cookie")
        request.set_headers(req_data['headers'])
        self.counter += 1
        return None

    def process_response(self, request, response, spider):
        r_body = response.body_as_unicode()
        if "访问过于频繁，请用微信扫描二维码进行访问" in r_body:
            print("IP被限制 一天之内无法通过局域网查看请更换IP")
            spider.crawler.engine.close_spider(spider, 'IP被限制 一天之内无法通过局域网查看请更换IP')
        article_data = DecodeArticle.decode_content(r_body)
        response.set_ext_data({"article_data":article_data,
                               "nickname":spider.current_nickname,
                               "raw_url":request.get_ext_data["raw_url"]})
        return response

    def spider_opened(self, spider):
        self.wx_num,self.req_data_dict,self.req_data_list = TidyReqData.get_gzh_req_data()
        if self.wx_num == 0:
            self.wx_num = 1


class ArticleReadDataMiddleware():
    counter = 0
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # 循环选择下一个参数作为请求参数
        current_req_data = self.req_data_list[self.counter%self.wx_num]

        request_data = self.prepare_req_data(current_req_data, request, 'getappmsgext')
        from crawler_assist.request_reading_data import RequestReadingData
        rrd = RequestReadingData(request_data['url_str'],request_data['header_dict'],request_data['body_dict'])
        read_data = rrd.act()
        res = Response(request_data['url_str'])
        res.set_ext_data({'read_data':read_data})
        download_delay = spider.settings.attributes.get('DOWNLOAD_DELAY').value
        self.counter += 1
        # 保证每个微信等待三秒之后再发起请求
        while (time.time()-self.pre_crawl_time) < download_delay-0.01:
            time.sleep(0.05)
        self.pre_crawl_time = time.time()
        return res

    def process_response(self, request, response, spider):
        read_data = response.get_ext_data['read_data']
        response.set_ext_data({"read_data":read_data,
                               "nickname":spider.current_nickname,
                               "content_url":request.meta["content_url"]})
        return response

    def spider_opened(self, spider):
        self.wx_num,self.req_data_dict,self.req_data_list = TidyReqData.get_gzh_req_data()
        if self.wx_num == 0:
            self.wx_num = 1
        self.pre_crawl_time = time.time()


    def prepare_req_data(self, current_req_data, request, _type):
        """
        :param current_req_data: 本轮请求需要使用的请求参数
        :param request: Request对象
        :return: 准备爬取阅读数据的请求参数
        """
        request_data = {}

        if _type in ['getappmsgext','appmsg_comment']:
            req_data = TidyReqData.req_to_dict(current_req_data[_type]['req_data'])
        else:
            return request_data

        #根据原始文章的url构建body参数
        content_url = request._get_url()
        content_url_param_dict = str_to_dict(content_url.split('?')[-1],'&','=')
        body_dict = copy(req_data['body_dict'])
        from tools.utils import update_dict_by_dict
        update_dict_by_dict(body_dict,content_url_param_dict,['mid','sn','idx','scene'])
        body_dict['comment_id'] = request.meta['comment_id']
        body_dict['is_need_reward'] = 1
        # 如果请求的是评论内容
        if "comment_id" in req_data['url_param_dict']:
            url_param_dict = copy(req_data['url_param_dict'])
            url_param_dict['comment_id'] = request.meta['comment_id']
            url_param_dict['idx'] = content_url_param_dict['idx']
            from tools.utils import dict_to_str
            url_param_str = dict_to_str(url_param_dict)
            request_data['url_str'] = req_data['url']+url_param_str
        # 如果请求的是阅读量
        else:
            request_data['url_str'] = req_data['url']+req_data['url_param_str']
        request_data['header_dict'] = req_data['headers']
        request_data['body_dict'] = body_dict

        return request_data
