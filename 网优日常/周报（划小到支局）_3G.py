# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 09:09:46 2018

@author: Administrator
"""

import pandas as pd
import numpy as np
import os
import xlsxwriter
import matplotlib.pyplot as plt
from datetime import datetime

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

path_3g = r'D:\_话务周报(划小到支局)\3G' + '\\'
path_3g_busy = r'D:\_话务周报(划小到支局)\3G忙时' + '\\'

data_path = r'D:\_话务周报(划小到支局)' + '\\'
out_path = r'D:\_话务周报(划小到支局)\报表输出' + '\\'
pic_path = r'D:\_话务周报(划小到支局)\pic' + '\\'

df_zte_eNodeB =  pd.read_excel(data_path + 'zte_eNode_name.xls',encoding = 'utf-8')

files_3G = os.listdir(path_3g) 
files_3G_busy = os.listdir(path_3g_busy) 


df_zte_3G_traffic = pd.DataFrame()
for file in files_3G:    
    df_tmp = pd.read_csv(path_3g + file,engine = 'python', encoding = 'gbk')
    df_tmp.fillna(0,inplace=True)
    df_tmp.columns = df_tmp.columns.map(lambda x:x.strip())
    df_tmp['开始时间'] = pd.to_datetime(df_tmp['开始时间'],format="%Y-%m-%d")  
    week = str(df_tmp.iloc[0,0]).split(' ')[0][5:10] + "_" + str(df_tmp.iloc[-1,0]).split(' ')[0][5:10]
    df_tmp['week'] = week
    df_zte_3G_traffic = df_zte_3G_traffic.append(df_tmp)

df_zte_3G_traffic['开始时间'] = pd.to_datetime(df_tmp['开始时间'],format="%Y-%m-%d")  
df_zte_3G_traffic.rename(columns={'DO: 小区RLP信息对象.前向MacIndex最大忙数':'3G用户数',
                                  'DO: 小区RLP信息对象.RLP层前向传送字节数(KB)':'3G流量(TB)',
                                  '1X: 小区CS呼叫话务量(Erl)':'1X话务量',
                                  'Cell':'网元'},inplace =True)
df_zte_3G_traffic['3G流量(TB)'] =  df_zte_3G_traffic['3G流量(TB)'].map(lambda x:x.replace('-','0'))
df_zte_3G_traffic['3G用户数'] =  df_zte_3G_traffic['3G用户数'].map(lambda x:x.replace('-','0'))
df_zte_3G_traffic['3G流量(TB)'] =  df_zte_3G_traffic['3G流量(TB)'].astype(float) 
df_zte_3G_traffic['3G用户数'] =  df_zte_3G_traffic['3G用户数'].astype(float) 
df_zte_3G_traffic['3G流量(TB)'] =  df_zte_3G_traffic['3G流量(TB)']/(1024*1024*1024)
df_zte_3G_traffic['网元'] =  df_zte_3G_traffic['网元'].map(lambda x:x.split('_')[2])
df_zte_3G_traffic['网元'] =  df_zte_3G_traffic['网元'].map(lambda x:x.split('J')[1])

df_zte_3G_traffic =  df_zte_3G_traffic[['week','网元','1X话务量','3G流量(TB)','3G用户数']]
df_zte_3G_traffic = pd.pivot_table(df_zte_3G_traffic, index=['week','网元'], 
                                   values = ['1X话务量','3G流量(TB)','3G用户数'], 
                                   aggfunc = {'1X话务量':np.sum,'3G流量(TB)':np.sum,'3G用户数':np.max})  
df_zte_3G_traffic = df_zte_3G_traffic.reset_index()                                                     

df_zte_3G_traffic = pd.merge(df_zte_3G_traffic,df_zte_eNodeB,how ='left',on = '网元' )  
df_zte_3G_traffic['week-区县'] = df_zte_3G_traffic['week'] + '-' + df_zte_3G_traffic['区县']

df_zte_3G_user = pd.DataFrame()
for file in files_3G_busy:    
    df_tmp = pd.read_csv(path_3g_busy + file,engine = 'python', encoding = 'gbk')
    df_tmp.fillna(0,inplace=True)
    df_tmp.columns = df_tmp.columns.map(lambda x:x.strip())
    df_tmp['开始时间'] = pd.to_datetime(df_tmp['开始时间'],format="%Y-%m-%d")  
    df_tmp.rename(columns={'1X: Sector基本性能测量对象.定时登记成功次数':'1X用户数',
                           'Cell':'网元'},inplace =True)
    df_tmp['网元'] =  df_tmp['网元'].map(lambda x:x.split('_')[2])
    df_tmp['网元'] =  df_tmp['网元'].map(lambda x:x.split('J')[1])
    df_tmp['1X用户数'] =  df_tmp['1X用户数']/2
    week = str(df_tmp.iloc[0,0]).split(' ')[0][5:10] + "_" + str(df_tmp.iloc[-1,0]).split(' ')[0][5:10]
    df_tmp['week'] = week
    # =============================================================================
    # 计算每日实际忙时确定RRC连接用户数
    # =============================================================================
    df_pivot_1Xuser = pd.pivot_table(df_tmp, index=['开始时间'], values = '1X用户数', aggfunc = {'1X用户数':np.sum})                                                  
    df_pivot_1Xuser = df_pivot_1Xuser.sort_values(by='1X用户数',ascending = False)
    df_pivot_1Xuser = df_pivot_1Xuser.reset_index()
    busy_hour =  df_pivot_1Xuser.loc[0,'开始时间']
    df_max_user =  df_tmp[['开始时间','week','网元','1X用户数']][df_tmp['开始时间'] == busy_hour]    
    df_max_user =  df_max_user[['week','网元','1X用户数']]
    df_zte_3G_user = df_zte_3G_user.append(df_max_user)
df_zte_3G_user = pd.merge(df_zte_3G_user,df_zte_eNodeB,how ='left',on = '网元' )     

# =============================================================================
# 各县基站总数
# =============================================================================
df_3G_country =  pd.pivot_table(df_zte_3G_traffic, index=['week','区县'], values = '网元', aggfunc = {'网元':len}) 
df_3G_country = df_3G_country.reset_index()
df_3G_country.rename(columns={'网元':'基站数量'},inplace =True)               
df_3G_country['week-区县'] = df_3G_country['week'] + '-' + df_3G_country['区县']

# =============================================================================
# 各县零流量基站数量
# =============================================================================
df_zero_traffic = df_zte_3G_traffic[df_zte_3G_traffic['1X话务量']==0]
df_zero_traffic =  pd.pivot_table(df_zero_traffic,
                                  index=['week','区县'], 
                                  values = '网元', aggfunc = {'网元':len})
df_zero_traffic.rename(columns={'网元':'零流量基站数量'},inplace =True)               
df_zero_traffic =  df_zero_traffic.reset_index()
df_zero_traffic['week-区县'] = df_zero_traffic['week'] + '-' + df_zero_traffic['区县']
df_zero_traffic = df_zero_traffic[['week-区县','零流量基站数量']] 

# =============================================================================
# 1X用户数
# =============================================================================
df_1X_uesr =  pd.pivot_table(df_zte_3G_user,
                              index=['week','区县'],
                              values = '1X用户数', aggfunc = {'1X用户数':sum})                  
df_1X_uesr =  df_1X_uesr.reset_index()
df_1X_uesr['week-区县'] = df_1X_uesr['week'] + '-' + df_1X_uesr['区县']
df_1X_uesr = df_1X_uesr[['week-区县','1X用户数']] 

# =============================================================================
# 3G用户数
# =============================================================================
df_3G_uesr =  pd.pivot_table(df_zte_3G_traffic,
                              index=['week','区县'],
                              values = '3G用户数', aggfunc = {'3G用户数':sum})                  
df_3G_uesr =  df_3G_uesr.reset_index()
df_3G_uesr['week-区县'] = df_3G_uesr['week'] + '-' + df_3G_uesr['区县']
df_3G_uesr = df_3G_uesr[['week-区县','3G用户数']] 


# =============================================================================
# 1X话务量和3G流量
# =============================================================================
df_3G_country_traffic =  pd.pivot_table(df_zte_3G_traffic,
                                index=['week','区县'],
                                values = ['1X话务量','3G流量(TB)'], 
                                aggfunc = {'1X话务量':sum,'3G流量(TB)':sum})                  
df_3G_country_traffic =  df_3G_country_traffic.reset_index()
df_3G_country_traffic['week-区县'] = df_3G_country_traffic['week'] + '-' + df_3G_country_traffic['区县']
df_3G_country_traffic = df_3G_country_traffic[['week-区县','1X话务量','3G流量(TB)']] 

df_3G_country = pd.merge(df_3G_country,df_zero_traffic,how ='left',on = 'week-区县' )    
df_3G_country = pd.merge(df_3G_country,df_1X_uesr,how ='left',on = 'week-区县' ) 
df_3G_country = pd.merge(df_3G_country,df_3G_uesr,how ='left',on = 'week-区县' )       
df_3G_country = pd.merge(df_3G_country,df_3G_country_traffic,how ='left',on = 'week-区县' )    
df_3G_country.fillna(0,inplace =True)

week1 = df_3G_country.iloc[0,0]
week2 = df_3G_country.iloc[-1,0]
# =============================================================================
# 画基站数量图
# =============================================================================
y1 = df_3G_country['基站数量'][df_3G_country['week'] == week1 ].T.values
y2 = df_3G_country['基站数量'][df_3G_country['week'] == week2 ].T.values
country_list = df_3G_country['区县'][df_3G_country['week'] == week1 ].T.values
plt.figure(figsize=(6, 4))
x_country = range(0,len(country_list)) 
x_country1 = [i+0.35 for i in x_country] 
plt.bar(x_country,y1,color='g',width = 0.3,alpha=0.6,label='上周基站数量')
plt.bar(x_country1,y2,color='b',width = 0.3,alpha=0.6,label='本周基站数量')
for x,y in zip(x_country,y1):
    plt.text(x, y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=8)
for x,y in zip(x_country1,y2 ):
    plt.text(x, y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=8)
plt.xlabel('各县3G基站数量')
plt.xticks(range(0,len(country_list)),country_list)
plt.ylabel('区县')
plt.legend(loc='upper middle')
plt.title('各县3G基站数量')
plt.savefig(pic_path + "各县3G基站数量.png",format='png', dpi=200)  
plt.close()

# =============================================================================
# 画各县3G零话务基站数量图
# =============================================================================
y1 = df_3G_country['零流量基站数量'][df_3G_country['week'] == week1 ].T.values
y2 = df_3G_country['零流量基站数量'][df_3G_country['week'] == week2 ].T.values
plt.figure(figsize=(6, 4))
x_country = range(0,len(country_list)) 
x_country1 = [i+0.35 for i in x_country] 
plt.bar(x_country,y1,color='g',width = 0.3,alpha=0.6,label='上周3G零流量基站')
plt.bar(x_country1,y2,color='b',width = 0.3,alpha=0.6,label='本周3G零流量基站')
for x,y in zip(x_country,y1):
    plt.text(x, y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=8)
for x,y in zip(x_country1,y2 ):
    plt.text(x, y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=8)
plt.xlabel('各县3G零流量基站数量')
plt.xticks(range(0,len(country_list)),country_list)
plt.ylabel('区县')
plt.legend(loc='upper middle')
plt.title('各县3G零流量基站数量')
plt.savefig(pic_path + "各县3G零流量基站数量.png",format='png', dpi=200)  
plt.close()

# =============================================================================
# 画1X用户数
# =============================================================================
y1 = df_3G_country['1X用户数'][df_3G_country['week'] == week1 ].T.values
y2 = df_3G_country['1X用户数'][df_3G_country['week'] == week2 ].T.values
plt.figure(figsize=(6, 4))
x_country = range(0,len(country_list)) 
x_country1 = [i+0.35 for i in x_country] 
plt.bar(x_country,y1,color='g',width = 0.3,alpha=0.6,label='上周1X用户数')
plt.bar(x_country1,y2,color='b',width = 0.3,alpha=0.6,label='本周1X用户数')
for x,y in zip(x_country,y1):
    plt.text(x, y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=6)
for x,y in zip(x_country1,y2 ):
    plt.text(x, y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=6)
plt.xlabel('各县1X用户数')
plt.xticks(range(0,len(country_list)),country_list)
plt.ylabel('区县')
plt.legend(loc='upper middle')
plt.title('各县1X用户数')
plt.savefig(pic_path + "各县1X用户数.png",format='png', dpi=200)  
plt.close()

# =============================================================================
# 画3G用户数
# =============================================================================
y1 = df_3G_country['3G用户数'][df_3G_country['week'] == week1 ].T.values
y2 = df_3G_country['3G用户数'][df_3G_country['week'] == week2 ].T.values
plt.figure(figsize=(6, 4))
x_country = range(0,len(country_list)) 
x_country1 = [i+0.35 for i in x_country] 
plt.bar(x_country,y1,color='g',width = 0.3,alpha=0.6,label='上周3G用户数')
plt.bar(x_country1,y2,color='b',width = 0.3,alpha=0.6,label='本周3G用户数')
for x,y in zip(x_country,y1):
    plt.text(x, y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=6)
for x,y in zip(x_country1,y2 ):
    plt.text(x, y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=6)
plt.xlabel('各县3G用户数')
plt.xticks(range(0,len(country_list)),country_list)
plt.ylabel('区县')
plt.legend(loc='upper middle')
plt.title('各县3G用户数')
plt.savefig(pic_path + "各县3G用户数.png",format='png', dpi=200)  
plt.close()

# =============================================================================
# 1X用户数环比变化率
# =============================================================================
y1 = df_3G_country['1X用户数'][df_3G_country['week'] == week1 ].T.values
y2 = df_3G_country['1X用户数'][df_3G_country['week'] == week2 ].T.values
y3 =  [(b-a)/a for a, b in zip(y1,y2)]
country_list = df_3G_country['区县'][df_3G_country['week'] == week1 ].T.values
plt.figure(figsize=(6, 4))
x_country = range(0,len(country_list)) 
plt.bar(x_country,y3,color='b',width = 0.3,alpha=0.6,label='各县1X用户数环比')
for x,y in zip(x_country,y3):
    plt.text(x, y*1.001, '%.2f%%' % (y*100), ha='center', va= 'bottom',fontsize=12)
plt.xlabel('各县1X用户数环比')
plt.xticks(range(0,len(country_list)),country_list)
plt.ylabel('区县')
plt.legend(loc='upper middle')
plt.title('各县1X用户数环比')
plt.savefig(pic_path + "各县1X用户数环比.png",format='png', dpi=200)  
plt.close()

# =============================================================================
# 3G用户数环比变化率
# =============================================================================
y1 = df_3G_country['3G用户数'][df_3G_country['week'] == week1 ].T.values
y2 = df_3G_country['3G用户数'][df_3G_country['week'] == week2 ].T.values
y3 =  [(b-a)/a for a, b in zip(y1,y2)]
country_list = df_3G_country['区县'][df_3G_country['week'] == week1 ].T.values
plt.figure(figsize=(6, 4))
x_country = range(0,len(country_list)) 
plt.bar(x_country,y3,color='b',width = 0.3,alpha=0.6,label='各县3G用户数环比')
for x,y in zip(x_country,y3):
    plt.text(x, y*1.001, '%.2f%%' % (y*100), ha='center', va= 'bottom',fontsize=12)
plt.xlabel('各县3G用户数环比')
plt.xticks(range(0,len(country_list)),country_list)
plt.ylabel('区县')
plt.legend(loc='upper middle')
plt.title('各县3G用户数环比')
plt.savefig(pic_path + "各县3G用户数环比.png",format='png', dpi=200)  
plt.close()

# =============================================================================
# 画1X话务量
# =============================================================================
y1 = df_3G_country['1X话务量'][df_3G_country['week'] == week1 ].T.values
y2 = df_3G_country['1X话务量'][df_3G_country['week'] == week2 ].T.values
plt.figure(figsize=(6, 4))
x_country = range(0,len(country_list)) 
x_country1 = [i+0.35 for i in x_country] 
plt.bar(x_country,y1,color='g',width = 0.3,alpha=0.6,label='上周1X话务量')
plt.bar(x_country1,y2,color='b',width = 0.3,alpha=0.6,label='本周1X话务量')
for x,y in zip(x_country,y1):
    plt.text(x, y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=6)
for x,y in zip(x_country1,y2 ):
    plt.text(x, y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=6)
plt.xlabel('各县1X话务量')
plt.xticks(range(0,len(country_list)),country_list)
plt.ylabel('区县')
plt.legend(loc='upper middle')
plt.title('各县1X话务量')
plt.savefig(pic_path + "各县1X话务量.png",format='png', dpi=200)  
plt.close()

# =============================================================================
# 1X话务量环比变化率
# =============================================================================
y1 = df_3G_country['1X话务量'][df_3G_country['week'] == week1 ].T.values
y2 = df_3G_country['1X话务量'][df_3G_country['week'] == week2 ].T.values
y3 =  [(b-a)/a for a, b in zip(y1,y2)]
country_list = df_3G_country['区县'][df_3G_country['week'] == week1 ].T.values
plt.figure(figsize=(6, 4))
x_country = range(0,len(country_list)) 
plt.bar(x_country,y3,color='b',width = 0.3,alpha=0.6,label='各县1X话务量环比')
for x,y in zip(x_country,y3):
    plt.text(x, y*1.001, '%.2f%%' % (y*100), ha='center', va= 'bottom',fontsize=12)
plt.xlabel('各县1X话务量环比')
plt.xticks(range(0,len(country_list)),country_list)
plt.ylabel('区县')
plt.legend(loc='upper middle')
plt.title('各县1X话务量环比')
plt.savefig(pic_path + "各县1X话务量环比.png",format='png', dpi=200)  
plt.close()

# =============================================================================
# 画3G流量
# =============================================================================
y1 = df_3G_country['3G流量(TB)'][df_3G_country['week'] == week1 ].T.values
y2 = df_3G_country['3G流量(TB)'][df_3G_country['week'] == week2 ].T.values
plt.figure(figsize=(6, 4))
x_country = range(0,len(country_list)) 
x_country1 = [i+0.35 for i in x_country] 
plt.bar(x_country,y1,color='g',width = 0.3,alpha=0.6,label='上周3G流量')
plt.bar(x_country1,y2,color='b',width = 0.3,alpha=0.6,label='本周3G流量')
for x,y in zip(x_country,y1):
    plt.text(x, y*1.001, '%2.2f' % y, ha='center', va= 'bottom',fontsize=6)
for x,y in zip(x_country1,y2 ):
    plt.text(x, y*1.001, '%2.2f' % y, ha='center', va= 'bottom',fontsize=6)
plt.xlabel('各县3G流量(TB)')
plt.xticks(range(0,len(country_list)),country_list)
plt.ylabel('区县')
plt.legend(loc='upper middle')
plt.title('各县3G流量(TB)')
plt.savefig(pic_path + "各县3G流量.png",format='png', dpi=200)  
plt.close()

# =============================================================================
# 3G流量环比变化率
# =============================================================================
y1 = df_3G_country['3G流量(TB)'][df_3G_country['week'] == week1 ].T.values
y2 = df_3G_country['3G流量(TB)'][df_3G_country['week'] == week2 ].T.values
y3 =  [(b-a)/a for a, b in zip(y1,y2)]
country_list = df_3G_country['区县'][df_3G_country['week'] == week1 ].T.values
plt.figure(figsize=(6, 4))
x_country = range(0,len(country_list)) 
plt.bar(x_country,y3,color='b',width = 0.3,alpha=0.6,label='各县3G流量环比')
for x,y in zip(x_country,y3):
    plt.text(x, y*1.001, '%.2f%%' % (y*100), ha='center', va= 'bottom',fontsize=12)
plt.xlabel('各县3G流量环比')
plt.xticks(range(0,len(country_list)),country_list)
plt.ylabel('区县')
plt.legend(loc='upper middle')
plt.title('各县3G流量环比')
plt.savefig(pic_path + "各县3G流量环比.png",format='png', dpi=200)  
plt.close()


#with  pd.ExcelWriter(out_path + 'df_zte_3G.xlsx')  as writer:  #输出到excel
    #df_zte_3G_traffic.to_excel(writer, 'df_zte_3G_traffic') 
    #df_zte_3G_user.to_excel(writer, 'df_zte_3G_user')     
