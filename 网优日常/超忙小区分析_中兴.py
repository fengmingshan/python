# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 08:52:20 2019

@author: Administrator
"""
import pandas as pd
import os
import numpy as np

L1800_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,49, 50, 51, 52, 53, 54, 55, 56, 129, 130, 131, 132, 133, 134, 135, 136,177, 178, 179, 180, 181, 182]
L800_list = [17, 18, 19, 20, 21, 22,145, 146, 147, 148, 149,150]

data_path = r'D:\test' + '\\'

df_zte = pd.read_csv(data_path + '2019_07_22_16_48_37_531_yn_zxgs_中兴忙时话务_19625.csv' ,engine= 'python')

df_zte['空口上行用户面流量（MByte）_1'] = df_zte['空口上行用户面流量（MByte）_1'].map(lambda x:str(x).replace(',',''))
df_zte['空口下行用户面流量（MByte）_1477070755617-11'] = df_zte['空口下行用户面流量（MByte）_1477070755617-11'].map(lambda x:str(x).replace(',',''))
df_zte['下行PRB平均占用率_1'] = df_zte['下行PRB平均占用率_1'].map(lambda x:str(x).replace('%',''))

df_zte['空口上行用户面流量（MByte）_1'] = df_zte['空口上行用户面流量（MByte）_1'].astype(float)
df_zte['空口下行用户面流量（MByte）_1477070755617-11'] = df_zte['空口下行用户面流量（MByte）_1477070755617-11'].astype(float)
df_zte['下行PRB平均占用率_1'] = df_zte['下行PRB平均占用率_1'].astype(float)/100

df_zte['小区总流量(GB)'] = round(((df_zte['空口上行用户面流量（MByte）_1']
                         + df_zte['空口下行用户面流量（MByte）_1477070755617-11'])/1024),2)
df_zte['日期'] = df_zte['开始时间'].map(lambda x:str(x).split(' ')[0])
df_zte['周'] =pd.to_datetime(df_zte['日期'])
df_zte['周'] = df_zte['周'].map(lambda x:x.isocalendar()[1])

df_zte = df_zte[df_zte['小区名称'].str.contains('_')]
df_zte['Net_type'] = df_zte['小区名称'].map(lambda x:x.split('_')[1])
df_zte['Net_type'] = df_zte['Net_type'].astype(int)

df_zte_L1800 = df_zte[df_zte['Net_type'].isin(L1800_list)]

df_zte_L800 = df_zte[df_zte['Net_type'].isin(L800_list)]

df_high_Data_Volume = df_zte_L1800[(df_zte_L1800['小区总流量(GB)'] >= 6) & (df_zte_L1800['下行PRB平均占用率_1'] >= 0.5) ]
df_massive_users = df_zte_L1800[(df_zte_L1800['最大RRC连接用户数_1'] >= 200) & (df_zte_L1800['下行PRB平均占用率_1'] >= 0.5) ]

df_busy_cell_1800 = df_high_Data_Volume.append(df_massive_users)

df_res_1800 = pd.DataFrame()
for week in list(set(df_busy_cell_1800['周'])):
     df_1800 =  df_busy_cell_1800[df_busy_cell_1800['周'] == week]
     df_pivot_1800 = pd.pivot_table(df_1800, index=['周','日期','网元','小区','小区名称'],
                                                 values =['小区总流量(GB)' ,
                                                          '下行PRB平均占用率_1',
                                                          '最大RRC连接用户数_1'],
                                                 aggfunc = {'小区总流量(GB)':np.max,
                                                            '下行PRB平均占用率_1':np.max,
                                                            '最大RRC连接用户数_1':np.max})
     df_pivot_1800 = df_pivot_1800.reset_index()

     df_busy_cell_count_1800 = pd.pivot_table(df_pivot_1800, index=['周','网元','小区','小区名称'],
                                                      values =['日期'],
                                                      aggfunc = {'日期':'count'})
     df_busy_cell_count_1800  = df_busy_cell_count_1800.reset_index()


     df_high_Data_800 = df_zte_L800[(df_zte_L800['小区总流量(GB)'] >= 1.5) & (df_zte_L800['下行PRB平均占用率_1'] >= 0.5) ]
     df_massive_users_800 = df_zte_L800[(df_zte_L800['最大RRC连接用户数_1'] >= 50) & (df_zte_L800['下行PRB平均占用率_1'] >= 0.5) ]

     df_busy_cell_count_1800['小区名称'] = df_busy_cell_count_1800['小区名称'].map(lambda x:x.replace('曲靖','QJ'))
     df_busy_cell_count_1800['小区名称'] = df_busy_cell_count_1800['小区名称'].map(lambda x:x.replace('Q麒麟','QJ麒麟'))
     df_busy_cell_count_1800['小区名称'] = df_busy_cell_count_1800['小区名称'].map(lambda x:x.replace('QJQJ','QJ'))
     df_busy_cell_count_1800['区县'] = df_busy_cell_count_1800['小区名称'].map(lambda x:x.split('QJ')[1][:2])

     df_busy_cell_count_1800 = df_busy_cell_count_1800[df_busy_cell_count_1800['日期'] >= 4]

     df_res_1800 = df_res_1800.append(df_busy_cell_count_1800)


df_high_Data_800 = df_zte_L800[(df_zte_L800['小区总流量(GB)'] >= 1.5) & (df_zte_L800['下行PRB平均占用率_1'] >= 0.5) ]
df_massive_users_800 = df_zte_L800[(df_zte_L800['最大RRC连接用户数_1'] >= 50) & (df_zte_L800['下行PRB平均占用率_1'] >= 0.5) ]

df_busy_cell_800 = df_high_Data_800.append(df_massive_users_800)

df_res_800 = pd.DataFrame()
for week in list(set(df_busy_cell_800['周'])):
     df_800 =  df_busy_cell_800[df_busy_cell_800['周'] == week]
     df_pivot_800 = pd.pivot_table(df_800, index=['周','日期','网元','小区','小区名称'],
                                            values =['小区总流量(GB)' ,
                                                     '下行PRB平均占用率_1',
                                                     '最大RRC连接用户数_1'],
                                            aggfunc = {'小区总流量(GB)':np.max,
                                                       '下行PRB平均占用率_1':np.max,
                                                       '最大RRC连接用户数_1':np.max})
     df_pivot_800 = df_pivot_800.reset_index()

     df_busy_cell_count_800 = pd.pivot_table(df_pivot_800, index=['周','网元','小区','小区名称'],
                                                           values =['日期'],
                                                           aggfunc = {'日期':'count'})
     df_busy_cell_count_800  = df_busy_cell_count_800.reset_index()

     df_busy_cell_count_800['小区名称'] = df_busy_cell_count_800['小区名称'].map(lambda x:x.replace('曲靖','QJ'))
     df_busy_cell_count_800['区县'] = df_busy_cell_count_800['小区名称'].map(lambda x:x.split('QJ')[1][:2])

     df_busy_cell_count_800 = df_busy_cell_count_800[df_busy_cell_count_800['日期'] >= 4]

     df_res_800 = df_res_800.append(df_busy_cell_count_800)

df_busy_1800 = pd.pivot_table(df_res_1800, index=['区县','网元','小区','小区名称'],
                                            values =['周'],
                                            aggfunc = {'周':len})
df_busy_1800.rename(columns = {'周':'超忙周数'},inplace =True)
df_busy_1800 = df_busy_1800.reset_index()
df_busy_1800.drop_duplicates('小区名称', keep='first', inplace = True)

df_country_1800 = pd.pivot_table(df_busy_1800, index=['区县'],
                                            values =['小区名称'],
                                            aggfunc = {'小区名称':'count'})
df_country_1800 = df_country_1800.reset_index()

df_busy_800 = pd.pivot_table(df_res_800, index=['区县','网元','小区','小区名称'],
                                            values =['周'],
                                            aggfunc = {'周':len})
df_busy_800.rename(columns = {'周':'超忙周数'},inplace =True)
df_busy_800 = df_busy_800.reset_index()

df_busy_800.drop_duplicates('小区名称', keep='first', inplace = True)
df_country_800 = pd.pivot_table(df_busy_800, index=['区县'],
                                            values =['小区名称'],
                                            aggfunc = {'小区名称':'count'})
df_country_800 = df_country_800.reset_index()


with  pd.ExcelWriter(data_path + '中兴超忙小区.xlsx')  as writer:  #输出到excel
    df_busy_1800.to_excel(writer,'1800超忙小区',index=False)
    df_country_1800.to_excel(writer,'1800超忙按县统计',index=False)
    df_busy_800.to_excel(writer,'L800超忙小区',index=False)
    df_country_800.to_excel(writer,'800M超忙按县统计',index=False)




