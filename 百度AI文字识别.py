# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 11:26:57 2018

@author: Administrator
"""
APP_ID = '11152511'
API_KEY = 'ueBdIukdXt1l7HFwD8ULehip'
SECRET_KEY = 'ZcOnmjOLRGIiKwR4cizGO9doQA5O9zdW'

# 初始化文字识别分类器
aipOcr=AipOcr(APP_ID, API_KEY, SECRET_KEY)

# 读取图片  
filePath =r"d:\_python\3859.bmp"  


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 定义参数变量
options = {
    'detect_direction': 'true',
    'language_type': 'CHN_ENG',
}

# 网络图片文字文字识别接口
result = aipOcr.webImage(get_file_content(filePath),options)
text = result['words_result'][0]
text['words']
