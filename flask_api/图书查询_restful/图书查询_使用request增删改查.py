# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 22:10:29 2020

@author: Administrator
"""

import requests
import json


url = 'http://127.0.0.1:5000/api/books/'
url_up = 'http://127.0.0.1:5000/api/books/up/'

# 查询店内所有图书
response1 = requests.get(url)
print(response1.text)

# 按id查询指定图书
response2 = requests.get(url+'4')
print(response2.text)

# 增加新图书
new_book = {
    'id': 4,
    'title': '流浪地球',
    'auther': '刘慈欣',
    'price':20
}

response3 = requests.post(url,new_book)
print(response3.text)

# 修改图书价格
update_book = {
    'title': '赡养人类',
    'auther': '刘慈欣',
    'price':18
}

response4 = requests.put(url+'4',update_book)
print(response4.text)

# 删除图书
response5 = requests.delete(url+'3')
print(response5.text)

