#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/6/28 下午12:04
# @Author  : 武明辉
# @File    : csmSpider.py
import scrapy
from scrapy.exceptions import IgnoreRequest

from weixin.items import ArticleItem


class CsmSpider(scrapy.Spider):
    name = 'csm'
    start_urls = ['http://chuansong.me/', ]
    custom_settings = {'ITEM_PIPELINES': {'weixin.pipelines.DropPipeline': 100,
                                          #'weixin.pipelines.MongoPipeline': 200,
                                          'weixin.pipelines.FilePipeline': 200,
                                          },
                       }

    def parse(self, response):
        # tagurls = response.xpath('//ul[@class="simple_profile_tabs"]//li/a/@href').extract()
        # tagurls.append('http://chuansong.me/')
        # for tagurl in tagurls:
        #     yield scrapy.Request(response.urljoin(tagurl), callback=self.parsetopic)
        yield scrapy.Request(response.urljoin('http://chuansong.me/'), callback=self.parsetopic)

    def parsetopic(self, response):
        account_urls = response.xpath('//div[@class="feed_item_photo"]//a/@href').extract()
        for au in account_urls:
            yield scrapy.Request(response.urljoin(au), callback=self.parseAccount)
        next_url = response.xpath(u'//a[contains(text(),"下一页")]/@href').extract_first()
        if next_url:
            yield scrapy.Request(response.urljoin(next_url), callback=self.parsetopic)

    def parseAccount(self, response):
        # wxid = response.xpath(u'//div[contains(text(),"微信ID")]/text()').extract_first()
        account = None
        try:
            account = response.url.split('?')[0].split('/')[-1].strip()
        except:
            pass
        if not account:
            raise IgnoreRequest('err:get account err in parseAccount')
        description = response.xpath('//div[@class="section"]//div[@class="inline"]/span/text()').extract_first()
        name = response.xpath('//div[@class="row topic_name_editor"]//h1[@class="inline"]/span/text()').extract_first()
        meta = {'account': account, 'name': name, 'description': description}

        lis = response.xpath('//div[@class="feed_item_question"]/h2/span/a/@href').extract()
        for li in lis:
            yield scrapy.Request(response.urljoin(li), callback=self.parseArticle, meta=meta)

        next_page = response.xpath(u'//a[contains(text(),"下一页")]/@href').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parseAccount)

    def parseArticle(self, response):
        meta = response.meta
        item = ArticleItem()
        item['account'] = meta['account']
        item['name'] = meta['name']
        item['description'] = meta['description']
        item['title'] = response.xpath('//h2[@class="rich_media_title"]/text()').extract_first()
        item['content'] = response.xpath('//div[@id="page-content"]').extract_first()
        item['pub_date'] = response.xpath('//em[@id="post-date"]/text()').extract_first()
        item['url_o'] = response.url
        item['author'] = response.xpath('//em[2]/text()').extract_first()
        yield item


