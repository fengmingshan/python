# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 09:39:32 2019

@author: Administrator
"""

import pandas as pd 
import numpy as np
import os
from datetime import datetime 
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

# =============================================================================
# 生成各县退服清单
# =============================================================================
def 填写退服小区(a,b):
	if pd.isnull(a):
		return b.split('_')[0] + '_' + b.split('_')[1]
	else:
		return a 

def 填写退服时长(a,b):
	if pd.isnull(a):
		return b
	else:
		return a 

current_date = str(datetime.now()).split('.')[0].split(' ')[0]

data_path = r'D:\2019年工作\2019年4月小区退服指标计算（新）' + '\\'
pic_path = r'D:\2019年工作\2019年4月小区退服指标计算（新）\PIC' + '\\'

all_files = os.listdir(data_path)
break_files = [x for x in all_files if 'alarm_cel_exit_service_child' in x] 

df_ALL = pd.DataFrame()
for file in break_files :
    df_tmp = pd.read_excel(data_path + file,skiprows = 1)
    df_ALL= df_ALL.append(df_tmp)
df_ALL = df_ALL.reset_index()
df_ALL.drop('index',axis = 1,inplace = True)

df_LTE = df_ALL[(df_ALL['是否NB小区'] == '否') | (df_ALL['是否NB小区'].isnull() == True) ] 

df_LTE.columns
df_LTE['退服小区标识'] = df_LTE.apply(lambda x : 填写退服小区(x.关联小区标识,x.告警对象名称),axis = 1)
df_LTE['LTE小区个数'] = df_LTE['LTE小区个数'].map(lambda x : 1 if pd.isnull(x) else x)
df_LTE.rename(columns={'退服时长(分钟)':'总退服时长',
                       '6-8点退服时长（分钟）':'总6至8点退服时长',
                       '8-22点退服时长（分钟）':'总8至22点退服时长',
                       '22-24点退服时长（分钟）':'总22至24点退服时长',
                       'LTE6-8点退服时长（分钟）':'LTE6至8点退服时长',
                       'LTE8-22点退服时长（分钟）':'LTE8至22点退服时长',
                       'LTE22-24点退服时长（分钟）':'LTE22至24点退服时长',},inplace =True)

df_LTE['LTE退服总时长'] = df_LTE.apply(lambda x : 填写退服时长(x.LTE退服总时长,x.总退服时长),axis = 1)
df_LTE['LTE6至8点退服时长'] = df_LTE.apply(lambda x : 填写退服时长(x.LTE6至8点退服时长,x.总6至8点退服时长),axis = 1)
df_LTE['LTE8至22点退服时长'] = df_LTE.apply(lambda x : 填写退服时长(x.LTE8至22点退服时长,x.总8至22点退服时长),axis = 1)
df_LTE['LTE22至24点退服时长'] = df_LTE.apply(lambda x : 填写退服时长(x.LTE22至24点退服时长,x.总22至24点退服时长),axis = 1)

with  pd.ExcelWriter(data_path + '各县退服清单.xlsx')  as writer:  #输出到excel
    for name in ['沾益县', '会泽县', '罗平县', '宣威市', '麒麟区', '马龙县', '富源县', '陆良县', '师宗县']:
        df_break = df_LTE[df_LTE['区县'] == name]
        
        
# =============================================================================
# 计算各县累计断站时长
# =============================================================================
statistics_file = [x for x in all_files if '小区退服时长统计' in x]
df_statistics = pd.read_excel(data_path + statistics_file[0],skiprows = 3)
df_country_break = pd.pivot_table(df_statistics, index=['地市/区县'], 
                                              values =['6-8点小区平均退服时长（分钟）' ,
                                                       '8-22点小区平均退服时长（分钟）',
                                                       '22-24点小区平均退服时长（分钟）',
                                                       '6-8点小区平均退服时长（分钟）.1',
                                                       '8-22点小区平均退服时长（分钟）.1',
                                                       '22-24点小区平均退服时长（分钟）.1',
                                                       '6-8点小区平均退服时长（分钟）.2',
                                                       '8-22点小区平均退服时长（分钟）.2',
                                                       '22-24点小区平均退服时长（分钟）.2',
                                                       '6-8点小区平均退服时长（分钟）.3',
                                                       '8-22点小区平均退服时长（分钟）.3',
                                                       '22-24点小区平均退服时长（分钟）.3',
                                                       'A类小区总数',
                                                       'B类小区总数',
                                                       'C类小区总数',
                                                       'D类小区总数'], 
                                              aggfunc = {'6-8点小区平均退服时长（分钟）':np.sum,
                                                         '8-22点小区平均退服时长（分钟）':np.sum,
                                                         '22-24点小区平均退服时长（分钟）':np.sum,
                                                         '6-8点小区平均退服时长（分钟）.1':np.sum,
                                                         '8-22点小区平均退服时长（分钟）.1':np.sum,
                                                         '22-24点小区平均退服时长（分钟）.1':np.sum,
                                                         '6-8点小区平均退服时长（分钟）.2':np.sum,
                                                         '8-22点小区平均退服时长（分钟）.2':np.sum,
                                                         '22-24点小区平均退服时长（分钟）.2':np.sum,
                                                         '6-8点小区平均退服时长（分钟）.3':np.sum,
                                                         '8-22点小区平均退服时长（分钟）.3':np.sum,
                                                         '22-24点小区平均退服时长（分钟）.3':np.sum,
                                                         'A类小区总数':np.max,
                                                         'B类小区总数':np.max,
                                                         'C类小区总数':np.max,
                                                         'D类小区总数':np.max})     
df_country_break['A类小区平均退服时长'] = df_country_break['6-8点小区平均退服时长（分钟）'] * 0.8 + \
                                         df_country_break['8-22点小区平均退服时长（分钟）'] * 1.2 + \
                                         df_country_break['22-24点小区平均退服时长（分钟）'] * 0.8
df_country_break['B类小区平均退服时长'] = df_country_break['6-8点小区平均退服时长（分钟）.1'] * 0.8 + \
                                         df_country_break['8-22点小区平均退服时长（分钟）.1'] * 1.2 + \
                                         df_country_break['22-24点小区平均退服时长（分钟）.1'] * 0.8
df_country_break['CD类小区平均退服时长'] = df_country_break['6-8点小区平均退服时长（分钟）.2'] * 0.8 +  \
                                            df_country_break['8-22点小区平均退服时长（分钟）.2'] * 1.2 + \
                                            df_country_break['22-24点小区平均退服时长（分钟）.2'] * 0.8 + \
                                            df_country_break['6-8点小区平均退服时长（分钟）.3'] * 0.8 + \
                                            df_country_break['8-22点小区平均退服时长（分钟）.3'] * 1.2 + \
                                            df_country_break['22-24点小区平均退服时长（分钟）.3'] * 0.8
df_country_break['CD类小区总数'] =   df_country_break['C类小区总数'] +  df_country_break['D类小区总数']  
                                      
df_country_break = df_country_break[['地市/区县','A类小区总数','A类小区平均退服时长','B类小区总数','B类小区平均退服时长','CD类小区总数','CD类小区平均退服时长']]
df_country_break.rename(columns={'A类小区平均退服时长':'A类小区平均退服时长(达标值: <115分钟)',
                                   'B类小区平均退服时长':'B类小区平均退服时长(达标值: <150分钟)',
                                   'CD类小区平均退服时长':'CD类小区平均退服时长(达标值: <300分钟)',},inplace =True)

with  pd.ExcelWriter(data_path + '小区退服时长汇总.xlsx')  as writer:  #输出到excel
    df_country_break.to_excel(writer,'小区退服时长汇总',index=False) 

    
