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
from datetime import date

# =============================================================================
# 环境变量
# =============================================================================
data_path = r'd:\_话务量划小报表\LTE话务数据' + '\\'
out_path = r'd:\_话务量划小报表' + '\\'
eNode_name = 'eNode_name.xls'

os.chdir(data_path) 
all_files = os.listdir() 
df_eNodeB = pd.read_excel(out_path + eNode_name,encoding = 'utf-8')
country_list = list(set(df_eNodeB['区县']))
list_tmp =[]
for i in range(0,len(country_list),1):
    list_tmp.append((country_list[i],i))

country_dict = dict(list_tmp)

df_list = list(range(0,9))

df_combine = pd.DataFrame()
for file in all_files:    
    df_tmp = pd.read_csv(file,engine = 'python',skiprows = 5,encoding = 'gbk')
    df_tmp['空口上行用户面流量（MByte）_1'] = df_tmp['空口上行用户面流量（MByte）_1'].map(lambda x:float(x.replace(',','')))
    df_tmp['空口下行用户面流量（MByte）_1477070755617-11'] = df_tmp['空口下行用户面流量（MByte）_1477070755617-11'].map(lambda x:float(x.replace(',','')))
    df_tmp['上行PRB平均占用率_1'] = df_tmp['上行PRB平均占用率_1'].map(lambda x:float(x.replace('%',''))/100)
    df_tmp['下行PRB平均占用率_1'] = df_tmp['下行PRB平均占用率_1'].map(lambda x:float(x.replace('%',''))/100)

    date = df_tmp.loc[0,'开始时间'].split(' ')[0] 
    
    df_pivot = pd.pivot_table(df_tmp, index=['网元'],
                              values = ['最大RRC连接用户数_1',
                                        '最大激活用户数_1',
                                        '空口上行用户面流量（MByte）_1',
                                        '空口下行用户面流量（MByte）_1477070755617-11',
                                        '上行PRB平均占用率_1',
                                        '下行PRB平均占用率_1',
                                        '分QCI用户体验上行平均速率（Mbps）_1',
                                        '分QCI用户体验下行平均速率（Mbps）_1'],                                   
                              aggfunc = {'最大RRC连接用户数_1':np.median,
                                         '最大激活用户数_1':np.median,
                                         '空口上行用户面流量（MByte）_1':np.sum,
                                         '空口下行用户面流量（MByte）_1477070755617-11':np.sum,
                                         '上行PRB平均占用率_1':np.max,
                                         '下行PRB平均占用率_1':np.max,
                                         '分QCI用户体验上行平均速率（Mbps）_1':np.median,
                                         '分QCI用户体验下行平均速率（Mbps）_1':np.median})    
    df_pivot['总流量'] = df_pivot['空口上行用户面流量（MByte）_1'] + df_pivot['空口下行用户面流量（MByte）_1477070755617-11']
    df_pivot['日期'] = date
    df_pivot = df_pivot.reset_index()
    df_combine = df_combine.append(df_pivot) 
    
df_combine = pd.merge(df_combine,df_eNodeB,how='left',on = '网元')
df_combine['最大RRC连接用户数_1'] = df_combine['最大RRC连接用户数_1'].map(lambda x:round(x,0))
df_combine['最大激活用户数_1'] = df_combine['最大激活用户数_1'].map(lambda x:round(x,0))

# =============================================================================
# 全市用户数和流量
# =============================================================================
df_all = pd.pivot_table(df_combine, index=['日期'],values=['最大RRC连接用户数_1','最大激活用户数_1','总流量'],
                         aggfunc = {'最大RRC连接用户数_1':np.sum,'最大激活用户数_1':np.sum,'总流量':np.sum})  
df_all = df_all.rename(columns={'最大RRC连接用户数_1':'开机用户数','最大激活用户数_1':'联网用户数'})
df_all['总流量'] =  df_all['总流量']/1024
df_all = df_all.reset_index()

y = df_all['开机用户数'].T.values
x = list(df_all['日期'])
plt.figure(figsize=(6, 4))
plt.plot(x,y,label='开机用户数',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=12) 
plt.xlabel('日期')
plt.ylabel('开机用户数')
plt.title('日开机用户数变化情况')
plt.savefig(out_path + "全市开机用户数.png",format='png', dpi=200)  
plt.show()
plt.close()

y = df_all['联网用户数'].T.values
x = list(df_all['日期'])
plt.figure(figsize=(6, 4))
plt.plot(x,y,label='联网用户数',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=12) 
plt.xlabel('日期')
plt.ylabel('联网用户数')
plt.title('日联网用户数变化情况')
plt.savefig(out_path + "全市联网用户数.png",format='png', dpi=200)  
plt.show()
plt.close()

y = df_all['总流量'].T.values
x = list(df_all['日期'])
plt.figure(figsize=(6, 4))
plt.plot(x,y,label='总流量',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=12) 
plt.xlabel('日期')
plt.ylabel('总流量')
plt.title('日总流量变化情况')
plt.savefig(out_path + "全市总流量.png",format='png', dpi=200)  
plt.show()
plt.close()

book = xlsxwriter.Workbook(out_path + '全市用户数及流量.xlsx')     # 将图片插入到excel表格中 
sheet = book.add_worksheet('全市用户数及流量')
sheet.insert_image('A2' , out_path + "全市开机用户数.png")
sheet.insert_image('J2', out_path + "全市联网用户数.png")
sheet.insert_image('A23', out_path + "全市总流量.png")
book.close()
                                 
df_city = pd.pivot_table(df_combine, index=['区县','日期'],values=['最大RRC连接用户数_1','最大激活用户数_1','总流量'],
                         aggfunc = {'最大RRC连接用户数_1':np.sum,'最大激活用户数_1':np.sum,'总流量':np.sum})                                

for i in range(0,len(country_list),1):
    df_list[i] = df_combine[df_combine['区县'] == country_list[i]] 

                                  

