#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/6/30 上午11:08
# @Author  : 武明辉
# @File    : MongoToMysql.py

import pymongo
import MySQLdb
from datetime import *


def start_MySQL():
    conn = MySQLdb.connect(
            host='localhost',
            user='root',
            passwd='root',
            db='wechat',
            charset='utf8')
    cur = conn.cursor()
    myConn_list = [conn, cur]
    return myConn_list


def close_MySQL(cur, conn):
    cur.close()
    conn.commit()
    conn.close()

if __name__ == "__main__":
    client = pymongo.MongoClient('mongodb://wmh:wmh666@127.0.0.1:27017/myinfo', 27017)
    myinfo = client['myinfo']

    wechats = myinfo['wechats']
    article = myinfo['article']

    conn, cur = start_MySQL()

    sql_w = 'insert into wechats(account,name,description,tags,clz) values(%s,%s,%s,%s,%s)'
    sql_a = 'insert into article(title,author,content,pub_date,wechats_id,url_o,url_c) values(%s,%s,%s,%s,%s,%s,%s)'
    cur.execute('set character_set_connection=utf8mb4;')
    for line in article.find():

        winfo = wechats.find_one({'_id': line['wechats_id']})
        print winfo
        if not winfo:
            print 'continue'
            continue
        cur.execute('select id from wechats where account = "%s"' % winfo['account'])
        w_id = cur.fetchone()
        if w_id:
            w_id = w_id[0]
            pub_date = line['pub_date']
            if pub_date:
                pub_date = datetime.strptime(pub_date, '%Y-%m-%d')
            cur.execute(sql_a, (line['title'], line['author'], line['content'], pub_date, w_id, line['url_o'], None))
            conn.commit()
        else:
            cur.execute(sql_w, (winfo['account'], winfo['name'], winfo['description'], None, None))
            id = int(cur.lastrowid)
            pub_date = line['pub_date']
            if pub_date:
                pub_date = datetime.strptime(pub_date, '%Y-%m-%d')
            cur.execute(sql_a, (line['title'], line['author'], line['content'], pub_date, id, line['url_o'], None))
            conn.commit()

    close_MySQL(cur, conn)
