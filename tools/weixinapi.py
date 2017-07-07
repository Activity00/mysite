#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/6/23 下午4:26
# @Author  : 武明辉
# @File    : weixinapi.py

import requests
from wechatsogou import WechatSogouApi

"""
 微信app
"""
r = requests.get('http://weixin.sogou.com/')
cookies = r.cookies
print cookies
print r.headers
url = 'http://weixin.sogou.com/weixin?type=2&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_='
print url.format('大明明')
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:54.0) Gecko/20100101 Firefox/54.0',
           'Host': 'weixin.sogou.com',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Referer': 'http://weixin.sogou.com/',
           'allow_redirects': 'true'}

r = requests.get(url=url, headers=headers, cookies=cookies)
print type(r)
print r.text

class WeixinApi():
    def __init__(self):
        pass

