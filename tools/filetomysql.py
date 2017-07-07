#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/6/29 下午4:12
# @Author  : 武明辉
# @File    : filetomysql.py
import json
import os

import MySQLdb
from datetime import *

LOCALHOST = 'localhost'
USERNAME = 'root'
PWD = 'root'
DBNAME = 'wechat'
# DPATH = '/home/minghui/dbbackup'
DPATH = '../'


def removefile(filenames):
    for f in filenames:
        os.remove(DPATH + f)


def getValidFilename(filenames):
    """
    
    :param filenames: 可用文件名字列表 
    :return: 当前要存文件列表
    """
    files = []
    for f in filenames:
        if '2017-' in f or '2018-' in f:
            files.append(f)

    if len(files) > 1:  # 有可用数据库
        datemax = datetime.strptime(files[0], '%Y-%m-%d-%X')
        for f in files:
            if datetime.strptime(f, '%Y-%m-%d-%X') > datemax:
                datemax = datetime.strptime(f, '%Y-%m-%d-%X')
        files.remove(datemax.strftime("%Y-%m-%d-%X"))
        return files
    elif len(files) == 1:
        datemax = datetime.strptime(files[0], '%Y-%m-%d-%X')
        if datemax + timedelta(hours=2) > datetime.now():
            files.remove(datemax.strftime("%Y-%m-%d-%X"))
        return files
    else:
        return []


def saveToMySql(filenames):
    """
    根据文件名字列表把数据存入Mysql数据库
    :param filenames: 
    :return: 
    """
    def save(filename):
        db = MySQLdb.connect(LOCALHOST, USERNAME, PWD, DBNAME, charset="utf8")
        cursor = db.cursor()
        sql_w = 'insert into wechats(account,name,description,tags,clz) values(%s,%s,%s,%s,%s)'
        sql_a = 'insert into article(title,author,content,pub_date,wechats_id,url_o,url_c) values(%s,%s,%s,%s,%s,%s,%s)'
        sql_d = ''
        cursor.execute('set character_set_connection=utf8mb4;')
        with open(DPATH + filename, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                line = json.loads(line)
                cursor.execute('select id from wechats where account = "%s"' % line['account'])
                w = cursor.fetchone()
                if w:  # 存在公众号
                    try:
                        cursor.execute('select id from article where title = "%s"' % line['title'])
                    except:
                        continue
                    a = cursor.fetchone()
                    if not a:   # 文章不存在
                        pub_date = line['pub_date']
                        if pub_date:
                            pub_date = datetime.strptime(pub_date, '%Y-%m-%d')
                        cursor.execute(sql_a, (line['title'], line['author'], line['content'], pub_date, w[0], line['url_o'], None))
                        db.commit()

                else:  # 不存在公众号
                    cursor.execute(sql_w, (line['account'], line['name'], line['description'], None, line['clz']))
                    id = int(cursor.lastrowid)
                    pub_date = line['pub_date']
                    if pub_date:
                        pub_date = datetime.strptime(pub_date, '%Y-%m-%d')
                    cursor.execute(sql_a, (line['title'], line['author'], line['content'], pub_date, id, line['url_o'], None))
                    db.commit()

        cursor.close()
        db.close()

    for name in filenames:
        save(name)
    return True


if __name__ == '__main__':
    dirlist = os.listdir(DPATH)
    filenames = getValidFilename(dirlist)
    if saveToMySql(filenames):
        removefile(filenames)



