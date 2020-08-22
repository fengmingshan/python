# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 14:17:53 2020

@author: Administrator
"""

import requests
import os


url = 'http://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png'
root_path = r'C:\Users\Administrator\Desktop\pic'

#利用split()函数获取url最后的文件名
img_name = url.split('/')[-1]

img_path = root_path + r'\{0}'.format(img_name)

try:
    #如果根目录不存在就创建该根目录
    if not os.path.exists(root_path):
        os.makedirs(root_path)

    if not os.path.exists(img_path):
        r = requests.get(url)
        with open(img_path, 'wb') as f:
            f.write(r.content)
            f.close()
            print("文件保存成功")
    else:
        print("文件已存在")
except:
    print("执行出错")
