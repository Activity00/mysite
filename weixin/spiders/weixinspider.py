#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/4/24 下午5:55
# @Author  : 武明辉
# @File    : weixinspider.py
import json

import scrapy
import time

from weixin.items import XinbangItem


class WeixinSpider(scrapy.Spider):
    name = 'weixin_xb'
    start_urls = ['http://www.newrank.cn/public/info/list.html?period=month&type=data', ]
    post_url = 'http://www.newrank.cn/xdnphb/list/month/rank'
    tags1 = ['时事', '民生', '财富', '科技', '创业', '汽车', '楼市', '职场', '教育', '学术', '政务', '企业']
    tags2 = ['文化', '百科', '健康', '时尚', '美食', '乐活', '旅行', '幽默', '情感', '体娱', '美体', '文摘']

    def __init__(self, start_time=None, end_time=None, *args, **kwargs):
        # 初始化参数
        super(WeixinSpider, self).__init__(*args, **kwargs)
        if self.__is_valid_datestr(start_time):
            self.start_time = start_time
        else:
            self.logger.info('开始时间使用默认时间2017-03-01')
            self.start_time = '2017-03-01'
        if self.__is_valid_datestr(end_time):
            self.end_time = end_time
        else:
            self.logger.info('结束日期使用默认时间2017-03-31')
            self.end_time = '2017-03-31'

    def parse(self, response):
        """ 根据标签 """
        headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Host': 'www.newrank.cn', 'Referer':'http://www.newrank.cn/public/info/list.html?period=month&type=data',
                   'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                   'X-Requested-With': 'XMLHttpRequest'}

        for tag1 in WeixinSpider.tags1:
            formdata = {'end': self.end_time, 'rank_name': tag1, 'rank_name_group': '资讯', 'start': self.start_time}
            meta = {'tag': tag1}
            print formdata
            yield scrapy.FormRequest(url=WeixinSpider.post_url, formdata=formdata, callback=self.after_post, meta=meta,headers=headers)
        for tag2 in WeixinSpider.tags2:
            meta = {'tag': tag2}
            formdata = {'end': self.end_time, 'rank_name': tag2, 'rank_name_group': '生活', 'start': self.start_time}
            print formdata
            yield scrapy.FormRequest(url=WeixinSpider.post_url, formdata=formdata, callback=self.after_post, meta=meta, headers=headers)

    def after_post(self, response):
        # 得到json数据
        print response
        print response.body,'aaaaaaaaaaaaaaaaa'
        resutl_json = json.loads(response.body)['value']
        xbitem = XinbangItem()

        for item in resutl_json:
            xbitem['account'] = item['account']
            xbitem['name'] = item['name']

            xbitem['xbzs'] = item['log1p_mark']
            xbitem['rank'] = item['a']
            xbitem['pub_b'] = item['b']
            xbitem['pub_c'] = item['c']
            xbitem['totalread'] = item['d']
            xbitem['toptl'] = item['h']
            xbitem['avg'] = item['f']
            xbitem['max'] = item['i']
            xbitem['favtotal'] = item['g']
            xbitem['tag'] = response.meta['tag']

            yield xbitem

    def __is_valid_datestr(self, str):
        """ 日期校验"""
        try:
            time.strptime(str, '%Y-%m-%d')
            return True
        except Exception:
            return False

