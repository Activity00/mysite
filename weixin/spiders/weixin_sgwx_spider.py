#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/6/23 下午5:49
# @Author  : 武明辉
# @File    : weixin_sgwx_spider.py
# -*- coding: utf-8 -*-
# @Time    : 17/5/3 下午2:27
# @Author  : 武明辉
# @File    : sougouwxSpider.py
import scrapy
from wechatsogou import WechatSogouApi

from weixin.items import ArticleItem


class SougouwxSpider(scrapy.Spider):
    """
    加入github sgwx 但是存在验证码问题
    """
    name = 'sgwx_key'
    start_urls = ['http://wx.sougou.com/', ]
    custom_settings = {'DOWNLOADER_MIDDLEWARES': {'weixin.middlewares.JavaScriptMiddleware': 900,
                                                  'weixin.middlewares.ProxytxtMiddleware': None,
                                                  },
                       }

    def start_requests(self):
        # urls = self.getmoreurls()
        wechats = WechatSogouApi()
        wechat_articles = wechats.search_article_info('数字化非')
        urls = []
        for article in wechat_articles:
            urls.append(article['gzh']['article_list_url'])
        for url in urls:
            yield scrapy.Request(url=url, callback=self.after_get)

    def getmoreurls(self):
        wechats = WechatSogouApi()
        txt = open('key_words.txt', 'r').read()
        ret = []
        for key in txt:
            print key
            while True:
                i = 1
                wechat_articles = wechats.search_article_info(key, i)
                if not wechat_articles:
                    break
                for article in wechat_articles:
                    try:
                        ret.append(article['gzh']['article_list_url'])
                    except:
                        break
                i += 1
        return ret

    def after_get(self, response):
        urls = response.xpath('//div[@class="weui_msg_card_bd"]//div/h4/@hrefs').extract()
        if urls:
            for url in urls:
                yield scrapy.Request('https://mp.weixin.qq.com'+url, self.parsewx)

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
