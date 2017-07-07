#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/4/26 下午6:59
# @Author  : 武明辉
# @File    : test2spider.py
import scrapy


class Test2Spider(scrapy.Spider):
    name = 'test2'
    start_urls = ['http://www.baidu.com']

    def parse(self, response):
        print '马上结束'