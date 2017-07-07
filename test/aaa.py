#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/4/26 下午5:48
# @Author  : 武明辉
# @File    : aaa.py
import MySQLdb
from wechatsogou.tools import *
from wechatsogou import *

conn = MySQLdb.connect(
            host='localhost',
            user='root',
            passwd='root',
            db='wechat',
            charset='utf8')
cur = conn.cursor()
sql_w = 'insert into wechats(account,name,description,tags,clz) values(%s,%s,%s,%s,%s)'

# cur.execute(sql_w, ('account', 'name', 'description', None, None))
a = 'fasfsadf"aaa\"fsda'
cur.execute('select id from article where title = "%s"', (a,))
data = cur.fetchone()
print data
id = int(cur.lastrowid)
print id
conn.commit()
cur.close()
conn.close()
