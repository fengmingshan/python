# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 11:42:45 2018

@author: Administrator
"""
import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt

%matplotlib inline #使图片内嵌交互环境显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

# =============================================================================
# 画折线图
# =============================================================================
data_every_month = pd.read_excel('data_every_month.xls')
y = data_every_month['nums'].T.values
x = range(0,len(y))
plt.figure(figsize=(15, 8))
plt.plot(x,y,'')  
plt.xticks((0,20,40,60,80,100,120),('200504','200912','201108','201306','201502','201610',''))
plt.xlabel('年月')
plt.ylabel('XX事件数')
plt.title('每月XX事件数')
plt.show()

# =============================================================================
# 取片段数据，同一张图画两条折线
# =============================================================================
y1 = y[79:91]
y2 = y[91:102]

x1=range(0,len(y1))
x2=range(0,len(y2))
plt.figure(figsize=(15, 8))
plt.plot(x1,y1,'',label="2015年")
plt.plot(x2,y2,'',label="2016年")
plt.title('2015-2016年月XX事件数')
plt.legend(loc='upper right')
plt.xticks((0,2,4,6,8,10),('1月','3月','5月','7月','9月','11月'))
plt.xlabel('月份')
plt.ylabel('XX事件数')
plt.grid(x1)
plt.show()
