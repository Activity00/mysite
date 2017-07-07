#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/6/26 下午2:46
# @Author  : 武明辉
# @File    : tempurls.py
import time
from selenium import webdriver
# 1.创建浏览器对象

browser = webdriver.Firefox()
browser.get('http://weixin.sogou.com/weixin?type=2&query=大明&ie=utf8&s_from=input&_sug_=n&_sug_type_=1&w=01015002&oq=&ri=14&sourceid=sugg&sut=51409&sst0=1498467049643&lkt=0%2C0%2C0&p=40040108')
time.sleep(3)
# 获取想要的内容
#根据内容找到节点
#browser.find_element_by_link_text("下一页").click()

print browser.page_source

browser.quit()
