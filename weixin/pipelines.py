# -*- coding: utf-8 -*-
import json

import pymongo
import scrapy
from bson import ObjectId
from scrapy.exceptions import DropItem
from datetime import *


class DropPipeline(object):
    """ 去掉无效的数据
        掉丢不可用数据
        优先级最高
    """
    def process_item(self, item, spider):
        if not item['account'] and not item['name']:
            raise DropItem('drop a error info ％s：' % item)
        return item


class MongoPipeline():
    """ 存入Mongodb数据库"""
    collection_wechats = 'wechats'
    collection_article = 'article'
    collection_article_data = 'article_data'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'myinfo')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()
        spider.logger.info('all inserted')

    def process_item(self, item, spider):
        try:
            w = self.db[self.collection_wechats].find_one({'account': item['account']}, {'_id': 1})
            # 是否存在该微信帐号，存在就～，不存在就直接插入
            if w:   # account exits
                # 是否存在这篇文章，存在就扔了，不存在就插入新文章
                title = self.db[self.collection_article].find_one({'wechats_id': ObjectId(w['_id']),
                                                                   'title': item['title']}, {'_id': 1})
                if title:  # if cleard url in mongo.if true dorp this item
                    return item
                _id = self.db[self.collection_wechats].find_one({'account': item['account']}, {'_id': 1})['_id']
                self.db[self.collection_article].insert({'url_o': item['url_o'], 'title': item['title'],
                                                         'author': item['author'],
                                                         'content': item['content'], 'pub_date': item['pub_date'],
                                                         'wechats_id': ObjectId(_id)})
            else:  # account not exist
                spider.logger.info('pp to insert...')
                _id = self.db[self.collection_wechats].insert({'account': item['account'], 'name': item['name'],
                                                               'description': item['description']})
                self.db[self.collection_article].insert({'url_o': item['url_o'], 'title': item['title'],
                                                         'content': item['content'], 'author': item['author'],
                                                         'pub_date': item['pub_date'], 'wechats_id': ObjectId(_id)})
            spider.logger.info('insert one more')
        except Exception as e:
            spider.logger.info('insert mongodb error:%s' % e)
        return item


class FilePipeline():
    """ 存入文件"""

    def open_spider(self, spider):
        self.createfile()

    def close_spider(self, spider):
        self.closefile()

    def closefile(self):
        if self.f:
            self.f.close()
            self.f = None

    def createfile(self):
        self.last = datetime.now()
        datestr = self.last.strftime("%Y-%m-%d-%X")
        self.f = open('%s' % datestr, 'a')

    def appenditem(self, item, spider):
        """
        追加item
        :param item: 
        :param spider: 
        :return: 
        """
        try:
            itemstr = json.dumps(dict(item))
            self.f.write(itemstr + '\n')
        except Exception as e:
            spider.logger.error('%s' % e)

    def process_item(self, item, spider):
        if not self.f or self.last + timedelta(hours=1) < datetime.now():
            # 变
            self.closefile()
            self.createfile()
            self.appenditem(item, spider)
        else:
            self.appenditem(item, spider)  # 保持






