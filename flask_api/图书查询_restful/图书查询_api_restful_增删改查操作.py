# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 22:10:29 2020

@author: Administrator
"""

import requests
import json


url = 'http://127.0.0.1:5000/books'

# 查询店内所有图书
all_books = requests.get(url)
print(all_books.text)

# 按id查询指定图书
single_book = requests.get(url+'/1')
print(single_book.text)

single_book = requests.get(url+'/2')
print(single_book.text)

single_book = requests.get(url+'/3')
print(single_book.text)

# 增加新图书
new_book = {
    'title': '流浪地球',
    'auther': '刘慈欣',
    'price':20
}

new = requests.post(url,new_book)
print(new.text)
# 验证增加结果
all_books = requests.get(url)
print(all_books.text)


# 修改图书属性
update_book = {
    'title': '赡养人类',
    'auther': '刘慈欣',
    'price':18
}
update = requests.put(url+'/4',update_book)
print(update.text)
# 验证修改结果
single_book = requests.get(url+'/4')
print(single_book.text)


# 删除图书
delete = requests.delete(url+'/4')
print(delete.text)
delete = requests.delete(url+'/3')
print(delete.text)
# 验证删除结果
all_books = requests.get(url)
print(all_books.text)
