# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 20:23:28 2020

@author: 86184
"""

#import urllib.request
import requests  # 获取网页内容
from bs4 import BeautifulSoup  # 解析网页内容
import os
import time

url='https://movie.douban.com/top250?start=0&filter='
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}

response = requests.get(url,headers=headers)
res=response.text
soup=BeautifulSoup(res,'lxml')
movielist = []
lis = soup.select("ol li")  # 选择ol li标签
for li in lis:
    #index = li.find('em').text  # 排名
    pic_link = li.find('div','pic').img['src'].strip()  #图片链接
    movielist.append(pic_link)

root_path = r'C:\Users\86184\Desktop\pic'

#利用split()函数获取url最后的文件名
for i in range(0,len(movielist),1):
    time.sleep(1)
    img_name = movielist[i].split('/')[-1]
    img_path = root_path + r'\{0}'.format(img_name)
    try:
        #如果根目录不存在就创建该根目录
        if not os.path.exists(root_path):
            os.makedirs(root_path)

        if not os.path.exists(img_path):
            r = requests.get(movielist[i])
            with open(img_path, 'wb') as f:
                f.write(r.content)
                f.close()
                print("文件保存成功")
        else:
            print("文件已存在")
    except:
        print("执行出错")





