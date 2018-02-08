#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import re
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from lxml.html import etree
import sqlite3
from fake_useragent import UserAgent
import time

s_time = time.time()
ua = UserAgent()
# print(type(ua.random))

conn = sqlite3.connect('bd_film_NoDown.db')

count = 0
URL = 'http://www.bd-film.co/'
res = requests.get(url=URL, headers={'User-Agent': ua.random})
dom_tree = etree.HTML(res.content)
hrefs = dom_tree.xpath('//div[@class="span6 shadow-frame"]/a/@href')
names = dom_tree.xpath('//div[@class="span6 shadow-frame"]/a/h4/text()')
print(names)
New_urls = [urljoin(URL, i) for i in hrefs]
for i in range(len(names)):
    print('*' * 5)
    name = names[i]
    conn.execute(
        'CREATE TABLE IF NOT EXISTS "{}" (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, info TEXT, score REAL, up_time DATE, url TEXT)'.format(
            name))
    New_url = New_urls[i]
    res = requests.get(url=New_url, headers={'User-Agent': ua.random})
    dom_tree = etree.HTML(res.content)
    page_num = int(dom_tree.xpath('//div[@class="pagination"]/ul/li[last()-2]/a/text()')[0])
    # print(page_num)
    for j in range(1, page_num + 1):
        print('*' * 10)
        page_url = urljoin(New_url, 'index_{}.htm'.format(j))
        # print(page_url)
        res = requests.get(url=page_url, headers={'User-Agent': ua.random})
        dom_tree = etree.HTML(res.content)
        tds = dom_tree.xpath('//table[@class="table table-striped shadow-frame"]/tbody/tr/td')
        for td in tds:
            print('*' * 15)
            content = td.xpath('./a[last()]/span/text()')[0]
            title = len(re.findall('(?<=《).*(?=》)', content)) and re.findall('(?<=《).*(?=》)', content)[
                0] or '@' + content
            info = len(re.findall('.*(?=《)', content)) and re.findall('.*(?=《)', content)[0] or '@' + content
            score = len(td.xpath('./span/text()')) and float(td.xpath('./span/text()')[0]) or -11
            up_time = td.xpath('./div[@class="text-info f-right"]/text()')[0]
            url = td.xpath('./a[last()]/@href')[0]

            # dcap = dict(DesiredCapabilities.PHANTOMJS)
            # dcap['phantomjs.page.settings.userAgent'] = (ua.random)
            # driver = webdriver.PhantomJS(desired_capabilities=dcap)
            # driver.get(url=url)
            # driver.implicitly_wait(3)
            # dom_tree = etree.HTML(driver.page_source)
            # down_url = 'baidu' in dom_tree.xpath('//td[@class="bd-address"][1]/div/i/@class')[0] and \
            #            dom_tree.xpath('//td[@class="bd-address"][1]/div/a/@href')[0] + '密码：' + \
            #            dom_tree.xpath('//td[@class="bd-address"][1]/div/span/text()')[0] or \
            #            dom_tree.xpath('//td[@class="bd-address"][1]/div/a/@href')[0]
            # driver.close()

            conn.execute(
                'INSERT INTO "{}" (title, info, score, up_time, url) VALUES ("{}","{}",{},"{}","{}")'.format(
                    name, title, info, score, up_time, url))
            conn.commit()
            count += 1
            print(count, title, info, score, up_time, url)
conn.close()

e_time = time.time()
print('\n耗时：{}'.format(e_time - s_time))
print('\n共采集 {} 条'.format(count))
