#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/5/3 上午11:10
# @Author  : 武明辉
# @File    : testSpider.py
import json

import scrapy


class WeixinTestSpider(scrapy.Spider):
    name = 'test'

    start_urls = ['http://www.newrank.cn/public/info/list.html?period=month&type=data', ]
    post_url = 'http://www.newrank.cn/xdnphb/list/month/rank'

    def start_requests(self):
        url = 'http://www.newrank.cn/xdnphb/list/month/rank'
        formdata = {'end': '2017-03-31', 'rank_name': '时事', 'rank_name_group': '资讯', 'start': '2017-03-01'}
        headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Host': 'www.newrank.cn',
                   'Referer': 'http://www.newrank.cn/public/info/list.html?period=month&type=data',
                   'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                   'X-Requested-With': 'XMLHttpRequest'}
        return [scrapy.FormRequest(url=url, formdata=formdata, callback=self.after_post,
                                   headers=headers)]

    def after_post(self, response):
        # 得到json数据
        print '****************', response.body
        # resutl_json = json.loads(response.body)['value']
        # return None
