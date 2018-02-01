# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 15:23:27 2018

@author: Administrator
"""

import pandas as pd   #导入pandas库
from math import radians, cos, sin, asin, sqrt 

A=r'd:\test\A.xls'
B=r'd:\test\B.xls'
jieguo=r'd:\test\result.xls'
juli_max=3000  #设置匹配范围，小于3000米

def open_xls(x):
    df_xls=pd.read_excel(x,encoding='utf-8',dtype='str') #导入发电费用
    return df_xls

def write_xls(x,sheet):
    writer = pd.ExcelWriter(jieguo) #输出到excel
    x.to_excel(writer, '%s'%sheet)
    writer.save()
    return None

def calc_juli(lon1, lat1, lon2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数） 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])     # 将十进制度数转化为弧度 
    dlon = lon2 - lon1      #计算距离的公式
    dlat = lat2 - lat1   
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2  
    c = 2 * asin(sqrt(a))   
    r = 6371*1000   #地球平均半径，单位为米
    return c * r 

df_A=open_xls(A)
df_B=open_xls(B)
df_A[['longitude','latitude']]=df_A[['longitude','latitude']].astype(float) 
df_B[['LON','LAT']]=df_B[['LON','LAT']].astype(float) #将B表的经纬度列转换为浮点数，以便进行数学运算

df_jieguo=pd.DataFrame(columns=['RRU中文名','eNBId','计算距离','匹配基站','匹配基站编码'])
df_jieguo['RRU中文名']=df_A['RRU中文名']
df_jieguo['eNBId']=df_A['eNBId']
juli_tmp=juli_max 	#设定tmp距离变量的初始值
B_name='未匹配'	#设定匹配基站名称的初始值
B_code='未匹配'	#设定匹配基站编码的初始值
#for i in range(0,len(df_A),1):
for i in range(0,20,1):
    for j in range(0,len(df_B),1): 
        juli_calc=calc_juli(df_A.loc[i,'longitude'],df_A.loc[i,'latitude'],df_B.loc[j,'LON'],df_B.loc[j,'LAT']) 	#j每跳一次，计算距离
        if juli_calc<juli_tmp: 	#如果计算的距离小于我们预设的初始距离就执行下面的代码
            juli_tmp=juli_calc	#将计算的距离赋值给零时变流量：juli_tmp
            B_name=df_B.loc[j,'CELLNAME']
            B_code=df_B.loc[j,'CELLID_B']
    df_jieguo.loc[i,'计算距离']=juli_tmp	#到这里完成了B表的一轮遍历，找到了与A表最近的一个站点，返回最小距离juli_tmp
    df_jieguo.loc[i,'匹配基站']= B_name		#返回最近的站点的name
    df_jieguo.loc[i,'匹配基站编码']=B_code	#返回最近的站点的基站代码
    juli_tmp=juli_max   #将零时变量juli_tmp置为初始值juli_max
    B_name='未匹配' 	#将零时变量B_name置为初始值'未匹配' 
    B_code='未匹配'
   
write_xls(df_jieguo,'匹配结果')