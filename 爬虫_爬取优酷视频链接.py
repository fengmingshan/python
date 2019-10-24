# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-10-23 23:10:10
# @Last Modified by:   Administrator
# @Last Modified time: 2019-10-23 23:19:17
import requests
from bs4 import BeautifulSoup

url = 'http://list.youku.com/category/video'
with requests.get(url) as response:
	bs = BeautifulSoup(response.text, features='html5lib')
	items = bs.select('.category_selected')
	for item in items:
		print(item)
