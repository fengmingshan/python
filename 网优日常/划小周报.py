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
from datetime import timedelta


plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

# =============================================================================
# 环境变量
# =============================================================================
data_path = r'd:\_话务量划小报表\LTE话务数据' + '\\'
out_path = r'd:\_话务量划小报表' + '\\'
pic_path = r'd:\_话务量划小报表\pic' + '\\'
eNode_name = 'eNode_name.xls'

yestoday = str(datetime.now() - timedelta(days=1)).split(' ')[0]
before_yestoday = str(datetime.now() - timedelta(days=2)).split(' ')[0]

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
    df_tmp = pd.read_csv(file,skiprows = 5,engine = 'python', encoding = 'gbk')
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
df_all = df_all.rename(columns={'最大RRC连接用户数_1':'联网用户数','最大激活用户数_1':'在线用户数'})
df_all['总流量'] =  df_all['总流量'].map(lambda x:round(float(x/(1024*1024)),1))
df_all = df_all.reset_index()
df_all['日期'] =  df_all['日期'].map(lambda x:x[5:10])


y = df_all['联网用户数'].T.values
x = list(df_all['日期'])
plt.figure(figsize=(6, 4))
plt.plot(x,y,label='联网用户数',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=8) 
for a,b in zip(x,y):
    plt.text(a, b*1.001, '%d' % b, ha='center', va= 'bottom',fontsize=12)
plt.xlabel('日期')
plt.ylabel('联网用户数')
plt.title('日联网用户数变化情况')
plt.savefig(pic_path + "全市联网用户数.png",format='png', dpi=200)  
plt.close()

y = df_all['总流量'].T.values
x = list(df_all['日期'])
plt.figure(figsize=(6, 4))
plt.plot(x,y,label='总流量',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=8) 
for a,b in zip(x,y):
    plt.text(a, b*1.001, '%.1f' % b, ha='center', va= 'bottom',fontsize=12)
plt.xlabel('日期')
plt.ylabel('总流量(TB)')
plt.title('日总流量变化情况')
plt.savefig(pic_path + "全市总流量.png",format='png', dpi=200)  
plt.close()

#按区县和日期透视
df_city = pd.pivot_table(df_combine, index=['区县','日期'],values=['最大RRC连接用户数_1','最大激活用户数_1','总流量'],
                         aggfunc = {'最大RRC连接用户数_1':np.sum,'最大激活用户数_1':np.sum,'总流量':np.sum})                                
df_city = df_city.reset_index()

yestoday_new_user = []
total_new_user = []
for country in country_list:
    df_country = df_city[df_city['区县'] == country]
    yestoday_new_user.append(df_country.iloc[-1 , 3] - df_country.iloc[-2 , 3])
    total_new_user.append(df_country.iloc[-1 , 3] - df_country.iloc[0 , 3])


plt.figure(figsize=(6, 4))
plt.bar(country_list,yestoday_new_user,color='g',width = 0.3,alpha=0.6,label='新增用户数')
for x,y in zip(country_list,yestoday_new_user):
    plt.text(x, y+10, '%d' % y, ha='center', va= 'bottom',fontsize=12)
plt.xlabel('昨日新增用户数')
plt.ylabel('区县')
plt.title('各县昨日新增用户数')
plt.savefig(pic_path + "各县昨日新增用户数.png",format='png', dpi=200)  
plt.close()

plt.figure(figsize=(6, 4))
plt.bar(country_list,total_new_user,color='g',width = 0.3,alpha=0.6,label='累计新增用户数')
for x,y in zip(country_list,total_new_user):
    plt.text(x, y+10, '%d' % y, ha='center', va= 'bottom',fontsize=12)
plt.xlabel('累计新增用户数')
plt.ylabel('区县')
plt.title('各县累计新增用户数')
plt.savefig(pic_path + "各县累计新增用户数.png",format='png', dpi=200)  
plt.close()



# =============================================================================
# 生成各区县数据
# =============================================================================                           
for i in range(0,len(country_list),1):
    df_list[i] = df_combine[df_combine['区县'] == country_list[i]] 

