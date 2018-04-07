# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 20:19:12 2018
datetime模块
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

# timestamp
t=time.time()
datetime.fromtimestamp(t)  
print(datetime.fromtimestamp(t)) # print出来的效果就是普通的时间格式：2018-03-25 20:34:42.996884

datetime.utcfromtimestamp(t)  # 格林威治标准时间-UTC时间
print(datetime.utcfromtimestamp(t))

# str 转时间
cday = datetime.strptime('2015-6-1 18:19:59', '%Y-%m-%d %H:%M:%S')
print(cday)

# 时间转 str
now = datetime.now()
print(now.strftime('%a, %b %d %H:%M'))

# datetime的加减
from datetime import timedelta

now = datetime.now()

now + timedelta(hours=10)

now - timedelta(days=1)

now + timedelta(days=2, hours=12)

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

