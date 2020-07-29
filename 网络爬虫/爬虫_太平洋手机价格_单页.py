# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 08:49:17 2020

@author: Administrator
"""

import requests
from bs4 import BeautifulSoup
url = 'http://detail.zol.com.cn/cell_phone_index/subcate57_0_list_1_0_1_1_0_1.html'
with requests.get(url) as response:
    bs = BeautifulSoup(response.text, features='html5lib')
    items = bs.select('.list-box .list-item')
    for item in items:
        phone_model = item.select_one('.pro-intro a').text
        phone_price = item.select_one('.price-box .price-type').text
        print(phone_model, phone_price)