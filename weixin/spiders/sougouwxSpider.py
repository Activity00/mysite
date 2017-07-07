# -*- coding: utf-8 -*-
# @Time    : 17/5/3 下午2:27
# @Author  : 武明辉
# @File    : sougouwxSpider.py
import scrapy
from weixin.items import ArticleItem


class SougouwxSpider(scrapy.Spider):

    name = 'sgwx'
    start_urls = ['http://wx.sougou.com/', ]

    def parse(self, response): 
        for i in range(20):
            for j in range(1, 14):
                url = 'http://wx.sogou.com/pcindex/pc/pc_%s/%s.html' % (i, j)
                yield scrapy.Request(url=url, callback=self.after_get)
    
    def after_get(self, response):

        urls = response.xpath('//div[@class="txt-box"]/h3/a/@href').extract()
        if urls:
            for url in urls:
                yield scrapy.Request(url, self.parsewx)

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
