# -*- coding: utf-8 -*-
# @Time    : 17/4/24 下午5:52
# @Author  : 武明辉
# @File    : cmdline.py
import scrapy.spidermiddlewares.httperror
import scrapy.cmdline
import os
import time
if __name__ == '__main__':
    # 三月份新榜的数据
    #scrapy.cmdline.execute(['scrapy', 'crawl', 'weixin_xb'])
    #scrapy.cmdline.execute(['scrapy', 'crawl', 'test'])git
    # scrapy.cmdline.execute(['scrapy', 'crawl', 'sgwx'])
#    while True:
#        time.sleep(1200)
    #os.system("scrapy crawl sgwx_key")
    # scrapy.cmdline.execute(['scrapy', 'crawl', 'sgwx_key'])
    scrapy.cmdline.execute(['scrapy', 'crawl', 'csm'])