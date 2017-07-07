#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/4/26 下午4:03
# @Author  : 武明辉
# @File    : test.py
import json
from datetime import *

from weixin.items import ArticleItem

f = open('aaaa', 'r')
for x in f.readlines():
    a = json.loads(x)
    print a['name']
