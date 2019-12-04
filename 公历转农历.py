# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 21:56:43 2019

@author: Administrator
"""

# pip install ZhDate
from zhdate import ZhDate
from datetime import datetime
import pandas as pd
import os


date_path = 'D:/Test'
os.chdir(date_path)

df = pd.read_csv('Chicago_Crimes_2012_to_2017.csv',engine ='python')
df.columns
df['old_Date'] = pd.to_datetime(df['Date'])
df['old_Date'][0:5]

date1 = ZhDate(2010, 1, 1) # 新建农历 2010年正月初一 的日期对象
print(date1)  # 直接返回农历日期字符串
dt_date1 = date1.to_datetime() # 农历转换成阳历日期 datetime 类型

dt_date2 = datetime(2010, 2, 6)
date2 = ZhDate.from_datetime(dt_date2) # 从阳历日期转换成农历日期对象

date3 = ZhDate(2020, 4, 30, leap_month=True) # 新建农历 2020年闰4月30日
print(date3.to_datetime())

# 支持比较
if ZhDate(2019, 1, 1) == ZhDate.from_datetime(datetime(2019, 2, 5)):
    pass

# 减法支持
new_zhdate = ZhDate(2019, 1, 1) - 30  #减整数，得到差额天数的新农历对象
new_zhdate2 = ZhDate(2019, 1, 1) - ZhDate(2018, 1, 1) #两个zhdate对象相减得到两个农历日期的差额
new_zhdate3 = ZhDate(2019, 1, 1) - datetime(2019, 1, 1) # 减去阳历日期，得到农历日期和阳历日期之间的天数差额

# 加法支持
new_zhdate4 = ZhDate(2019, 1, 1) + 30 # 加整数返回相隔天数以后的新农历对象

# 中文输出
new_zhdate5 = ZhDate(2019, 1, 1)
print(new_zhdate5.chinese())

# 当天的农历日期
ZhDate.today()
