# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 08:49:17 2020

@author: Administrator
"""

import requests
from bs4 import BeautifulSoup
import time
#http://detail.zol.com.cn/cell_phone_index/subcate57_0_list_1_0_1_1_0_1.html
#http://detail.zol.com.cn/cell_phone_index/subcate57_0_list_1_0_1_1_0_2.html
data = []
for page in range(1, 10):
    url = 'http://detail.zol.com.cn/cell_phone_index/subcate57_0_list_1_0_1_1_0_{}.html'.format(page)
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
    }
    with requests.get(url,headers = headers) as response:
        time.sleep(2)
        bs = BeautifulSoup(response.text, features='html5lib')
        items = bs.select('.list-box .list-item')
        for item in items:
            phone_model = item.select_one('.pro-intro a').text
            if item.select_one('.price-box .price-type'):
                phone_price = item.select_one('.price-box .price-type').text
            else:
                phone_price = ''
            data.append({'phone_model': phone_model, 'phone_price' : phone_price})
    print('完成第{}页.'.format(page))

print(len(data))
for item in data:
    print(item)