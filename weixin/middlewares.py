# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
import time
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver

from weixin import settings


class WeixinSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MyCustomDownloaderMiddleware(object):

    def process_request(self, request, spider):
        pass
        #request.headers.setdefault('User-Agent', random.choice(self.agents))


class JavaScriptMiddleware(object):
    """
    webdriver PhantomsJS
    """
    def __init__(self):
        self.driver = webdriver.PhantomJS()

    def process_request(self, request, spider):
        url = request.url
        if url.startswith('https://mp.weixin.qq.com/profile') or url.startswith('http://mp.weixin.qq.com/profile'):
            self.driver.get(url)
            time.sleep(2)
            js = "var q=document.documentElement.scrollTop=100"
            self.driver.execute_script(js)  # 可执行js，模仿用户操作。此处为将页面拉至最底端。
            body = self.driver.page_source
            return HtmlResponse(url, encoding='utf-8', status=200, body=body)
            # return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
        return None


class RandomUserAgent(object):
    '''auto change user-agent'''

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        ag = random.choice(self.agents)
        print ag
        request.headers.setdefault('User-Agent', ag)
