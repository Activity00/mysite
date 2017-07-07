#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/4/26 下午6:58
# @Author  : 武明辉
# @File    : test1spider.py

import scrapy
from scrapy import Selector
from scrapy.spiders import Rule


class Test1Spider(scrapy.Spider):
    name = 'test1'
    start_urls = ['http://www.baidu.com']
    # 允许爬的域名地址
    allowed_domains = ['', ]
    #  自定义设置，会覆盖掉settings的设置
    custom_settings = {'User-Agent': '...'}

    def __init__(self, start_time=None, end_time=None, *args, **kwargs):
        super(Test1Spider, self).__init__(*args, **kwargs)
        self.start_time = start_time
        self.end_time = end_time

    def parse(self, response):
        print '111马上结束'

from scrapy.linkextractor import LinkExtractor
class CrawlSpider(scrapy.CrawlSpider):
    name = 'test2'
    allow_domains = ['', ]
    start_urls = ['', ]
    rules = (
        Rule(LinkExtractor(allow='category\.php', deny=('subsection\.php'))),
        Rule(LinkExtractor(allow='item\.php'),callback='parse_item'),
    )

    def parse_item(self,response):
        self.logger.info('aaa%s',response.url)
        item = scrapy.Item()
        item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
        item['name'] = response.xpath('//td[@id="item_name"]/text()').extract()
        item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()
        return item


from scrapy.spiders import XMLFeedSpider
class MySpider(XMLFeedSpider):
    name = 'test3'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com/feed.xml']
    iterator = 'iternodes'  # This is actually unnecessary, since it's the default value
    itertag = 'item'

    def parse_node(self, response, node):
        self.logger.info('Hi, this is a <%s> node!: %s', self.itertag, ''.join(node.extract()))
        item = scrapy.Item()
        item['id'] = node.xpath('@id').extract()
        item['name'] = node.xpath('name').extract()
        item['description'] = node.xpath('description').extract()
        return item


from scrapy.spiders import CSVFeedSpider
""" 读取CSV数据 """
class MySpider(CSVFeedSpider):
    name = 'test4'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com/feed.csv']
    delimiter = ';'
    quotechar = "'"
    headers = ['id', 'name', 'description']

    def parse_row(self, response, row):
        self.logger.info('Hi, this is a row!: %r', row)
        item = scrapy.Item()
        item['id'] = row['id']
        item['name'] = row['name']
        item['description'] = row['description']
        return item

from scrapy.spiders import SitemapSpider

class MySpider(SitemapSpider):
    sitemap_urls = ['http://www.example.com/sitemap.xml']

    def parse(self, response):
        pass # ... scrape item here ...

from scrapy.spiders import SitemapSpider

class MySpider(SitemapSpider):
    sitemap_urls = ['http://www.example.com/sitemap.xml']
    sitemap_rules = [
        ('/product/', 'parse_product'),
        ('/category/', 'parse_category'),
    ]

    def parse_product(self, response):
        pass # ... scrape product ...

    def parse_category(self, response):
        pass # ... scrape category ...
from scrapy.spiders import SitemapSpider


class MySpider(SitemapSpider):
    sitemap_urls = ['http://www.example.com/robots.txt']
    sitemap_rules = [
        ('/shop/', 'parse_shop'),
    ]
    sitemap_follow = ['/sitemap_shops']

    def parse_shop(self, response):
        pass # ... scrape shop here ...

from scrapy.spiders import SitemapSpider

class MySpider(SitemapSpider):
    sitemap_urls = ['http://www.example.com/robots.txt']
    sitemap_rules = [
        ('/shop/', 'parse_shop'),
    ]
    custom_settings = {'SOME_SETTING': 'some value', }
    other_urls = ['http://www.example.com/about']

    def start_requests(self):
        requests = list(super(MySpider, self).start_requests())
        requests += [scrapy.Request(x, self.parse_other) for x in self.other_urls]
        return requests

    def parse_shop(self, response):
        pass # ... scrape shop here ...

    def parse_other(self, response):
        pass # ... scrape other here ...
