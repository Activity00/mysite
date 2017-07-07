#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re, requests, urllib2, pymysql

def getHtml(url):
    #url1= url.encode('utf-8')
    page = urllib2.urlopen(url)
    html = page.read()
    return html

def getRurl(url):
    #linshi_link = url.encode('utf-8')
    timestamp = re.findall('timestamp=(\d+)',url)[0]
    signature = re.findall('signature=(.+)',url)[0]
    s = 'http://mp.weixin.qq.com/mp/getcomment?src=3&timestamp=%s&ver=1&signature=%s'%(timestamp,signature)
    return s

def getName(html):
    reg = r'meta_nickname">(.*)</span>'
    name = re.compile(reg)
    namelist = re.findall(name, getHtml(url))
    return namelist[0].decode('utf-8')

def getTitle(url):
    reg = r'<title>(.*)</title>'
    title = re.compile(reg)
    titlelist = re.findall(title, getHtml(url))
    return titlelist[0].decode('utf-8')

def getReadnum(url):
    r = requests.get(getRurl(url))
    if r.status_code==200:
        c = r.content
        readnum = re.findall('"read_num":(\d+)',c)[-1]
        return readnum

def getLikenum(url):
    r = requests.get(getRurl(url))
    if r.status_code==200:
        c=r.content
        likenum = re.findall('"like_num":(\d+)',c)[-1]
        return likenum

def getComment(url):
    reg =r'"content":"(.*)","'
    comment =re.compile(reg)
    commentlist =re.findall(comment,getRurl(url))
    return commentlist

url='http://mp.weixin.qq.com/s?src=3&timestamp=1493174527&ver=1&signature=Oh7JEQRctQUnVoKJc6k*VBRTQTyWQ7AhJOeuTwgyjnaPFnwrDycyX3819frnY0ayfhipnGCU4RZ-PgmrwCtPJWin3fvHlCkHRA3g3H01cyxr9KEpSLjrAkyXnfOWnNIyNZbTKtx*S7WgSlNl*DtISVmi9bkh*MJHdoX0ii70Xm8='
a = getName(url)
b = getTitle(url)
i = j = 0
if(getReadnum(url)is not None):
    i=getReadnum(url)
if(getLikenum(url)is not None):
    j = getLikenum(url)
print a
print b
print i
print j

x='jfkasl'
y='jfkldasjf'
w=1
e=3232
conn = pymysql.connect(host='127.0.0.1', user='root', password='root', port=3306, db='myinfo')
cursor = conn.cursor()
cursor.execute("insert into test(name,title,readnumber,likenumber) VALUES(%s,%s,%s,%s)", (x, y, w, e))
conn.commit()
conn.close()