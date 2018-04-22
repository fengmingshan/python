# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 11:42:45 2018

@author: Administrator
"""
import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
import xlsxwriter

path = r'd:\test' + '\\'  

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

# =============================================================================
# 画折线图
# =============================================================================
data_every_month = pd.read_excel(path +'data_every_month.xls')
y = data_every_month['nums'].T.values
x = range(0,len(y))
plt.figure(figsize=(7, 4))
plt.plot(x,y,'')  
plt.xticks((0,20,40,60,80,100,120),('200504','200912','201108','201306','201502','201610',''))
plt.xlabel('年月')
plt.ylabel('XX事件数')
plt.title('每月XX事件数')
plt.savefig(path + "123.png",format='png', dpi=200)  
plt.show()
plt.close()

# =============================================================================
# 取片段数据，同一张图画两条折线
# =============================================================================
y1 = y[79:91]
y2 = y[91:102]

x1=range(0,len(y1))
x2=range(0,len(y2))
plt.figure(figsize=(7, 4))
plt.plot(x1,y1,'',label="2015年")
plt.plot(x2,y2,'',label="2016年")
plt.title('2015-2016年月XX事件数')
plt.legend(loc='upper right')
plt.xticks((0,2,4,6,8,10),('1月','3月','5月','7月','9月','11月'))
plt.xlabel('月份')
plt.ylabel('XX事件数')
plt.grid(x1)
plt.savefig(path + "456.png",format='png', dpi=200)  
plt.show()
plt.close()

# =============================================================================
# 读取小时频数数据，画重叠的条形图
# =============================================================================
data_hour2015 = pd.read_excel(path +'data_hour2015.xlsx')
data_hour2016 = pd.read_excel(path +'data_hour2016.xlsx')
plt.figure(figsize=(7, 4))
data_hour2015['nums'].T.plot.bar(color='g',alpha=0.6,label='2015年')
data_hour2016['nums'].T.plot.bar(color='r',alpha=0.4,label='2016年')
plt.xlabel('小时')
plt.ylabel('XX事件数量')
plt.title('XX事件数小时分布')
plt.legend(loc='upper right')
plt.savefig(path + "789.png",format='png', dpi=200)  
plt.show()
plt.close()


# =============================================================================
# 读取周频数数据，画非重叠的条形图
# =============================================================================
data_week2015 = pd.read_excel(path +'data_week2015.xlsx')['nums'].T.values
data_week2016 = pd.read_excel(path +'data_week2016.xlsx')['nums'].T.values
plt.figure(figsize=(7, 4))
xweek=range(0,len(data_week2015))
xweek1=[i+0.3 for i in xweek]
plt.bar(xweek,data_week2015,color='g',width = .3,alpha=0.6,label='2015年')
plt.bar(xweek1,data_week2016,color='r',width = .3,alpha=0.4,label='2016年')
plt.xlabel('周')
plt.ylabel('XX事件数量')
plt.title('XX事件数周分布')
plt.legend(loc='upper right')
plt.xticks(range(0,7),['星期日','星期一','星期二','星期三','星期四','星期五','星期六'])
plt.savefig(path + "890.png",format='png', dpi=200)  
plt.show()
plt.close()

data_bar = pd.read_excel(path +'data_bar.xlsx')
label = data_bar['wfxw'].T.values
xtop = data_bar['nums'].T.values
idx = np.arange(len(xtop))
fig = plt.figure(figsize=(7,4))
plt.barh(idx, xtop, color='b',alpha=0.6)
plt.yticks(idx+0.4,label)
plt.grid(axis='x')
plt.xlabel('XX事件次数')
plt.ylabel('XX事件名称')
plt.title('2015.1-2016.11月XX事件排行榜')
plt.savefig(path + "111.png",format='png', dpi=200)  
plt.show()
plt.close()


book = xlsxwriter.Workbook(path + 'pict.xlsx')      # 将图片插入到excel表格中 
sheet = book.add_worksheet('paint')
sheet.insert_image(2,0 , path + "123.png")
sheet.insert_image(23,0, path + "456.png")
sheet.insert_image(2,10, path + "890.png")
sheet.insert_image(23,10, path + "111.png")
book.close()

book = xlsxwriter.Workbook(path + 'pict2.xlsx')     # 将图片插入到excel表格中 
sheet = book.add_worksheet('paint')
sheet.insert_image('A2' , path + "123.png")
sheet.insert_image('A23', path + "456.png")
sheet.insert_image('L2', path + "890.png")
sheet.insert_image('L23', path + "111.png")
book.close()

