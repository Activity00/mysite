#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/6/28 上午11:44
# @Author  : 武明辉
# @File    : wxqSpider.py
import scrapy

from weixin.items import ArticleItem


class WxqSpider(scrapy.Spider):
    """
    只用来搜集公众号，没有文章    
    """
    name = 'wxq'
    start_urls = ['http://www.weixinqun.com/openid', ]

    def parse(self, response):
        lis = response.xpath('//ul[@id="tab_head"]/li/div/a/@href').extract()
        for li in lis:
            yield scrapy.Request(response.urljoin(li), callback=self.parsewx)
        nextpage = response.xpath('//a[@class="pageNext"]/@href').extract_first()
        if nextpage:
            yield scrapy.Request(response.urljoin(nextpage), callback=self.parse)


    def parsewx(self, response):
        """ 解析微信链接界面 """
        title = response.xpath('//h2[@class="rich_media_title"]/text()').extract_first()
        pub_date = response.xpath('//em[@id="post-date"]/text()').extract_first()
        name = response.xpath('//div[@class="profile_inner"]/strong/text()').extract_first()
        author = response.xpath('//em[2]/text()').extract_first()
        account = response.xpath('//div[@class="profile_inner"]/p[1]/span/text()').extract_first()
        description = response.xpath('//div[@class="profile_inner"]/p[2]/span/text()').extract_first()
        content = response.xpath('//div[@id="page-content"]').extract_first()
        if title:
            title = title.strip()
        item = ArticleItem()
        item['title'] = title
        item['account'] = account
        item['name'] = name
        item['description'] = description
        item['content'] = content
        item['pub_date'] = pub_date
        item['url_o'] = response.url
        item['author'] = author

        yield item