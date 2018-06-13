# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 21:44:00 2018
划小周报
@author: Administrator
"""
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import xlsxwriter
from datetime import datetime

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

# =============================================================================
# 环境变量
# =============================================================================
data_path = r'd:\_话务量划小报表' + '\\'
zte_data_path = r'd:\_话务量划小报表\zte' + '\\'
eric_data_path = r'd:\_话务量划小报表\eric' + '\\'
traffic_path_3g = r'd:\_话务量划小报表\3g话务量' + '\\'
user_path_1x = r'd:\_话务量划小报表\3g登记' + '\\'

out_path = r'd:\_话务量划小报表' + '\\'
pic_path = r'd:\_话务量划小报表\pic' + '\\'
eNode_name = 'eNode_name.xls'

zte_files = os.listdir(zte_data_path) 
eric_files = os.listdir(eric_data_path) 
traffic_file_3g = os.listdir(traffic_path_3g) 
user_file_1x = os.listdir(user_path_1x) 

df_eric_titles  = pd.read_excel(out_path + 'title.xlsx',encoding = 'utf-8')
titles = list(df_eric_titles.columns)

df_eNodeB = pd.read_excel(out_path + eNode_name,encoding = 'utf-8')
country_list = list(set(df_eNodeB['区县']))
list_tmp =[]
for i in range(0,len(country_list),1):
    list_tmp.append((country_list[i],i))
    
msc_file =  os.listdir(data_path + 'MSC登记' + '\\')
df_msc = pd.read_excel(data_path + 'MSC登记' + '\\' + msc_file[0], skiprows = 1,encoding = 'utf-8')
df_msc = df_msc[['时间','漫游用户数']]
df_msc['时间'] = df_msc['时间'].map(lambda x:x.split(' ')[0])                                     
df_msc['时间'] =  df_msc['时间'].map(lambda x:x.replace('-','/'))
df_msc['时间'] =  df_msc['时间'].map(lambda x:x.replace('/0','/'))
df_msc = df_msc.rename(columns={'时间':'日期'})
df_msc['日期'] =  df_msc['日期'].map(lambda x:x[5:])


country_dict = dict(list_tmp)

df_list = list(range(0,9))

df_combine = pd.DataFrame()

# 汇总3G话务量
df_3g_traffic = pd.DataFrame()
for file in traffic_file_3g:    
    df_tmp = pd.read_csv(traffic_path_3g + file,engine = 'python', encoding = 'gbk')
    df_tmp.columns = df_tmp.columns.map(lambda x:x.strip())
    df_tmp['DO: 小区RLP信息对象.前向MacIndex最大忙数'] = df_tmp['DO: 小区RLP信息对象.前向MacIndex最大忙数'].replace('-',0)
    df_tmp['DO: 小区RLP信息对象.RLP层前向传送字节数(KB)'] =  df_tmp['DO: 小区RLP信息对象.RLP层前向传送字节数(KB)'].replace('-',0)
    df_tmp['DO: 小区RLP信息对象.前向MacIndex最大忙数'] = df_tmp['DO: 小区RLP信息对象.前向MacIndex最大忙数'].map(lambda x:int(x))
    df_tmp['DO: 小区RLP信息对象.RLP层前向传送字节数(KB)'] =  df_tmp['DO: 小区RLP信息对象.RLP层前向传送字节数(KB)'].map(lambda x:int(x))    
    df_tmp['开始时间'] =  df_tmp['开始时间'].map(lambda x:x.replace('-','/')) 
    df_tmp['开始时间'] =  df_tmp['开始时间'].map(lambda x:x.replace('/0','/'))  
    date_list = list(set(df_tmp['开始时间'].map(lambda x:x.split(' ')[0])))
    # =============================================================================
    # 计算每日实际忙时确定RRC连接用户数
    # =============================================================================
    for date in date_list:
        df_date = df_tmp[df_tmp['开始时间'].str.contains(date)]
        # =============================================================================
        # 计算每日总流量
        # =============================================================================
        df_pivot_traffic  = pd.pivot_table(df_date, index=['BTS'],
                                          values = ['DO: 小区RLP信息对象.RLP层前向传送字节数(KB)',
                                                    '1X: 小区CS呼叫话务量(Erl)'],
                                          aggfunc = {'DO: 小区RLP信息对象.RLP层前向传送字节数(KB)':np.sum,
                                                     '1X: 小区CS呼叫话务量(Erl)':np.sum})
        df_pivot_traffic = df_pivot_traffic.reset_index()
        df_pivot_traffic.rename(columns={'DO: 小区RLP信息对象.RLP层前向传送字节数(KB)':'3G流量',                                 
                                          '1X: 小区CS呼叫话务量(Erl)':'语音话务量'},inplace =True)
                                        
        df_pivot_rrc = pd.pivot_table(df_date, index=['开始时间'],
                                      values ='DO: 小区RLP信息对象.前向MacIndex最大忙数',
                                      aggfunc = {'DO: 小区RLP信息对象.前向MacIndex最大忙数':np.sum})                                                  
        df_pivot_rrc = df_pivot_rrc.sort_values(by='DO: 小区RLP信息对象.前向MacIndex最大忙数',ascending = False)
        df_pivot_rrc = df_pivot_rrc.reset_index()
        busy_hour =  df_pivot_rrc.loc[0,'开始时间']
        df_max_rrc =  df_date[['BTS','DO: 小区RLP信息对象.前向MacIndex最大忙数']][df_tmp['开始时间'] == busy_hour] 
        df_max_rrc.rename(columns={'DO: 小区RLP信息对象.前向MacIndex最大忙数':'3G联网用户数'},inplace =True)                                

        df_pivot_traffic = pd.merge(df_pivot_traffic,df_max_rrc,how = 'left', on ='BTS')
        df_pivot_traffic['日期'] = date
        df_3g_traffic = df_3g_traffic.append(df_pivot_traffic)
        df_3g_traffic['日期'] = pd.to_datetime(df_3g_traffic['日期'])
        df_3g_traffic = df_3g_traffic.sort_values(by='日期',ascending = True)
        df_3g_traffic['日期'] =  df_3g_traffic['日期'].map(lambda x:str(x))
        df_3g_traffic['日期'] =  df_3g_traffic['日期'].map(lambda x:x.split(' ')[0])

# 汇总1X登记用户数
df_1x_user = pd.DataFrame()        
for file in user_file_1x: 
    df_tmp = pd.read_csv(user_path_1x + file,engine = 'python', encoding = 'gbk')
    df_tmp.columns = df_tmp.columns.map(lambda x:x.strip())
    date_list = list(set(df_tmp['开始时间'].map(lambda x:x.split(' ')[0])))
    # =============================================================================
    # 计算每日实际忙时确定RRC连接用户数
    # =============================================================================
    for date in date_list:
        df_date = df_tmp[df_tmp['开始时间'].str.contains(date)]
        # =============================================================================
        # 计算每日总流量
        # =============================================================================
        df_pivot_user = pd.pivot_table(df_date, index=['开始时间'],
                                      values ='1X: Sector基本性能测量对象.定时登记成功次数',
                                      aggfunc = {'1X: Sector基本性能测量对象.定时登记成功次数':np.sum})                                                  
        df_pivot_user = df_pivot_user.sort_values(by='1X: Sector基本性能测量对象.定时登记成功次数',ascending = False)
        df_pivot_user = df_pivot_user.reset_index()
        busy_hour =  df_pivot_user.loc[0,'开始时间']
        df_max_user =  df_date[['BTS','1X: Sector基本性能测量对象.定时登记成功次数']][df_date['开始时间'] == busy_hour]        
        df_max_user['日期'] = date
        df_1x_user = df_1x_user.append(df_max_user)  
        df_1x_user['日期'] =  df_1x_user['日期'].map(lambda x:x.replace('-','/'))
        df_1x_user['日期'] =  df_1x_user['日期'].map(lambda x:x.replace('/0','/'))
df_1x_user = df_1x_user.rename(columns={'1X: Sector基本性能测量对象.定时登记成功次数':'1X用户数','BTS':'网元'})
df_1x_user =  pd.merge(df_1x_user,df_eNodeB,on = '网元',how = 'left')  

# 汇总中兴数据
for file in zte_files:  
    df_tmp = pd.read_csv(zte_data_path + file,skiprows = 5,engine = 'python', encoding = 'gbk')
    df_tmp['空口上行用户面流量（MByte）_1'] = df_tmp['空口上行用户面流量（MByte）_1'].map(lambda x:float(x.replace(',','')))
    df_tmp['空口下行用户面流量（MByte）_1477070755617-11'] = df_tmp['空口下行用户面流量（MByte）_1477070755617-11'].map(lambda x:float(x.replace(',','')))
    date = df_tmp.loc[0,'开始时间'].split(' ')[0]
    
    # =============================================================================
    # 计算每日实际忙时确定RRC连接用户数
    # =============================================================================
    df_pivot_rrc = pd.pivot_table(df_tmp, index=['开始时间'], values = '最大RRC连接用户数_1', aggfunc = {'最大RRC连接用户数_1':np.sum})                                                  
    df_pivot_rrc = df_pivot_rrc.sort_values(by='最大RRC连接用户数_1',ascending = False)
    df_pivot_rrc = df_pivot_rrc.reset_index()
    busy_hour =  df_pivot_rrc.loc[0,'开始时间']
    df_max_rrc =  df_tmp[['网元','最大RRC连接用户数_1']][df_tmp['开始时间'] == busy_hour]
    
    # =============================================================================
    # 计算每日总流量
    # =============================================================================
    df_pivot = pd.pivot_table(df_tmp, index=['网元'],
                              values = [ '空口上行用户面流量（MByte）_1',
                                        '空口下行用户面流量（MByte）_1477070755617-11'],
                              aggfunc = {'空口上行用户面流量（MByte）_1':np.sum,
                                         '空口下行用户面流量（MByte）_1477070755617-11':np.sum})
    df_pivot['总流量'] = df_pivot['空口上行用户面流量（MByte）_1'] + df_pivot['空口下行用户面流量（MByte）_1477070755617-11']
    df_pivot = df_pivot.reset_index()
    df_pivot = pd.merge(df_pivot,df_max_rrc,on = '网元',how = 'left')  
    df_pivot['日期'] = date.replace('-','/')
    df_pivot.rename(columns={'最大RRC连接用户数_1':'RRC连接用户数',
                             '空口上行用户面流量（MByte）_1':'上行流量(MB)',
                             '空口下行用户面流量（MByte）_1477070755617-11':'下行流量(MB)'},inplace =True)
    df_combine = df_combine.append(df_pivot)  

# 汇总爱立信数据
for file in eric_files:    
    df_tmp = pd.read_csv(eric_data_path + file,header = None,names = titles, engine = 'python', encoding = 'gbk')
    df_tmp['DATE_ID'] = df_tmp['DATE_ID'].map(lambda x:x.replace('\'',''))
    df_tmp['eNodeB'] = df_tmp['eNodeB'].map(lambda x:x.replace('\'',''))
    date = df_tmp.loc[0,'DATE_ID']
    
    # =============================================================================
    # 计算每日实际忙时确定RRC连接用户数
    # =============================================================================
    df_pivot_rrc = pd.pivot_table(df_tmp, index=['HOUR_ID'], values = 'Max number of UE in RRc', aggfunc = {'Max number of UE in RRc':np.sum})                                                  
    df_pivot_rrc = df_pivot_rrc.sort_values(by='Max number of UE in RRc',ascending = False)
    df_pivot_rrc = df_pivot_rrc.reset_index()
    busy_hour =  df_pivot_rrc.loc[0,'HOUR_ID']
    df_max_rrc =  df_tmp[['eNodeB','Max number of UE in RRc']][df_tmp['HOUR_ID'] == busy_hour]
    
    df_pivot = pd.pivot_table(df_tmp, index=['eNodeB'],
                              values = ['Air Interface_Traffic_Volume_UL_MBytes',
                                        'Air Interface_Traffic_Volume_DL_MBytes'], 
                              aggfunc = {'Air Interface_Traffic_Volume_UL_MBytes':np.sum,
                                         'Air Interface_Traffic_Volume_DL_MBytes':np.sum})  
    df_pivot['总流量'] = df_pivot['Air Interface_Traffic_Volume_UL_MBytes'] + df_pivot['Air Interface_Traffic_Volume_DL_MBytes']
    df_pivot = df_pivot.reset_index()
    df_pivot = pd.merge(df_pivot,df_max_rrc,on = 'eNodeB',how = 'left')  
    df_pivot['日期'] = date.replace('-','/')
    df_pivot.rename(columns={'eNodeB':'网元',
                             'Max number of UE in RRc' : 'RRC连接用户数',
                             'Air Interface_Traffic_Volume_UL_MBytes':'上行流量(MB)',
                             'Air Interface_Traffic_Volume_DL_MBytes':'下行流量(MB)'},inplace =True)
    df_combine = df_combine.append(df_pivot)  

df_combine['网元'] = df_combine['网元'].map(lambda x:int(x))
df_combine = pd.merge(df_combine,df_eNodeB,how='left',on = '网元')
df_combine['RRC连接用户数'] = df_combine['RRC连接用户数'].map(lambda x:round(x,0))
df_combine = df_combine.fillna(0)

# =============================================================================
# 全市用户数和流量
# =============================================================================
df_all = pd.pivot_table(df_combine, index=['日期'],values=['RRC连接用户数','总流量'],
                         aggfunc = {'RRC连接用户数':np.sum,'总流量':np.sum})  
df_all = df_all.rename(columns={'RRC连接用户数':'联网用户数'})
df_all['总流量'] =  df_all['总流量'].map(lambda x:round(float(x/(1024*1024)),1))
df_all = df_all.reset_index()
df_all['日期'] =  df_all['日期'].map(lambda x:x.replace('/0','/'))
df_all['日期'] =  df_all['日期'].map(lambda x:x[5:])

df_all_1x = pd.pivot_table(df_1x_user, index=['日期'],values='1X用户数',
                           aggfunc = {'1X用户数':np.sum})  
df_all_1x['1X用户数'] = df_all_1x['1X用户数'].map(lambda x:round(x/2,0))
df_all_1x = df_all_1x.reset_index()
Ddf_all_1x['日期'] = pd.to_datetime(df_all_1x['日期'])
df_all_1x = df_all_1x.sort_values(by='日期',ascending = True)
df_all_1x['日期'] = df_all_1x['日期'].map(lambda x:str(x))
df_all_1x['日期'] =  df_all_1x['日期'].map(lambda x:x.split(' ')[0])        
df_all_1x['日期'] =  df_all_1x['日期'].map(lambda x:x.replace('-','/'))
df_all_1x['日期'] =  df_all_1x['日期'].map(lambda x:x.replace('/0','/'))
df_all_1x['日期'] =  df_all_1x['日期'].map(lambda x:x[5:])
df_all_1x =  pd.merge(df_all_1x,df_msc,how='left',on = '日期')
df_all_1x['本地用户数'] =  df_all_1x['1X用户数'] - df_all_1x['漫游用户数']

df_4g_ratio = pd.DataFrame()      
df_4g_ratio['日期'] =  df_all_1x['日期']
df_4g_ratio['1x用户数'] =  df_all_1x['1X用户数']
df_4g_ratio['4G用户数'] =  df_all['联网用户数']
df_4g_ratio['4G渗透率'] =  df_4g_ratio['4G用户数']/df_4g_ratio['1x用户数']*100

                              
df_all_3g = pd.pivot_table(df_3g_traffic, index=['日期'],values='3G流量',aggfunc = {'3G流量':np.sum})  
df_all_3g = df_all_3g.reset_index()
df_all_3g['3G流量'] =  df_all_3g['3G流量'].map(lambda x:round(float(x/(1024*1024*1024)),1))
df_all_3g['日期'] =  df_all_3g['日期'].map(lambda x:x.replace('-','/'))
df_all_3g['日期'] =  df_all_3g['日期'].map(lambda x:x.replace('/0','/'))
df_all_3g['日期'] =  df_all_3g['日期'].map(lambda x:x[5:])

y1 = df_all['联网用户数'].T.values
x1 = df_all['日期'].T.values
plt.figure(figsize=(14, 4))
plt.xticks(range(len(x1)), x1,fontsize=8)
plt.plot(range(len(x1)),y1,label='4G联网用户数',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=6) 
for a,b in zip(range(len(x1)),y1):
    plt.text(a,b*1.001, '%d' % b, ha='center', va= 'bottom',fontsize=10)
plt.xlabel('日期')
plt.ylabel('4G联网用户数')
plt.title('4G日联网用户数变化情况')
plt.legend(loc='center right')
plt.savefig(pic_path + "全市4G用户数.png",format='png', dpi=400)  
plt.close()

y2 = df_all_1x['本地用户数'].T.values
x2 = df_all_1x['日期'].T.values
plt.figure(figsize=(14, 4))
plt.xticks(range(len(x2)), x2,fontsize=8)
plt.plot(range(len(x2)),y2,label='1X用户数',linewidth=3,color='b',marker='o',markerfacecolor='yellow',markersize=6)
for a,b in zip(range(len(x2)),y2):
    plt.text(a,b*1.001, '%d' % b, ha='center', va= 'bottom',fontsize=10)
plt.xlabel('日期')
plt.ylabel('1X用户数')
plt.title('1X注册用户数变化情况')
plt.legend(loc='center right')
plt.savefig(pic_path + "全市1X用户数.png",format='png', dpi=400)  
plt.close()

y5 = list(df_4g_ratio['4G渗透率'])
x5 = list(df_4g_ratio['日期'])
plt.figure(figsize=(14, 4))
plt.xticks(range(len(x5)), x5,fontsize=8)
plt.plot(range(len(x5)),y5,label='4G渗透率',linewidth=3,color='b',marker='o',markerfacecolor='yellow',markersize=6) 
for a,b in zip(range(len(x5)),y5):
    plt.text(a, b*1.001, '%.2f%%' % b, ha='center', va= 'bottom',fontsize=10)
plt.xlabel('日期')
plt.ylabel('4G渗透率(%)')
plt.legend(loc='center right')
plt.title('4G渗透率')
plt.savefig(pic_path + "4G渗透率.png",format='png', dpi=400) 
plt.close()


y3 = list(df_all['总流量'])
x3 = list(df_all['日期'])
plt.figure(figsize=(14, 4))
plt.xticks(range(len(x3)), x3,fontsize=8)
plt.plot(range(len(x3)),y3,label='4G总流量',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=6) 
for a,b in zip(range(len(x3)),y3):
    plt.text(a, b*1.001, '%.1f' % b, ha='center', va= 'bottom',fontsize=10)
plt.xlabel('日期')
plt.ylabel('4G总流量(TB)')
plt.legend(loc='center right')
plt.title('4G日总流量变化情况')
plt.savefig(pic_path + "全市4G总流量.png",format='png', dpi=400) 
plt.close()

y4 = list(df_all_3g['3G流量'])
x4 = list(df_all_3g['日期'])
plt.figure(figsize=(14, 4))
plt.xticks(range(len(x4)), x4,fontsize=8)
plt.plot(range(len(x4)),y4,label='3G总流量',linewidth=3,color='b',marker='o',markerfacecolor='yellow',markersize=6) 
for a,b in zip(range(len(x4)),y4):
    plt.text(a, b*1.001, '%.1f' % b, ha='center', va= 'bottom',fontsize=10)
plt.xlabel('日期')
plt.ylabel('3G总流量(TB)')
plt.legend(loc='center right')
plt.title('3G日总流量变化情况')
plt.savefig(pic_path + "全市3G总流量.png",format='png', dpi=400) 
plt.close()

#按区县和日期透视
df_city = pd.pivot_table(df_combine, index=['区县','日期'],values=['RRC连接用户数','总流量'],
                         aggfunc = {'RRC连接用户数':np.sum,'总流量':np.sum})                                
df_city = df_city.reset_index()
yestoday_new_user = []
total_new_user = []
total_user = []
for country in country_list:
    df_country = df_city[df_city['区县'] == country]
    yestoday_new_user.append(df_country.iloc[-1 , 2] - df_country.iloc[-2 , 2])
    total_new_user.append(df_country.iloc[-1 , 2] - df_country.iloc[0 , 2])
    total_user.append(df_country.iloc[-1 , 2])

df_city_1x = pd.pivot_table(df_1x_user, index=['区县','日期'],values='1X用户数',
                         aggfunc = {'1X用户数':np.sum})                                
df_city_1x = df_city_1x.reset_index()
yestoday_new_1x = []
total_new_1x = []
total_user_1x = []
for country in country_list:
    df_country_1x = df_city_1x[df_city_1x['区县'] == country]
    yestoday_new_1x.append(df_country_1x.iloc[-1 , 2] - df_country_1x.iloc[-2 , 2])
    total_new_1x.append(df_country_1x.iloc[-1 , 2] - df_country_1x.iloc[0 , 2])
    total_user_1x.append(df_country_1x.iloc[-1 , 2])

#计算出漫游用户占比，从而计算本地用户数
roaming_rate = df_all_1x.iloc[-1,2]/df_all_1x.iloc[-1,1]

yestoday_new_1x = [round((x/2*(1-roaming_rate)),0) for x in yestoday_new_1x]
total_new_1x = [round((x/2*(1-roaming_rate)),0) for x in total_new_1x]
total_user_1x = [round((x/2*(1-roaming_rate)),0) for x in total_user_1x]


plt.figure(figsize=(6, 4))
x_country = range(0,len(country_list)) 
x_country1 = [i+0.3 for i in x_country] 
plt.bar(x_country,yestoday_new_user,color='g',width = 0.3,alpha=0.6,label='昨日新增4G用户数')
plt.bar(x_country1,yestoday_new_1x,color='b',width = 0.3,alpha=0.6,label='昨日新增1X用户数')
for x,y in zip(x_country,yestoday_new_user):
    plt.text(x, y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=12)
for x,y in zip(x_country1,yestoday_new_1x):
    plt.text(x, y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=12)
plt.xlabel('昨日新增用户数')
plt.xticks(range(0,len(country_list)),country_list)
plt.ylabel('区县')
plt.legend(loc='upper middle')
plt.title('各县昨日新增用户数')
plt.savefig(pic_path + "各县昨日新增用户数.png",format='png', dpi=200)  
plt.close()

plt.figure(figsize=(6, 4))
x_country = range(0,len(country_list)) 
x_country1 = [i+0.3 for i in x_country] 
plt.bar(x_country,total_new_user,color='g',width = 0.3,alpha=0.6,label='4G累计新增用户数')
plt.bar(x_country1,total_new_1x,color='b',width = 0.3,alpha=0.6,label='3G累计新增用户数')
for x,y in zip(x_country,total_new_user):
    plt.text(x,y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=12)
for x,y in zip(x_country1,total_new_1x):
    plt.text(x,y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=12)
plt.xlabel('累计新增用户数')
plt.xticks(range(0,len(country_list)),country_list)
plt.ylabel('区县')
plt.legend(loc='upper middle')
plt.title('各县累计新增用户数')
plt.savefig(pic_path + "各县累计新增用户数.png",format='png', dpi=200)  
plt.close()

plt.figure(figsize=(6, 4))
x_country = range(0,len(country_list)) 
x_country1 = [i+0.3 for i in x_country] 
plt.bar(x_country,total_user,color='g',width = 0.3,alpha=0.6,label='4G到达用户数')
plt.bar(x_country1,total_user_1x,color='b',width = 0.3,alpha=0.6,label='3G到达用户数')
for x,y in zip(x_country,total_user):
    plt.text(x, y+10, '%d' % y, ha='center', va= 'bottom',fontsize=12)
for x,y in zip(x_country1,total_user_1x):
    plt.text(x, y+10, '%d' % y, ha='center', va= 'bottom',fontsize=12)
plt.xlabel('到达用户数')
plt.xticks(range(0,len(country_list)),country_list)
plt.ylabel('区县')
plt.title('各县到达用户数')
plt.savefig(pic_path + "各县到达用户数.png",format='png', dpi=200)  
plt.close()

country_4G_ratio = [a/b for a,b in zip(total_user,total_user_1x)]

# =============================================================================
# 生成各区县数据
# =============================================================================                           
for i in range(0,len(country_list),1):
    df_list[i] = df_combine[df_combine['区县'] == country_list[i]] 

for df_country in df_list:
    df_country = df_country.reset_index() 
    country_name = df_country.loc[0,'区县']
    df_country_pivot = df_country.groupby(by = '日期',as_index=False)[['RRC连接用户数','总流量']].sum()
    df_country_pivot['总流量'] = df_country_pivot['总流量'].map(lambda x:round(float(x/(1024*1024)),1))
    df_country_pivot['日期'] = df_country_pivot['日期'].map(lambda x:x[5:10])
    # =============================================================================
    # 画各县联网用户数图   
    # =============================================================================
    x = list(df_country_pivot['日期'])
    y = df_country_pivot['RRC连接用户数'].T.values
    plt.figure(figsize=(14, 4))
    plt.plot(x,y,label='4G联网用户数',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=8) 
    for a,b in zip(x,y):
        plt.text(a, b*1.001, '%d' % b, ha='center', va= 'bottom',fontsize=12)
    plt.xlabel('日期')
    plt.ylabel(country_name + '4G联网用户数')
    plt.title(country_name + '4G联网用户数')
    plt.savefig(pic_path + country_name + "4G联网用户数.png",format='png', dpi=200) 
    plt.close()                                   
    # =============================================================================
    # 画各县流量
    # =============================================================================
    x = list(df_country_pivot['日期'])
    y = df_country_pivot['总流量'].T.values
    plt.figure(figsize=(14, 4))
    plt.plot(x,y,label='4G总流量(TB)',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=8) 
    for a,b in zip(x,y):
        plt.text(a, b*1.001, '%.1f' % b, ha='center', va= 'bottom',fontsize=12)
    plt.xlabel('日期')
    plt.ylabel(country_name + '4G总流量(TB)')
    plt.title(country_name + '4G总流量(TB)')
    plt.savefig(pic_path + country_name + "4G总流量.png",format='png', dpi=200)  
    plt.close()
    # =============================================================================
    # 按支局透视 
    # =============================================================================
    substation_list = list(set(df_country['支局']))
    df_substation_pivot = pd.pivot_table(df_country, index=['支局','日期'],values=['RRC连接用户数','总流量'],
                                         aggfunc = {'RRC连接用户数':np.sum,'总流量':np.sum}) 
    df_substation_pivot = df_substation_pivot.reset_index()
    # =============================================================================
    # 画各支局用户数增长图  
    # =============================================================================  
    substation_new_user = []
    substation_total_add_user = []
    substation_total_user = []
    for substation in substation_list:
        df_substation = df_substation_pivot[df_substation_pivot['支局'] == substation]
        substation_new_user.append(df_substation.iloc[-1,2]-df_substation.iloc[-2,2]) 
        substation_total_add_user.append(df_substation.iloc[-1,2]-df_substation.iloc[0,2]) 
        substation_total_user.append(df_substation.iloc[-1,2])
     
    plt.figure(figsize=(6,4))
    plt.bar(substation_list,substation_new_user,color='g',width = 0.3,alpha=0.6,label='昨日新增用户数')
    for x,y in zip(substation_list,substation_new_user):
        plt.text(x, y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=12)
    plt.xlabel('支局')
    plt.ylabel('昨日新增用户数')
    plt.title(country_name + '各支局昨日新增用户数')
    plt.savefig(pic_path + country_name + "各支局昨日新增用户数.png",format='png', dpi=200)  
    plt.close()
    
    plt.figure(figsize=(6,4))
    plt.bar(substation_list,substation_total_add_user,color='g',width = 0.3,alpha=0.6,label='累计新增用户数')
    for x,y in zip(substation_list,substation_total_add_user):
        plt.text(x, y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=12)
    plt.xlabel('支局')
    plt.ylabel('累计新增用户数')
    plt.title(country_name + '各支局累计新增用户数')
    plt.savefig(pic_path + country_name + "各支局累计新增用户数.png",format='png', dpi=200)  
    plt.close()
    
    plt.figure(figsize=(6,4))
    plt.bar(substation_list,substation_total_user,color='g',width = 0.3,alpha=0.6,label='到达用户数')
    for x,y in zip(substation_list,substation_total_user):
        plt.text(x, y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=12)
    plt.xlabel('支局')
    plt.ylabel('到达用户数')
    plt.title(country_name + '各支局到达用户数')
    plt.savefig(pic_path + country_name + "各支局到达用户数.png",format='png', dpi=200)  
    plt.close()

    # =============================================================================
    # 画各支局日用户数、日流量
    # =============================================================================
    for substation in substation_list:
        df_substation = df_substation_pivot[df_substation_pivot['支局'] == substation]
        df_substation['总流量'] =  df_substation['总流量'].map(lambda x:round(float(x/(1024*1024)),1))
        df_substation['日期'] = df_substation['日期'].map(lambda x:x[5:10])
        x = list(df_substation['日期'])
        y = df_substation['RRC连接用户数'].T.values
        plt.figure(figsize=(14, 4))
        plt.plot(x,y,label='联网用户数',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=8) 
        for a,b in zip(x,y):
            plt.text(a, b*1.001, '%d' % b, ha='center', va= 'bottom',fontsize=12)
        plt.xlabel('日期')
        plt.ylabel(substation +'支局_联网用户数')
        plt.title(country_name + '_' +substation +'支局_4G联网用户数')
        plt.savefig(pic_path + country_name + substation + '支局_4G联网用户数.png',format='png', dpi=200)  
        plt.close()                                   

        x = list(df_substation['日期'])
        y = df_substation['总流量'].T.values
        plt.figure(figsize=(14, 4))
        plt.plot(x,y,label='总流量(TB)',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=8) 
        for a,b in zip(x,y):
            plt.text(a, b*1.001, '%.1f' % b, ha='center', va= 'bottom',fontsize=12)
        plt.xlabel('日期')
        plt.ylabel(substation+ '支局_总流量(TB)')
        plt.title(country_name + '_' +substation+ '支局_4G总流量(TB)')
        plt.savefig(pic_path + country_name + substation + "支局_4G总流量.png",format='png', dpi=200)  
        plt.close()                                   
        
# =============================================================================
# 生成全市汇总表格
# =============================================================================
book = xlsxwriter.Workbook(out_path + '_全市各区县用户数及流量.xlsx')     # 将图片插入到excel表格中 
sheet = book.add_worksheet('全市用户数及流量')
sheet.insert_image('A2' , pic_path + "全市1X用户数.png")
sheet.insert_image('A23', pic_path + "全市4G用户数.png")
sheet.insert_image('A44', pic_path +  "4G渗透率.png")
sheet.insert_image('A65', pic_path +  "全市4G总流量.png")
sheet.insert_image('A86', pic_path +  "全市3G总流量.png")
sheet.insert_image('A107', pic_path + "各县昨日新增用户数.png")
sheet.insert_image('J107', pic_path + "各县累计新增用户数.png")
sheet.insert_image('A128', pic_path + "各县到达用户数.png")

for country in country_list:
    sheet = book.add_worksheet(country)
    sheet.insert_image('A2' , pic_path + country + "4G联网用户数.png")
    sheet.insert_image('A23', pic_path + country + "4G总流量.png")
    sheet.insert_image('A44', pic_path + country + "各支局昨日新增用户数.png")
    sheet.insert_image('J44', pic_path + country + "各支局累计新增用户数.png")
    sheet.insert_image('A65', pic_path + country + "各支局到达用户数.png")
book.close()

# =============================================================================
# 生成各县表格
# =============================================================================
for i in range(0,len(df_list),1):
    substation_list = list(set(df_list[i]['支局']))
    book = xlsxwriter.Workbook(out_path + country_list[i] + '各支局用户数及流量.xlsx')     # 将图片插入到excel表格中         
    for substation in substation_list:
        sheet = book.add_worksheet(substation)
        sheet.insert_image('A2' , pic_path +country_list[i]+ substation + '支局_4G联网用户数.png')
        sheet.insert_image('A23', pic_path + country_list[i]+ substation + "支局_4G总流量.png")
    book.close()

with  pd.ExcelWriter(out_path + '1x用户数.xlsx')  as writer:  #输出到excel
    df_1x_user.to_excel(writer,'1x用户数')

with  pd.ExcelWriter(out_path + '4G汇总.xlsx')  as writer:  #输出到excel
    df_combine.to_excel(writer,'4G汇总')