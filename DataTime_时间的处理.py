# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 20:32:30 2018
Python中DataTime,时间的处理
@author: Administrator
"""
import datetime


d1 = datetime.datetime.now() # 获取当前时间
print(d1)

d2 = d1 + datetime.timedelta(hours=0.5)     #当前时间加上半小时
print(d2)

d3 = d2.strftime('%Y-%m-%d %H:%M:%S')   #格式化字符串输出
print(d3)
type(d3)

d4 = datetime.datetime.strptime(d3,'%Y-%m-%d %H:%M:%S') #将字符串转化为时间类型
print(d4)

d5=datetime.datetime.strptime('1970-01-01 00:00:00','%Y-%m-%d %H:%M:%S')
print(d5)