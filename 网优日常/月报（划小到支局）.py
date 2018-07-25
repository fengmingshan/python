# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 10:22:59 2018

@author: Administrator
"""
import pandas as pd
import numpy as np
import os
import xlsxwriter
from datetime import datetime

data_path = r'd:\_月报（划小到支局）' + '\\'
eric_data_path = r'd:\_月报（划小到支局）\爱立信话务' + '\\'
zte_data_path = r'd:\_月报（划小到支局）\中兴话务' + '\\'
zte3g_data_path =  r'd:\_月报（划小到支局）\3G话务' + '\\'


eric_busy_data = r'd:\_月报（划小到支局）\爱立信忙时' + '\\'
zte_busy_data = r'd:\_月报（划小到支局）\中兴忙时' + '\\'
zte3g_user_path =  r'd:\_月报（划小到支局）\3G登记' + '\\'


out_path = r'd:\_月报（划小到支局）' + '\\'
eric_eNodeB = '爱立信关联支局.xlsx'
zte_eNodeB = 'eNode_name.xls'


eric_files = os.listdir(eric_data_path) 
zte_files = os.listdir(zte_data_path) 
zte3g_file = os.listdir(zte3g_data_path) 

eric_busy_files =  os.listdir(eric_busy_data) 
zte_busy_files =  os.listdir(zte_busy_data) 
zte3g_user_file =  os.listdir(zte3g_user_path) 

df_eric_eNodeB = pd.read_excel(data_path + eric_eNodeB,encoding = 'utf-8')
df_zte_eNodeB = pd.read_excel(data_path + zte_eNodeB,encoding = 'utf-8')


df_titles  = pd.read_excel(data_path + 'title.xlsx',encoding = 'utf-8')
df_busy_titles  = pd.read_excel(data_path + 'busy_title.xlsx',encoding = 'utf-8')

titles = list(df_titles.columns)
busy_titles = list(df_busy_titles.columns)

df_4G_traffic = pd.DataFrame() #用来汇总4G话务量
for file in eric_files:    
    df_tmp = pd.read_csv(eric_data_path + file,header = None,names = titles, engine = 'python', encoding = 'gbk')
    df_tmp['DATE_ID'] = df_tmp['DATE_ID'].map(lambda x:x.replace('\'',''))
    df_tmp['DATE_ID'] = df_tmp['DATE_ID'].map(lambda x:x[0:7])
    df_tmp['eNodeB'] = df_tmp['eNodeB'].map(lambda x:x.replace('\'',''))
    df_pivot = pd.pivot_table(df_tmp, index=['DATE_ID','eNodeB'],
                              values = ['Air Interface_Traffic_Volume_UL_MBytes',
                                        'Air Interface_Traffic_Volume_DL_MBytes'],                                                                         
                              aggfunc = {'Air Interface_Traffic_Volume_UL_MBytes':np.sum,
                                         'Air Interface_Traffic_Volume_DL_MBytes':np.sum })                                                                               
    df_pivot['总流量'] = df_pivot['Air Interface_Traffic_Volume_UL_MBytes'] + df_pivot['Air Interface_Traffic_Volume_DL_MBytes']
    df_pivot = df_pivot.reset_index()
    df_pivot.rename(columns={'DATE_ID':'月份',
                             'eNodeB':'网元',
                             'Air Interface_Traffic_Volume_UL_MBytes':'上行流量(MB)',
                             'Air Interface_Traffic_Volume_DL_MBytes':'下行流量(MB)'},inplace =True)
    df_pivot['网元'] = df_pivot['网元'].astype(int)
    df_pivot = pd.merge(df_pivot,df_eric_eNodeB,on = '网元',how = 'left')  
    df_4G_traffic = df_4G_traffic.append(df_pivot) 


for file in zte_files:    
    df_tmp = pd.read_csv(zte_data_path + file,skiprows = 5,engine = 'python', encoding = 'gbk')
    df_tmp['空口上行用户面流量（MByte）_1'] = df_tmp['空口上行用户面流量（MByte）_1'].map(lambda x:float(x.replace(',','')))
    df_tmp['空口下行用户面流量（MByte）_1477070755617-11'] = df_tmp['空口下行用户面流量（MByte）_1477070755617-11'].map(lambda x:float(x.replace(',','')))
    df_tmp['开始时间'] = df_tmp['开始时间'].map(lambda x:x[0:7])
    df_pivot = pd.pivot_table(df_tmp, index=['开始时间','网元'],
                              values = [ '空口下行用户面流量（MByte）_1477070755617-11',
                                        '空口上行用户面流量（MByte）_1'],                                        
                              aggfunc = {'空口下行用户面流量（MByte）_1477070755617-11':np.sum,
                                         '空口上行用户面流量（MByte）_1':np.sum})
    df_pivot['总流量'] = df_pivot['空口上行用户面流量（MByte）_1'] + df_pivot['空口下行用户面流量（MByte）_1477070755617-11']
    df_pivot = df_pivot.reset_index()
    df_pivot.rename(columns={'开始时间':'月份',
                             '空口下行用户面流量（MByte）_1477070755617-11':'下行流量(MB)',
                             '空口上行用户面流量（MByte）_1':'上行流量(MB)',
                             },inplace =True)
    df_pivot = df_pivot[['月份','网元','下行流量(MB)','上行流量(MB)','总流量']]
    df_pivot = pd.merge(df_pivot,df_zte_eNodeB,on = '网元',how = 'left')  
    df_4G_traffic = df_4G_traffic.append(df_pivot) #用来汇总4G话务量

df_3G_traffic = pd.DataFrame() #用来汇总4G话务量

for file in zte3g_file:    
    df_tmp = pd.read_csv(zte3g_data_path + file,engine = 'python', encoding = 'gbk')
    df_tmp['开始时间'] = pd.to_datetime(df_tmp['开始时间'],format="%Y/%m/%d")
    df_tmp['开始时间'] = df_tmp['开始时间'].astype(str)
    df_tmp['开始时间'] = df_tmp['开始时间'].map(lambda x:x[0:7])
    columns = list(x.strip() for x in df_tmp.columns)
    df_tmp.columns = columns
    df_tmp['DO: 小区RLP信息对象.RLP层前向传送字节数(KB)'] = df_tmp['DO: 小区RLP信息对象.RLP层前向传送字节数(KB)'].replace('-',0)
    df_tmp['DO: 小区RLP信息对象.RLP层前向传送字节数(KB)'] = df_tmp['DO: 小区RLP信息对象.RLP层前向传送字节数(KB)'].astype(int)
    df_tmp['DO: 小区RLP信息对象.RLP层前向传送字节数(KB)'] = df_tmp['DO: 小区RLP信息对象.RLP层前向传送字节数(KB)']/(1024*1024)
    df_tmp['DO: 小区RLP信息对象.RLP层前向传送字节数(KB)'] = df_tmp['DO: 小区RLP信息对象.RLP层前向传送字节数(KB)'].map(lambda x:round(x,1))
    df_pivot = pd.pivot_table(df_tmp, index=['开始时间','BTS'],
                              values = [ '1X: 小区CS呼叫话务量(Erl)',
                                        'DO: 小区RLP信息对象.RLP层前向传送字节数(KB)'],                                        
                              aggfunc = {'1X: 小区CS呼叫话务量(Erl)':np.sum,
                                         'DO: 小区RLP信息对象.RLP层前向传送字节数(KB)':np.sum})
    df_pivot = df_pivot.reset_index()
    df_pivot.rename(columns={'开始时间':'月份',
                             'BTS': '网元',
                             '1X: 小区CS呼叫话务量(Erl)':'话务量',
                             'DO: 小区RLP信息对象.RLP层前向传送字节数(KB)':'3G流量(GB)',
                             },inplace =True)
    df_pivot = pd.merge(df_pivot,df_zte_eNodeB,on = '网元',how = 'left')  
    df_3G_traffic = df_3G_traffic.append(df_pivot) #用来汇总3G话务量


df_4G_user = pd.DataFrame() #用来汇总4G话务量

for file in eric_busy_files:    
    df_tmp = pd.read_csv(eric_busy_data + file,header = None,names = busy_titles, engine = 'python', encoding = 'gbk')
    df_tmp['DATE_ID'] = df_tmp['DATE_ID'].map(lambda x:x.replace('\'',''))
    df_tmp['DATE_ID'] = df_tmp['DATE_ID'].map(lambda x:x[0:7])
    df_tmp['eNodeB'] = df_tmp['eNodeB'].map(lambda x:x.replace('\'',''))
    df_pivot = pd.pivot_table(df_tmp, index=['DATE_ID','eNodeB'],
                              values = ['Max number of UE in RRc'],   
                              aggfunc = {'Max number of UE in RRc':np.max })   
    df_pivot = df_pivot.reset_index()
    df_pivot.rename(columns={'DATE_ID':'月份',
                             'eNodeB':'网元',
                             'Max number of UE in RRc' : 'RRC连接用户数',},inplace =True)
    df_pivot['网元'] = df_pivot['网元'].astype(int)
    df_4G_user = df_4G_user.append(df_pivot) 

for file in zte_busy_files:    
    df_tmp = pd.read_csv(zte_busy_data + file,skiprows = 5,engine = 'python', encoding = 'gbk')
    df_tmp['空口上行用户面流量（MByte）_1'] = df_tmp['空口上行用户面流量（MByte）_1'].map(lambda x:float(x.replace(',','')))
    df_tmp['空口下行用户面流量（MByte）_1477070755617-11'] = df_tmp['空口下行用户面流量（MByte）_1477070755617-11'].map(lambda x:float(x.replace(',','')))
    df_tmp['开始时间'] = df_tmp['开始时间'].map(lambda x:x[0:7])
    df_pivot = pd.pivot_table(df_tmp, index=['开始时间','网元'],
                              values = [ '最大RRC连接用户数_1'],                                        
                              aggfunc = {'最大RRC连接用户数_1':np.max})
    df_pivot = df_pivot.reset_index()
    df_pivot.rename(columns={'开始时间':'月份',
                             '最大RRC连接用户数_1':'RRC连接用户数'},inplace =True)
    df_4G_user = df_4G_user.append(df_pivot) #用来汇总4G话务量

df_3G_user = pd.DataFrame() #用来汇总3G用户数

for file in zte3g_user_file:    
    df_tmp = pd.read_csv(zte3g_user_path + file,engine = 'python', encoding = 'gbk')
    df_tmp['开始时间'] = pd.to_datetime(df_tmp['开始时间'],format="%Y/%m/%d")
    df_tmp['开始时间'] = df_tmp['开始时间'].astype(str)
    df_tmp['开始时间'] = df_tmp['开始时间'].map(lambda x:x.split(' ')[0][0:7])
    columns = list(x.strip() for x in df_tmp.columns)
    df_tmp.columns = columns
    df_pivot = pd.pivot_table(df_tmp, index=['开始时间','BTS'],
                              values = [ '1X: Sector基本性能测量对象.定时登记成功次数'],                                        
                              aggfunc = {'1X: Sector基本性能测量对象.定时登记成功次数':np.max})
    df_pivot = df_pivot.reset_index()
    df_pivot.rename(columns={'开始时间':'月份',
                             'BTS': '网元',
                             '1X: Sector基本性能测量对象.定时登记成功次数':'1X用户数',
                             },inplace =True)
    df_pivot['1X用户数'] = df_pivot['1X用户数']/2
    df_pivot['1X用户数'] = df_pivot['1X用户数'].map(lambda x:round(x,0))
    df_3G_user = df_3G_user.append(df_pivot) #用来汇总3G话务量
    
df_4G_traffic['month_网元'] = df_4G_traffic['月份'].map(str) + '_' + df_4G_traffic['网元'].map(str)
df_4G_user['month_网元'] = df_4G_user['月份'].map(str) + '_' +df_4G_user['网元'].map(str)
del df_4G_user['月份']
del df_4G_user['网元']
df_4G_ALL = pd.merge(df_4G_traffic , df_4G_user , on='month_网元',how = 'left')
df_4G_ALL['总流量'] = df_4G_ALL['总流量']/1024
df_4G_ALL['总流量'] = df_4G_ALL['总流量'].map(lambda x:round(x,1))
df_4G_ALL.rename(columns={'总流量':'总流量(GB)'},inplace =True)

df_3G_traffic['month_网元'] = df_3G_traffic['月份'].map(str) + '_' + df_3G_traffic['网元'].map(str)
df_3G_user['month_网元'] = df_3G_user['月份'].map(str) + '_' +df_3G_user['网元'].map(str)
del df_3G_user['月份']
del df_3G_user['网元']
df_3G_ALL = pd.merge(df_3G_traffic , df_3G_user , on='month_网元',how = 'left')


country_list = list(set(df_4G_ALL['区县']))
with  pd.ExcelWriter(out_path + '4G话务量.xlsx')  as writer:  #输出到excel
    for country in country_list :
        df_country = df_4G_ALL[df_4G_ALL['区县'] == country]
        df_country_pivot = pd.pivot_table(df_country, index=['月份','支局'],
                                      values = [ '总流量(GB)','RRC连接用户数'],                                        
                                      aggfunc = {'总流量(GB)':np.sum,
                                                 'RRC连接用户数':np.sum})
        df_country_pivot = df_country_pivot.reset_index()
        df_country_pivot.to_excel(writer,country) 

country_list = list(set(df_3G_ALL['区县']))
with  pd.ExcelWriter(out_path + '3G话务量.xlsx')  as writer:  #输出到excel
    for country in country_list :
        df_country = df_3G_ALL[df_3G_ALL['区县'] == country]
        df_country_pivot = pd.pivot_table(df_country, index=['月份','支局'],
                                      values = ['话务量','1X用户数','3G流量(GB)',],                                        
                                      aggfunc = {'话务量':np.sum,
                                                 '1X用户数':np.sum,
                                                 '3G流量(GB)':np.sum})
        df_country_pivot = df_country_pivot.reset_index()
        df_country_pivot.to_excel(writer,country) 


for country in country_list :
    df_country = df_4G_ALL[df_4G_ALL['区县'] == country]
    df_country_3G = df_3G_ALL[df_3G_ALL['区县'] == country]
    substation_list = list(set(df_country['支局']))
    with  pd.ExcelWriter(out_path +country + '.xlsx')  as writer:  #输出到excel
        for substation in substation_list :
            df_substation = df_country[(df_country['支局'] == substation)&(df_country['月份'] == '2018-06')]
            df_substation_3G = df_country_3G[(df_country_3G['支局'] == substation)&(df_country_3G['月份'] == '2018-06')]

            df_substation = df_substation.sort_values(by='总流量(GB)',ascending = True)
            df_substation = df_substation.reset_index()
            df_traffic_top = df_substation.loc[0:9,['网元名称', '厂家','总流量(GB)']]
            df_traffic_top['TOP类型'] ='低流量基站'
            
            df_substation_3G = df_substation_3G.sort_values(by='话务量',ascending = True)
            df_substation_3G = df_substation_3G.reset_index()
            df_traffic_top_3G = df_substation_3G.loc[0:9,['网元名称', '厂家','话务量']]
            df_traffic_top_3G['TOP类型'] ='低话务基站'
            
            df_substation = df_substation.sort_values(by='RRC连接用户数',ascending = True)
            df_substation_3G = df_substation_3G.sort_values(by='1X用户数',ascending = True)
            
            df_substation = df_substation.reset_index()
            df_user_top = df_substation.loc[0:9,['网元名称', '厂家','RRC连接用户数']]
            df_user_top['TOP类型'] = '低4G用户数基站'
            
            df_substation_3G = df_substation_3G.reset_index()
            df_user_top_3G = df_substation_3G.loc[0:9,['网元名称', '厂家','1X用户数']]
            df_user_top_3G['TOP类型'] = '低1X用户数基站'

            
            df_merge = pd.concat([df_traffic_top,df_user_top,df_traffic_top_3G,df_user_top_3G],axis=1)
            df_merge.to_excel(writer, substation) 


with  pd.ExcelWriter(out_path + '3G.xlsx')  as writer:  #输出到excel
    df_3G_ALL.to_excel(writer, '3G') 


with  pd.ExcelWriter(out_path + '4G.xlsx')  as writer:  #输出到excel
    df_4G_ALL.to_excel(writer, '4G') 