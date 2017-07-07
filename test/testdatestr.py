#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/4/27 上午10:46
# @Author  : 武明辉
# @File    : testdatestr.py
import time

a = '2017-01-31'
b = '2017-1-1－a'


def __is_valid_datestr(str):
    try:
        time.strptime(str, '%Y-%m-%d')
        return True
    except Exception:
        return False
print __is_valid_datestr(a)
print __is_valid_datestr(b)