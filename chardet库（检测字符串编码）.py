# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 10:15:17 2018
chardet 库
@author: Administrator
"""
import chardet

chardet.detect(b'Hello, world!')

data = '离离原上草，一岁一枯荣'.encode('gbk')
chardet.detect(data)

data = '离离原上草，一岁一枯荣'.encode('utf-8')
chardet.detect(data)

data = '最新の主要ニュース'.encode('euc-jp')
chardet.detect(data)