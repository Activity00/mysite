# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class WeChartsItem(scrapy.Item):

    name = scrapy.Field()  # 公众号名字
    account = scrapy.Field()  # 账号名称
    description = scrapy.Field()  # 账号描述
    tags = scrapy.Field()  # 标签
    clz = scrapy.Field()  # 分类


class ArticleItem(WeChartsItem):
    '''继承自WeChartsItem'''
    title = scrapy.Field()  # 标题
    url_o = scrapy.Field()  # 原始 url链接
    url_c = scrapy.Field()  # 清洗过的链接  pk
    pub_date = scrapy.Field()  # 发表日期
    content = scrapy.Field()   # 原始内容
    author = scrapy.Field()  # 作者（默认原创）
    '''以下是article_date中的数据'''
    readcount = scrapy.Field()  # 阅读量
    favorcount = scrapy.Field()  # 点赞量
    comment = scrapy.Field()  # 评论


class XinbangItem(WeChartsItem):
    '''新榜数据'''
    rank = scrapy.Field()  # 排名
    pub_b = scrapy.Field()  # 发布b
    pub_c = scrapy.Field()  # 发布c
    totalread = scrapy.Field()  # 总阅读量
    toptl = scrapy.Field()  # 头条次数
    avg = scrapy.Field()  # 平均数
    max = scrapy.Field()  # max
    favtotal = scrapy.Field()  # 点赞总数
    xbzs = scrapy.Field()  # 新榜指数
    get_date = scrapy.Field()  # 爬取的时间
    sha = scrapy.Field()  # 网页的hash值
    tag = scrapy.Field()  # 标签


