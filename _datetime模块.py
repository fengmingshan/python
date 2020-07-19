# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 20:19:12 2018

@author: Administrator
"""
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import time


# 获取当前时间
now = datetime.now()    # 获取当前时间
today = datetime.today()    # 获取今天时间
dt = datetime(1980, 10, 31, 12, 30)  # 指定一个时间
dt_stamp = dt.timestamp() # 将时间装换成timestamp


# dateTime转换为date，但date不能直接转换为dateTime
dateTime_p = datetime.now()
date_p = dateTime_p.date()
print(dateTime_p) #2019-01-30 15:17:46.573139
print(date_p) #2019-01-30


# 日期类型datetime转换为字符串str
today1 = str(datetime.today().date())
print(today1) # '2020-07-04'
today2 = datetime.today().strftime("%Y-%m-%d")
print(today2) # '2020-01-21'
today3 = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
print(today3) # '2020-01-21 23:40:38'


# 字符串类型str转换为dateTime类型
str_p = '2019-01-30 15:29:08'
dateTime_p = datetime.strptime(str_p,'%Y-%m-%d %H:%M:%S')
print(dateTime_p) # 2019-01-30 15:29:08

str_p = '2020-07-05'
dateTime_p = datetime.strptime(str_p,'%Y-%m-%d')
print(dateTime_p) # 2019-01-30 15:29:08


# 字符串类型str转换为date类型
str_p = '2020-07-05'
date_p = datetime.strptime(str_p,'%Y-%m-%d').date()
print(date_p,type(date_p)) # 2019-01-30 <class 'datetime.date'>


# 日期转换成星期几
weekday = datetime.strptime('2020-07-18',"%Y-%m-%d").weekday()
weekday


# 日期转换成周数
s_date =
week = datetime.strptime('2020-07-18','%Y-%m-%d').date().isocalendar()[1]
week

# dateTime类型和date类型可以直接做加1减1操作
from datetime import timedelta

today = datetime.today().date()
yestoday = today + timedelta(days=-1)
tomorrow = today + timedelta(days=1)
print(today) # 2019-01-30
print(yestoday)# 2019-01-29
print(tomorrow)# 2019-01-31

now = datetime.now()
now + timedelta(hours=10)
now - timedelta(days=1)
now + timedelta(days=2, hours=12)


# timestamp
t=time.time()
datetime.fromtimestamp(t)
print(datetime.fromtimestamp(t)) # print出来的效果就是普通的时间格式：2018-03-25 20:34:42.996884

datetime.utcfromtimestamp(t)  # 格林威治标准时间-UTC时间
print(datetime.utcfromtimestamp(t))


# 计算时间差
t1 = '2015-04-06 23:30:03'
t2 = '2015-04-07 04:28:03'
time_interval = datetime.strptime(t2,"%Y-%m-%d %H:%M:%S") - datetime.strptime(t1,"%Y-%m-%d %H:%M:%S")
t3 = str(time_interval)
t4 = time_interval.seconds  # 表示为秒数
t5 = time_interval.days  # 表示为天数


# 时区转换
from datetime import timezone
from datetime import timedelta

tz_utc_8 = timezone(timedelta(hours=8))  # 创建时区UTC+8:00

now = datetime.now()

dt = now.replace(tzinfo=tz_utc_8) # # 强制设置为UTC+8:00

