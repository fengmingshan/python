# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 15:23:27 2018

@author: Administrator
"""

import pandas as pd   #导入pandas库
from math import radians, cos, sin, asin, sqrt 

data_path =  r'd:\test' + '\\'
L1800 = 'L1800.xlsx'
L800 = 'L800.xlsx'
result = 'result.xlsx'
juli_max = 500  #设置匹配范围，小于500米


def calc_juli(lon1, lat1, lon2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数） 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])     # 将十进制度数转化为弧度 
    dlon = lon2 - lon1      #计算距离的公式
    dlat = lat2 - lat1   
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2  
    c = 2 * asin(sqrt(a))   
    r = 6371*1000   #地球平均半径，单位为米
    return c * r 

df_A = pd.read_excel(data_path + L1800,encoding='utf-8') #导入发电费用
df_B = pd.read_excel(data_path + L800,encoding='utf-8') 
df_A[['LON','LAT']]=df_A[['LON','LAT']].astype(float) 
df_B[['LON','LAT']]=df_B[['LON','LAT']].astype(float)  #将经纬度列转换为浮点数，以便进行数学运算

df_jieguo=pd.DataFrame(columns=['CELLNAME','CELLID','计算距离','匹配CELLNAME','匹配CELLID'])
df_jieguo['CELLNAME']=df_A['CELLNAME']
df_jieguo['CELLID']=df_A['CELLID']
juli_tmp=juli_max 	#设定tmp距离变量的初始值
tmp_name='未匹配'	#设定匹配基站名称的初始值
tmp_code='未匹配'	#设定匹配基站编码的初始值
for i in range(0,len(df_A),1):
    for j in range(0,len(df_B),1): 
        juli_calc=calc_juli(df_A.loc[i,'LON'],df_A.loc[i,'LAT'],df_B.loc[j,'LON'],df_B.loc[j,'LAT']) 	#j每跳一次，计算距离
        if juli_calc<juli_tmp: 	#如果计算的距离小于我们预设的初始距离就执行下面的代码
            juli_tmp=juli_calc	#将计算的距离赋值给零时变流量：juli_tmp
            tmp_name=df_B.loc[j,'CELLNAME']
            tmp_code=df_B.loc[j,'CELLID']
    df_jieguo.loc[i,'计算距离']=juli_tmp	#到这里完成了B表的一轮遍历，找到了与A表最近的一个站点，返回最小距离juli_tmp
    df_jieguo.loc[i,'匹配CELLNAME']= tmp_name		#返回最近的站点的name
    df_jieguo.loc[i,'匹配CELLID']=tmp_code	#返回最近的站点的基站代码
    juli_tmp= juli_max   #将零时变量juli_tmp置为初始值juli_max
    tmp_name='未匹配' 	#将零时变量B_name置为初始值'未匹配' 
    tmp_code='未匹配'

with pd.ExcelWriter(data_path + 'L1800与L800匹配.xlsx') as writer:   
    df_jieguo.to_excel(writer,'匹配结果')