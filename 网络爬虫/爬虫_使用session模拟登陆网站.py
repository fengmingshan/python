# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 20:19:12 2018

@author: Administrator
"""

import requests

passwd_dict ={'username':'qjwx','password':'a123456'}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}

session = requests.session()
res = session.post(url='http://218.63.75.44:8000/login',data=passwd_dict,headers = headers).text
res
res1 = session.get('http://218.63.75.44:8000/rsrp_grid').text
res

