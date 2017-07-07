#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/4/26 下午5:40
# @Author  : 武明辉
# @File    : test_selenium.py
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

from selenium import webdriver
from scrapy.selector import Selector
import time
import os

def writeFile(dirPath, page):
    data = Selector(text = page).xpath("//td[@class='zwmc']/div/a")
    titles = data.xpath('string(.)').extract()
    timeMarks = Selector(text = browser.page_source).xpath("//td[@class='gxsj']/span/text()").extract()
    links = Selector(text = browser.page_source).xpath("//td[@class='zwmc']/div/a/@href").extract()

    for i in range(len(titles)):
        fileName = titles[i].replace(':', '-').replace('/', '-').replace('\\', '-').replace('*', 'x').replace('|', '-').replace('?', '-').replace('<', '-').replace('>', '-').replace('"', '-').replace('\n', '-').replace('\t', '-')
        filePath = dirPath + os.sep + fileName + '.txt'

        with open(filePath, 'w') as fp:
            fp.write(titles[i])
            fp.write('$***$')
            fp.write(timeMarks[i])
            fp.write('$***$')
            fp.write(links[i])


def searchFunction(browser, url, keyWord, dirPath):
    browser.get(url)

#勾选城市
    browser.find_element_by_xpath("//input[@id='buttonSelCity']").click()
    browser.find_element_by_xpath("//table[@class='sPopupTabC']/tbody/tr[1]/td/label/input[@iname='北京']").click()
    browser.find_element_by_xpath("//table[@class='sPopupTabC']/tbody/tr[1]/td/label/input[@iname='上海']").click()
    browser.find_element_by_xpath("//table[@class='sPopupTabC']/tbody/tr[3]/td/label/input[@iname='南京']").click()
    browser.find_element_by_xpath("//table[@class='sPopupTabC']/tbody/tr[4]/td/label/input[@iname='苏州']").click()
    browser.find_element_by_xpath("//table[@class='sPopupTabC']/tbody/tr[4]/td/label/input[@iname='无锡']").click()
    browser.find_element_by_xpath("//div[@class='sPopupTitle250']/div/a[1]").click()

#定位搜索框
    searchBox = browser.find_element_by_xpath("//div[@class='keyword']/input[@type='text']")

#发送搜索内容
    searchBox.send_keys(keyWord)

#确认搜索
    browser.find_element_by_xpath("//div[@class='btn']/button[@class='doSearch']").click()

    totalCount = Selector(text = browser.page_source).xpath("//span[@class='search_yx_tj']/em/text()").extract()[0]
    pageOver = int(totalCount) / 40
    for i in range(pageOver):
        time.sleep(3)
        writeFile(dirPath, browser.page_source)
        browser.find_element_by_link_text("下一页").click()

    time.sleep(3)
    writeFile(dirPath, browser.page_source)


if __name__ == '__main__':
    print 'START'
    url = 'http://www.zhaopin.com/'
    keyWord = u"华为技术有限公司"
    dirPath = keyWord + u"招聘信息"

    if not os.path.exists(dirPath):
        os.makedirs(dirPath)

#定义一个火狐浏览器对象
    browser = webdriver.Firefox()
    searchFunction(browser, url, keyWord, dirPath)
    browser.close()
    print 'END'