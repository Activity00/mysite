#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/5/2 上午11:25
# @Author  : 武明辉
# @File    : testmongodb.py
# coding：utf-8

import pymongo
from bson import ObjectId
from pymongo import MongoClient

# 连接数据库
client = MongoClient('mongodb://root:root@127.0.0.1:27017/myinfo')
# 指定数据库名称
db = client['myinfo']
# 获取集合名称
wechats = db['wechats']
# 查询单个文档
w = db['wechats'].find_one({'account': 'fuxingzhongyiwang'}, {'_id': 1})
print w