for df_country in df_list:
    df_country = df_country.reset_index() 
    country_name = df_country.loc[0,'区县']
    df_country_pivot = df_country.groupby(by = '日期',as_index=False)[['最大RRC连接用户数_1','总流量']].sum()
    df_country_pivot['总流量'] = df_country_pivot['总流量'].map(lambda x:round(float(x/(1024*1024)),1))
    df_country_pivot['日期'] = df_country_pivot['日期'].map(lambda x:x[5:10])
    # =============================================================================
    # 画各县联网用户数图   
    # =============================================================================
    x = list(df_country_pivot['日期'])
    y = df_country_pivot['最大RRC连接用户数_1'].T.values
    plt.figure(figsize=(6, 4))
    plt.plot(x,y,label='联网用户数',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=8) 
    for a,b in zip(x,y):
        plt.text(a, b*1.001, '%d' % b, ha='center', va= 'bottom',fontsize=12)
    plt.xlabel('日期')
    plt.ylabel(country_name + '联网用户数')
    plt.title(country_name + '联网用户数')
    plt.savefig(pic_path + country_name + "联网用户数.png",format='png', dpi=200)  
    plt.close()                                   
    # =============================================================================
    # 画各县流量
    # =============================================================================
    x = list(df_country_pivot['日期'])
    y = df_country_pivot['总流量'].T.values
    plt.figure(figsize=(6, 4))
    plt.plot(x,y,label='总流量(TB)',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=8) 
    for a,b in zip(x,y):
        plt.text(a, b*1.001, '%.1f' % b, ha='center', va= 'bottom',fontsize=12)
    plt.xlabel('日期')
    plt.ylabel(country_name + '总流量(TB)')
    plt.title(country_name + '总流量(TB)')
    plt.savefig(pic_path + country_name + "总流量.png",format='png', dpi=200)  
    plt.close()
    # =============================================================================
    # 按支局透视 
    # =============================================================================
    substation_list = list(set(df_country['支局']))
    df_substation_pivot = pd.pivot_table(df_country, index=['支局','日期'],values=['最大RRC连接用户数_1','总流量'],
                                         aggfunc = {'最大RRC连接用户数_1':np.sum,'总流量':np.sum}) 
    df_substation_pivot = df_substation_pivot.reset_index()
    # =============================================================================
    # 画各支局用户数增长图  
    # =============================================================================  
    substation_new_user = []
    substation_total_user = []
    for substation in substation_list:
        df_substation = df_substation_pivot[df_substation_pivot['支局'] == substation]
        substation_new_user.append(df_substation.iloc[-1,3]-df_substation.iloc[-2,3]) 
        substation_total_user.append(df_substation.iloc[-1,3]-df_substation.iloc[0,3]) 
   
     
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
    plt.bar(substation_list,substation_total_user,color='g',width = 0.3,alpha=0.6,label='昨日新增用户数')
    for x,y in zip(substation_list,substation_total_user):
        plt.text(x, y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=12)
    plt.xlabel('支局')
    plt.ylabel('累计新增用户数')
    plt.title(country_name + '各支局累计新增用户数')
    plt.savefig(pic_path + country_name + "各支局累计新增用户数.png",format='png', dpi=200)  
    plt.close()


    # =============================================================================
    # 画各支局日用户数、日流量
    # =============================================================================
    for substation in substation_list:
        df_substation = df_substation_pivot[df_substation_pivot['支局'] == substation]
        df_substation['总流量'] =  df_substation['总流量'].map(lambda x:round(float(x/(1024*1024)),1))
        df_substation['日期'] = df_substation['日期'].map(lambda x:x[5:10])
        x = list(df_substation['日期'])
        y = df_substation['最大RRC连接用户数_1'].T.values
        plt.figure(figsize=(6, 4))
        plt.plot(x,y,label='联网用户数',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=8) 
        for a,b in zip(x,y):
            plt.text(a, b*1.001, '%d' % b, ha='center', va= 'bottom',fontsize=12)
        plt.xlabel('日期')
        plt.ylabel(substation +'支局_联网用户数')
        plt.title(country_name + '_' +substation +'支局_联网用户数')
        plt.savefig(pic_path + country_name + substation + '支局_联网用户数.png',format='png', dpi=200)  
        plt.close()                                   

        x = list(df_substation['日期'])
        y = df_substation['总流量'].T.values
        plt.figure(figsize=(6, 4))
        plt.plot(x,y,label='总流量(TB)',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=8) 
        for a,b in zip(x,y):
            plt.text(a, b*1.001, '%.1f' % b, ha='center', va= 'bottom',fontsize=12)
        plt.xlabel('日期')
        plt.ylabel(substation+ '支局_总流量(TB)')
        plt.title(country_name + '_' +substation+ '支局_总流量(TB)')
        plt.savefig(pic_path + country_name + substation + "支局_总流量.png",format='png', dpi=200)  
        plt.close()                                   
        
# =============================================================================
# 生成全市汇总表格
# =============================================================================
book = xlsxwriter.Workbook(out_path + '_全市各区县用户数及流量.xlsx')     # 将图片插入到excel表格中 
sheet = book.add_worksheet('全市用户数及流量')
sheet.insert_image('A2' , pic_path + "全市联网用户数.png")
sheet.insert_image('J2', pic_path +  "全市总流量.png")
sheet.insert_image('A23', pic_path + "各县昨日新增用户数.png")
sheet.insert_image('J23', pic_path + "各县累计新增用户数.png")

for country in country_list:
    sheet = book.add_worksheet(country)
    sheet.insert_image('A2' , pic_path + country + "联网用户数.png")
    sheet.insert_image('J2', pic_path + country + "总流量.png")
    sheet.insert_image('A23', pic_path + country + "各支局昨日新增用户数.png")
    sheet.insert_image('J23', pic_path + country + "各支局累计新增用户数.png")

book.close()

# =============================================================================
# 生成各县表格
# =============================================================================
for i in range(0,len(df_list),1):
    substation_list = list(set(df_list[i]['支局']))
    book = xlsxwriter.Workbook(out_path + country_list[i] + '各支局用户数及流量.xlsx')     # 将图片插入到excel表格中         
    for substation in substation_list:
        sheet = book.add_worksheet(substation)
        sheet.insert_image('A2' , pic_path +country_list[i]+ substation + '支局_联网用户数.png')
        sheet.insert_image('J2', pic_path + country_list[i]+ substation + "支局_总流量.png")
    book.close()
        
