#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from lxml.html import etree
import sqlite3
import re
from pprint import pprint

conn = sqlite3.connect('top_movies.db')
url = 'http://www.bd-film.co/hjtj/24644.htm'
res = requests.get(url)
dom_tree = etree.HTML(res.content)
all_h4 = dom_tree.xpath('//*[@id="collelction_content"]//h4')
all_div = dom_tree.xpath('//*[@id="collelction_content"]//div')
# [re.findall('(?<=\d\.).*', div.xpath('.//text()')[0])[0].strip(), float(re.findall('.*(?=分)', div.xpath('.//text()')[1])[0]), div.xpath('.//text()')[-1]]
# all_div = [div for div in all_div if len(div.xpath('.//text()'))]
# pprint(all_div)
j = -10
for h4 in all_h4:
    i = 0
    h4 = h4.xpath('.//text()')
    h4 = ''.join(h4)
    conn.execute('CREATE TABLE IF NOT EXISTS "{}" (ID INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT, score REAL, url TEXT)'.format(h4))
    conn.commit()
    # print(h4)
    j += 11
    for i in range(j, j + 10):
        try:
            content = all_div[i].xpath('.//text()')
            title = re.findall('(?<=\d\.).*', content[0])[0].strip()
            score = float(re.findall('.*(?=分)', content[1])[0])
            down_url = '下载' in content[-1] and '无' or content[-1]
            conn.execute(
                'INSERT INTO "{}" (name, score, url) VALUES ("{}", {}, "{}")'.format(h4, title, score, down_url))
            conn.commit()
            # print(title, score, down_url)
        except:
            print('录入失败：', h4, all_div[i].xpath('.//text()'))
conn.close()
# conn = sqlite3.connect('movies.db')
# conn.execute('CREATE TABLE IF NOT EXISTS ')
