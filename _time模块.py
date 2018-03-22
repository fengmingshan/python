# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 15:56:36 2018

@author: Administrator
"""
import time

time.sleep(5)   #等待一定时间
for i in range(0,10,1):
    print(i)
    time.sleep(1)
    
#时间戳timestamp是一种时间表示形式
time.time()     #时间戳，从1970年1月1日至今，经过的秒数，
type(time.time())   #时间戳是float格式的小数

# 本地时间，细化到年、月、日、小时、分钟、秒等
print(time.localtime())
type(time.localtime())  #格式是time模块的标准格式struct_time格式

# 将本地时间转为时间戳形式：
time.mktime(time.localtime())

# 将时间表示形式转为asctime形式：
time.asctime(time.localtime()) #这里将得到一个空格分隔的字符串
type(time.asctime(time.localtime()))   #这里的格式是str
x=time.asctime(time.localtime()) 
y=x.split(' ',)     #将字符串以空格拆分，得到一个list

# 将时间戳转为asctime形式：
a = time.ctime(1519545859.0) 
b=a[-4:]
type(time.ctime(1519545859.0))


# 把一个元组或者struct_time转化为自定义格式的时间字符串
time.localtime()
time.strftime('%Y-%m-%d %X',time.localtime())   
type(time.strftime('%Y-%m-%d %X',time.localtime()))     # 转换后时间是string格式

#上面的操作也可以逆操作
time.strptime('2018-02-25 16:22:34','%Y-%m-%d %X')      # 将格式时间装换为struct_time格式
type(time.strptime('2018-02-25 16:22:34','%Y-%m-%d %X'))    # 可以看出格式变回了标准格式struct_time

# 将其它格式的时间字符串转为标准的时间字符串：
a='2017-02-25 16:17:13'
time_array=time.strptime(a,'%Y-%m-%d %H:%M:%S')     # 转换为标准格式struct_time
otherstyletime=time.strftime('%Y/%m/%d %H:%M:%S',time_array)    # 转换为其他格式
otherstyletime1=time.strftime('%Y/%m/%d %H/%M/%S',time_array)    # 转换为其他格式
otherstyletime2=time.strftime('%Y/%m/%d %H-%M-%S',time_array)    # 其他格式连接符可以自定义
otherstyletime3=time.strftime('%Y/%m/%d %H %M %S',time_array)    # 其他格式连接符可以自定义

b='20180308161313'
c=(int(b[0:4]),int(b[4:6]),int(b[6:8]),int(b[8:10]),int(b[10:12]),int(b[12:14]),5,50,1)
otherstyletime4=time.strftime('%Y/%m/%d %H:%M:%S',c)    # 转换为其他格式


# 总结
# time模块的时间格式有3种：标准格式struct_time，时间戳格式（float），自定义格式（str）
# time.strftime()可以把任意格式时间字符串转换成自定义格式的时间字符串str
# time.strptime()可以把任意自定义格式的时间字符串，转换成time模块的标准格式struct_time
time1 ='2018-03-19 20:07:02'
time2 ='2018-03-19 22:07:02'  
a = time.strptime(time1,'%Y-%m-%d %H:%M:%S') 
b = time.strptime(time2,'%Y-%m-%d %H:%M:%S') 
c=time.mktime(a)
d=time.mktime(b)

detal_time =(d-c)/60





# =============================================================================
# 函数取当前时间并转换成strftime
# =============================================================================
def get_current_time():
    month_trans = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'June':6,
              'July':7,'Aug':8,'Sept':9,'Oct':10,'Nov':11,'Dec':12} # 中英文月份对照字典
    time_str = time.ctime(time.time())
    time_tuple = tuple(time.localtime())
    year = int(time_str[-4:])
    month = month_trans[time_str.split(' ')[1]]  # 查月份翻译表得到数字的月份
    day = int(time_str.split(' ')[2])
    hour = int(time_str.split(' ')[3][0:2])
    minute = int(time_str.split(' ')[3][3:5])
    second = int(time_str.split(' ')[3][-2:])
    tm_wday = time_tuple[-3]    # 周几
    tm_yday = time_tuple[-2]    # 一年中的第几天
    tm_isdst = time_tuple[-1]    # 是否夏令时

    struct_time = (year,month,day,hour,minute,second,tm_wday,tm_yday,tm_isdst)
    current_time = time.strftime('%Y/%m/%d %H:%M:%S',struct_time) # 转换采集时间为正常时间格式
    return current_time







