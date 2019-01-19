# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 17:22:00 2018

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

path_4g = r'D:\_话务周报(划小到支局)\4G' + '\\'
path_4g_busy = r'D:\_话务周报(划小到支局)\4G忙时' + '\\'

data_path = r'D:\_话务周报(划小到支局)' + '\\'
out_path = r'D:\_话务周报(划小到支局)\报表输出' + '\\'
pic_path = r'D:\_话务周报(划小到支局)\pic' + '\\'

df_zte_eNodeB =  pd.read_excel(data_path + 'zte_eNode_name.xls',encoding = 'utf-8')
df_eric_eNodeB =  pd.read_excel(data_path + '爱立信关联支局.xlsx',encoding = 'utf-8')


df_eric_titles  = pd.read_excel(data_path + 'title.xlsx',encoding = 'utf-8')
titles = list(df_eric_titles.columns)

df_eric_busy_titles  = pd.read_excel(data_path + 'busy_title.xlsx',encoding = 'utf-8')
busy_titles = list(df_eric_busy_titles.columns)



files_4G = os.listdir(path_4g) 
zte_4G_files = [x for x in files_4G if '历史性能' in x]
eric_4G_files = [x for x in files_4G if '爱立信' in x]


files_4G_busy = os.listdir(path_4g_busy) 
zte_4G_busy_files = [x for x in files_4G_busy if '历史性能' in x]
eric_4G_busy_files = [x for x in files_4G_busy if '爱立信' in x]

df_eric_4G_traffic = pd.DataFrame()
for file in eric_4G_files:    
    df_tmp = pd.read_csv(path_4g + file,header = None,names = titles, engine = 'python', encoding = 'gbk')
    df_tmp.fillna(0,inplace=True)
    df_tmp['DATE_ID'] = df_tmp['DATE_ID'].map(lambda x:x.replace('\'',''))
    df_tmp['eNodeB'] = df_tmp['eNodeB'].map(lambda x:x.replace('\'',''))
    week = df_tmp.iloc[0,0][5:10] + "_" + df_tmp.iloc[-1,0][5:10]
    df_tmp['week'] = week
    df_tmp.rename(columns={'eNodeB':'网元',
                         'Air Interface_Traffic_Volume_UL_MBytes':'上行流量(MB)',
                         'Air Interface_Traffic_Volume_DL_MBytes':'下行流量(MB)'},inplace =True)
    df_tmp['总流量(MB)'] =  df_tmp['上行流量(MB)'] + df_tmp['下行流量(MB)'] 
    df_tmp =  df_tmp[['week','网元','总流量(MB)']]
    df_pivot_traffic = pd.pivot_table(df_tmp, index=['week','网元'], 
                                      values = '总流量(MB)', 
                                      aggfunc = {'总流量(MB)':np.sum})
    df_pivot_traffic = df_pivot_traffic.reset_index()                                                     
    df_eric_4G_traffic = df_eric_4G_traffic.append(df_pivot_traffic)
df_eric_4G_traffic['网元'] = df_eric_4G_traffic['网元'].astype(int)
df_eric_4G_traffic = pd.merge(df_eric_4G_traffic,df_eric_eNodeB,how ='left',on = '网元' )     

df_eric_4G_user = pd.DataFrame()
for file in eric_4G_busy_files:    
    df_tmp = pd.read_csv(path_4g_busy + file,header = None,names = busy_titles, engine = 'python', encoding = 'gbk')
    df_tmp.fillna(0,inplace=True)
    df_tmp['DATE_ID'] = df_tmp['DATE_ID'].map(lambda x:x.replace('\'',''))
    df_tmp['eNodeB'] = df_tmp['eNodeB'].map(lambda x:x.replace('\'',''))
    df_tmp['DATE_HOUR'] = df_tmp['DATE_ID'].map(str) + '_' + df_tmp['HOUR_ID'].map(str)
    # =============================================================================
    # 计算每日实际忙时确定RRC连接用户数
    # =============================================================================
    df_pivot_rrc = pd.pivot_table(df_tmp, index=['DATE_HOUR'], values = 'Max number of UE in RRc', aggfunc = {'Max number of UE in RRc':np.sum})                                                  
    df_pivot_rrc = df_pivot_rrc.sort_values(by='Max number of UE in RRc',ascending = False)
    df_pivot_rrc = df_pivot_rrc.reset_index()
    busy_hour =  df_pivot_rrc.loc[0,'DATE_HOUR']
    df_max_rrc =  df_tmp[['DATE_ID','eNodeB','Max number of UE in RRc']][df_tmp['DATE_HOUR'] == busy_hour]    
    week = df_tmp.iloc[0,0][5:10] + "_" + df_tmp.iloc[-1,0][5:10]
    df_max_rrc['week'] = week
    df_max_rrc.rename(columns={'eNodeB':'网元',
                               'Max number of UE in RRc':'RRC连接用户数'},inplace =True)
    df_max_rrc =  df_max_rrc[['week','网元','RRC连接用户数']]
    df_eric_4G_user = df_eric_4G_user.append(df_max_rrc)
df_eric_4G_user['网元'] = df_eric_4G_user['网元'].astype(int)
df_eric_4G_user = pd.merge(df_eric_4G_user,df_eric_eNodeB,how ='left',on = '网元' )     


df_zte_4G_traffic = pd.DataFrame()
for file in zte_4G_files:    
    df_tmp = pd.read_csv(path_4g + file,skiprows = 5,engine = 'python', encoding = 'gbk')
    df_tmp.fillna(0,inplace=True)
    df_tmp['空口上行用户面流量（MByte）_1'] = df_tmp['空口上行用户面流量（MByte）_1'].map(lambda x:float(x.replace(',','')))
    df_tmp['空口下行用户面流量（MByte）_1477070755617-11'] = df_tmp['空口下行用户面流量（MByte）_1477070755617-11'].map(lambda x:float(x.replace(',','')))
    df_tmp['开始时间'] = pd.to_datetime(df_tmp['开始时间'],format="%Y-%m-%d")  
    week = str(df_tmp.iloc[0,1]).split(' ')[0][5:10] + "_" + str(df_tmp.iloc[-1,1]).split(' ')[0][5:10]
    df_tmp['week'] = week
    df_tmp.rename(columns={'空口上行用户面流量（MByte）_1':'上行流量(MB)',
                           '空口下行用户面流量（MByte）_1477070755617-11':'下行流量(MB)'},inplace =True)
    df_tmp['总流量(MB)'] =  df_tmp['上行流量(MB)'] + df_tmp['下行流量(MB)'] 
    df_tmp =  df_tmp[['week','网元','总流量(MB)']]
    df_pivot_traffic = pd.pivot_table(df_tmp, index=['week','网元'], 
                                              values = '总流量(MB)', 
                                              aggfunc = {'总流量(MB)':np.sum})  
    df_pivot_traffic = df_pivot_traffic.reset_index()                                                     
    df_zte_4G_traffic = df_zte_4G_traffic.append(df_pivot_traffic)
df_zte_4G_traffic['网元'] = df_zte_4G_traffic['网元'].astype(int)
df_zte_4G_traffic = pd.merge(df_zte_4G_traffic,df_zte_eNodeB,how ='left',on = '网元' )     


df_zte_4G_user = pd.DataFrame()
for file in zte_4G_busy_files:    
    df_tmp = pd.read_csv(path_4g_busy + file,skiprows = 5,engine = 'python', encoding = 'gbk')
    df_tmp.fillna(0,inplace=True)
    df_tmp['空口上行用户面流量（MByte）_1'] = df_tmp['空口上行用户面流量（MByte）_1'].map(lambda x:float(x.replace(',','')))
    df_tmp['空口下行用户面流量（MByte）_1477070755617-11'] = df_tmp['空口下行用户面流量（MByte）_1477070755617-11'].map(lambda x:float(x.replace(',','')))
    df_tmp['开始时间'] = pd.to_datetime(df_tmp['开始时间'],format="%Y-%m-%d")  
    # =============================================================================
    # 计算每日实际忙时确定RRC连接用户数
    # =============================================================================
    df_pivot_rrc = pd.pivot_table(df_tmp, index=['开始时间'], values = '最大RRC连接用户数_1', aggfunc = {'最大RRC连接用户数_1':np.sum})                                                  
    df_pivot_rrc = df_pivot_rrc.sort_values(by='最大RRC连接用户数_1',ascending = False)
    df_pivot_rrc = df_pivot_rrc.reset_index()
    busy_hour =  df_pivot_rrc.loc[0,'开始时间']
    df_max_rrc =  df_tmp[['开始时间','网元','最大RRC连接用户数_1']][df_tmp['开始时间'] == busy_hour]    
    week = str(df_tmp.iloc[0,1]).split(' ')[0][5:10] + "_" + str(df_tmp.iloc[-1,1]).split(' ')[0][5:10]
    df_max_rrc['week'] = week
    df_max_rrc.rename(columns={'最大RRC连接用户数_1':'RRC连接用户数'},inplace =True)
    df_max_rrc =  df_max_rrc[['week','网元','RRC连接用户数']]
    df_zte_4G_user = df_zte_4G_user.append(df_max_rrc)
df_zte_4G_user['网元'] = df_zte_4G_user['网元'].astype(int)
df_zte_4G_user = pd.merge(df_zte_4G_user,df_zte_eNodeB,how ='left',on = '网元' )     

df_4Guser_ALL = df_eric_4G_user.append(df_zte_4G_user)
df_4Guser_ALL['week-eNodeB'] = df_4Guser_ALL['week'] + '_' + df_4Guser_ALL['网元'].map(str)
df_4Guser_ALL =  df_4Guser_ALL[['week-eNodeB','RRC连接用户数']]

df_4G_ALL = df_eric_4G_traffic.append(df_zte_4G_traffic)
df_4G_ALL['week-eNodeB'] = df_4G_ALL['week'] + '_' + df_4G_ALL['网元'].map(str)
df_4G_ALL = pd.merge(df_4G_ALL,df_4Guser_ALL,how ='left',on = 'week-eNodeB' )

df_4G_ALL['总流量(MB)'] = df_4G_ALL['总流量(MB)']/1024
df_4G_ALL['总流量(MB)'] = df_4G_ALL['总流量(MB)'].map(lambda x:round(x,1))
df_4G_ALL.rename(columns={'总流量(MB)':'总流量(GB)'},inplace =True)

# =============================================================================
# 各县基站总数
# =============================================================================
df_4G_country =  pd.pivot_table(df_4G_ALL, index=['week','区县'], values = '网元', aggfunc = {'网元':len}) 
df_4G_country = df_4G_country.reset_index()
df_4G_country.rename(columns={'网元':'基站数量'},inplace =True)               
df_4G_country['week-区县'] = df_4G_country['week'] + '-' + df_4G_country['区县']

# =============================================================================
# 各县零流量基站数量
# =============================================================================
df_zero_traffic = df_4G_ALL[df_4G_ALL['总流量(GB)']==0]
df_zero_traffic =  pd.pivot_table(df_zero_traffic,
                                  index=['week','区县'], 
                                  values = '网元', aggfunc = {'网元':len})
df_zero_traffic.rename(columns={'网元':'零流量基站数量'},inplace =True)               
df_zero_traffic =  df_zero_traffic.reset_index()
df_zero_traffic['week-区县'] = df_zero_traffic['week'] + '-' + df_zero_traffic['区县']
df_zero_traffic = df_zero_traffic[['week-区县','零流量基站数量']] 

# =============================================================================
# 4G用户数
# =============================================================================
df_rrc_uesr =  pd.pivot_table(df_4G_ALL,
                              index=['week','区县'],
                              values = 'RRC连接用户数', aggfunc = {'RRC连接用户数':sum})                  
df_rrc_uesr =  df_rrc_uesr.reset_index()
df_rrc_uesr['week-区县'] = df_rrc_uesr['week'] + '-' + df_rrc_uesr['区县']
df_rrc_uesr = df_rrc_uesr[['week-区县','RRC连接用户数']] 
# =============================================================================
# 4G总流量
# =============================================================================
df_4G_traffic =  pd.pivot_table(df_4G_ALL,
                                index=['week','区县'],
                                values = '总流量(GB)', aggfunc = {'总流量(GB)':sum})                  
df_4G_traffic =  df_4G_traffic.reset_index()
df_4G_traffic['week-区县'] = df_4G_traffic['week'] + '-' + df_4G_traffic['区县']
df_4G_traffic = df_4G_traffic[['week-区县','总流量(GB)']] 

df_4G_country = pd.merge(df_4G_country,df_zero_traffic,how ='left',on = 'week-区县' )    
df_4G_country = pd.merge(df_4G_country,df_rrc_uesr,how ='left',on = 'week-区县' )    
df_4G_country = pd.merge(df_4G_country,df_4G_traffic,how ='left',on = 'week-区县' )    
df_4G_country.fillna(0,inplace =True)


week1 = df_4G_country.iloc[0,0]
week2 = df_4G_country.iloc[-1,0]
# =============================================================================
# 画基站数量图
# =============================================================================
y1 = df_4G_country['基站数量'][df_4G_country['week'] == week1 ].T.values
y2 = df_4G_country['基站数量'][df_4G_country['week'] == week2 ].T.values
country_list = df_4G_country['区县'][df_4G_country['week'] == week1 ].T.values
plt.figure(figsize=(6, 4))
x_country = range(0,len(country_list)) 
x_country1 = [i+0.35 for i in x_country] 
plt.bar(x_country,y1,color='g',width = 0.3,alpha=0.6,label='上周基站数量')
plt.bar(x_country1,y2,color='b',width = 0.3,alpha=0.6,label='本周基站数量')
for x,y in zip(x_country,y1):
    plt.text(x, y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=8)
for x,y in zip(x_country1,y2 ):
    plt.text(x, y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=8)
plt.xlabel('各县基站数量')
plt.xticks(range(0,len(country_list)),country_list)
plt.ylabel('区县')
plt.legend(loc='upper middle')
plt.title('各县基站数量')
plt.savefig(pic_path + "各县基站数量.png",format='png', dpi=200)  
plt.close()

# =============================================================================
# 画零话务基站数量图
# =============================================================================
y1 = df_4G_country['零流量基站数量'][df_4G_country['week'] == week1 ].T.values
y2 = df_4G_country['零流量基站数量'][df_4G_country['week'] == week2 ].T.values
country_list = df_4G_country['区县'][df_4G_country['week'] == week1 ].T.values
plt.figure(figsize=(6, 4))
x_country = range(0,len(country_list)) 
x_country1 = [i+0.35 for i in x_country] 
plt.bar(x_country,y1,color='g',width = 0.3,alpha=0.6,label='上周零流量基站')
plt.bar(x_country1,y2,color='b',width = 0.3,alpha=0.6,label='本周零流量基站')
for x,y in zip(x_country,y1):
    plt.text(x, y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=8)
for x,y in zip(x_country1,y2 ):
    plt.text(x, y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=8)
plt.xlabel('各县零流量基站数量')
plt.xticks(range(0,len(country_list)),country_list)
plt.ylabel('区县')
plt.legend(loc='upper middle')
plt.title('各县零流量基站数量')
plt.savefig(pic_path + "各县零流量基站数量.png",format='png', dpi=200)  
plt.close()

# =============================================================================
# 画4G用户数
# =============================================================================
y1 = df_4G_country['RRC连接用户数'][df_4G_country['week'] == week1 ].T.values
y2 = df_4G_country['RRC连接用户数'][df_4G_country['week'] == week2 ].T.values
country_list = df_4G_country['区县'][df_4G_country['week'] == week1 ].T.values
plt.figure(figsize=(6, 4))
x_country = range(0,len(country_list)) 
x_country1 = [i+0.35 for i in x_country] 
plt.bar(x_country,y1,color='g',width = 0.3,alpha=0.6,label='上周4G用户数')
plt.bar(x_country1,y2,color='b',width = 0.3,alpha=0.6,label='本周4G用户数')
for x,y in zip(x_country,y1):
    plt.text(x, y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=6)
for x,y in zip(x_country1,y2 ):
    plt.text(x, y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=6)
plt.xlabel('各县4G用户数')
plt.xticks(range(0,len(country_list)),country_list)
plt.ylabel('区县')
plt.legend(loc='upper middle')
plt.title('各县4G用户数')
plt.savefig(pic_path + "各县4G用户数.png",format='png', dpi=200)  
plt.close()

# =============================================================================
# 4G用户数环比变化率
# =============================================================================
y1 = df_4G_country['RRC连接用户数'][df_4G_country['week'] == week1 ].T.values
y2 = df_4G_country['RRC连接用户数'][df_4G_country['week'] == week2 ].T.values
y3 =  [(b-a)/a for a, b in zip(y1,y2)]
country_list = df_4G_country['区县'][df_4G_country['week'] == week1 ].T.values
plt.figure(figsize=(6, 4))
x_country = range(0,len(country_list)) 
plt.bar(x_country,y3,color='b',width = 0.3,alpha=0.6,label='各县4G用户数环比')
for x,y in zip(x_country,y3):
    plt.text(x, y*1.001, '%.2f%%' % (y*100), ha='center', va= 'bottom',fontsize=12)
plt.xlabel('各县4G用户数环比')
plt.xticks(range(0,len(country_list)),country_list)
plt.ylabel('区县')
plt.legend(loc='upper middle')
plt.title('各县4G用户数环比')
plt.savefig(pic_path + "各县4G用户数环比.png",format='png', dpi=200)  
plt.close()

# =============================================================================
# 画4G流量
# =============================================================================
y1 = df_4G_country['总流量(GB)'][df_4G_country['week'] == week1 ].T.values
y2 = df_4G_country['总流量(GB)'][df_4G_country['week'] == week2 ].T.values
country_list = df_4G_country['区县'][df_4G_country['week'] == week1 ].T.values
plt.figure(figsize=(6, 4))
x_country = range(0,len(country_list)) 
x_country1 = [i+0.35 for i in x_country] 
plt.bar(x_country,y1,color='g',width = 0.3,alpha=0.6,label='上周4G流量')
plt.bar(x_country1,y2,color='b',width = 0.3,alpha=0.6,label='本周4G流量')
for x,y in zip(x_country,y1):
    plt.text(x, y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=6)
for x,y in zip(x_country1,y2 ):
    plt.text(x, y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=6)
plt.xlabel('各县4G流量')
plt.xticks(range(0,len(country_list)),country_list)
plt.ylabel('区县')
plt.legend(loc='upper middle')
plt.title('各县4G流量')
plt.savefig(pic_path + "各县4G流量.png",format='png', dpi=200)  
plt.close()

# =============================================================================
# 4G流量环比变化率
# =============================================================================
y1 = df_4G_country['总流量(GB)'][df_4G_country['week'] == week1 ].T.values
y2 = df_4G_country['总流量(GB)'][df_4G_country['week'] == week2 ].T.values
y3 =  [(b-a)/a for a, b in zip(y1,y2)]
country_list = df_4G_country['区县'][df_4G_country['week'] == week1 ].T.values
plt.figure(figsize=(6, 4))
x_country = range(0,len(country_list)) 
x_country1 = [i+0.35 for i in x_country] 
plt.bar(x_country,y3,color='b',width = 0.3,alpha=0.6,label='各县4G流量环比')
for x,y in zip(x_country,y3):
    plt.text(x, y*1.001, '%.2f%%' % (y*100), ha='center', va= 'bottom',fontsize=12)
plt.xlabel('各县4G流量环比')
plt.xticks(range(0,len(country_list)),country_list)
plt.ylabel('区县')
plt.legend(loc='upper middle')
plt.title('各县4G流量环比')
plt.savefig(pic_path + "各县4G流量环比.png",format='png', dpi=200)  
plt.close()

df_country_last_week = df_4G_country[df_4G_country['week'] == week1]
df_country_last_week = df_country_last_week[['区县','基站数量','零流量基站数量','RRC连接用户数','总流量(GB)']]
df_country_last_week.rename(columns={'基站数量':'上周基站数量',
                                     '零流量基站数量':'上周零流量基站数量',
                                     'RRC连接用户数':'上周4G用户数',
                                     '总流量(GB)':'上周4G流量'},inplace =True)
    
df_country_this_week = df_4G_country[df_4G_country['week'] == week2]
df_country_this_week = df_country_this_week[['区县','基站数量','零流量基站数量','RRC连接用户数','总流量(GB)']]
df_country_this_week.rename(columns={'基站数量':'本周周基站数量',
                                     '零流量基站数量':'本周零流量基站数量',
                                     'RRC连接用户数':'本周4G用户数',
                                     '总流量(GB)':'本周4G流量'},inplace =True)
df_country_compare = pd.merge(df_country_last_week, df_country_this_week, how = 'left', on = '区县')
df_country_compare = df_country_compare[['区县','上周基站数量','本周周基站数量',
                                        '上周零流量基站数量','本周零流量基站数量',
                                        '上周4G用户数','本周4G用户数',
                                        '上周4G流量','本周4G流量',]]

df_zero_traffic_list = df_4G_ALL[(df_4G_ALL['week'] == week2)&(df_4G_ALL['总流量(GB)'] == 0)]
df_zero_traffic_list = df_zero_traffic_list[['week','网元名称','总流量(GB)','区县','支局','乡镇_街道','厂家']]

df_4G_this_week = df_4G_ALL[df_4G_ALL['week'] == week2]
df_4G_this_week = df_4G_this_week[['week','网元名称','RRC连接用户数','总流量(GB)','区县','支局','乡镇_街道','厂家']]

with  pd.ExcelWriter(out_path + '4G话务周报_' + week2 +'.xlsx', engine='xlsxwriter') as writer:
    book = writer.book     # 将图片插入到excel表格中 
    sheet = book.add_worksheet('各区县用户数及流量')
    sheet.insert_image('A2' , pic_path + "各县基站数量.png")
    sheet.insert_image('K2', pic_path + "各县零流量基站数量.png")
    sheet.insert_image('A23', pic_path +  "各县4G用户数.png")
    sheet.insert_image('K23', pic_path +  "各县4G用户数环比.png")
    sheet.insert_image('A44', pic_path +  "各县4G流量.png")
    sheet.insert_image('K44', pic_path + "各县4G流量环比.png")
    df_country_compare.to_excel(writer,'各县指标汇总')
    df_zero_traffic_list.to_excel(writer,'零流量基站清单')
    df_4G_this_week.to_excel(writer,'基站详单')

# =============================================================================
# 按县划小到支局
# =============================================================================
country_list = list(set(df_4G_ALL['区县']))
with  pd.ExcelWriter(out_path + '4G话务周报_' + week2 + '_按支局.xlsx',engine='xlsxwriter')  as writer:  #输出到excel
    for country in country_list :
        df_country = df_4G_ALL[df_4G_ALL['区县'] == country]
        df_country_pivot = pd.pivot_table(df_country, index=['week','支局'],
                                      values = ['网元', '总流量(GB)','RRC连接用户数'],                                        
                                      aggfunc = {'网元':len,
                                                 '总流量(GB)':np.sum,
                                                 'RRC连接用户数':np.sum})
        df_country_pivot = df_country_pivot.reset_index()
        df_country_pivot.rename(columns={'网元':'基站数量',
                                         'RRC连接用户数':'4G用户数',
                                         '总流量(GB)':'4G流量'},inplace =True)
        book = writer.book     # 将图片插入到excel表格中 
        sheet = book.add_worksheet(country)
        
        # =============================================================================
        # 画各支局基站数量图
        # =============================================================================
        y1 = df_country_pivot['基站数量'][df_country_pivot['week'] == week1 ].T.values
        y2 = df_country_pivot['基站数量'][df_country_pivot['week'] == week2 ].T.values
        substation_list = df_country_pivot['支局'][df_country_pivot['week'] == week1 ].T.values
        plt.figure(figsize=(6, 4))
        x_substation = range(0,len(substation_list)) 
        x_substation1 = [i+0.35 for i in x_substation] 
        plt.bar(x_substation,y1,color='g',width = 0.3,alpha=0.6,label='上周4G基站数量')
        plt.bar(x_substation1,y2,color='b',width = 0.3,alpha=0.6,label='本周4G基站数量')
        for x,y in zip(x_substation,y1):
            plt.text(x, y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=8)
        for x,y in zip(x_substation1,y2 ):
            plt.text(x, y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=8)
        plt.xlabel(country+'各支局4G基站数量')
        plt.xticks(range(0,len(substation_list)),substation_list)
        plt.ylabel('支局')
        plt.legend(loc='upper middle')
        plt.title(country+'各支局4G基站数量')
        plt.savefig(pic_path + country  + "各支局4G基站数量.png",format='png', dpi=200)  
        plt.close()
        
        # =============================================================================
        # 画各支局4G用户数图
        # =============================================================================
        y1 = df_country_pivot['4G用户数'][df_country_pivot['week'] == week1 ].T.values
        y2 = df_country_pivot['4G用户数'][df_country_pivot['week'] == week2 ].T.values
        substation_list = df_country_pivot['支局'][df_country_pivot['week'] == week1 ].T.values
        plt.figure(figsize=(6, 4))
        x_substation = range(0,len(substation_list)) 
        x_substation1 = [i+0.35 for i in x_substation] 
        plt.bar(x_substation,y1,color='g',width = 0.3,alpha=0.6,label='上周4G用户数')
        plt.bar(x_substation1,y2,color='b',width = 0.3,alpha=0.6,label='本周4G用户数')
        for x,y in zip(x_substation,y1):
            plt.text(x, y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=8)
        for x,y in zip(x_substation1,y2 ):
            plt.text(x, y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=8)
        plt.xlabel(country+'各支局4G用户数')
        plt.xticks(range(0,len(substation_list)),substation_list)
        plt.ylabel('支局')
        plt.legend(loc='upper middle')
        plt.title(country+'各支局4G用户数')
        plt.savefig(pic_path + country  + "各支局4G用户数.png",format='png', dpi=200)  
        plt.close()

        # =============================================================================
        # 各支局4G用户数环比变化图
        # =============================================================================
        y1 = df_country_pivot['4G用户数'][df_country_pivot['week'] == week1 ].T.values
        y2 = df_country_pivot['4G用户数'][df_country_pivot['week'] == week2 ].T.values
        y3 =  [(b-a)/a for a, b in zip(y1,y2)]
        substation_list = df_country_pivot['支局'][df_country_pivot['week'] == week1 ].T.values
        plt.figure(figsize=(6, 4))
        x_substation = range(0,len(substation_list)) 
        plt.bar(x_substation,y3,color='b',width = 0.3,alpha=0.6,label='各支局4G用户数环比')
        for x,y in zip(x_substation,y3):
            plt.text(x, y*1.001, '%.2f%%' % (y*100), ha='center', va= 'bottom',fontsize=10)
        plt.xlabel(country+'各支局4G用户数环比变化')
        plt.xticks(range(0,len(substation_list)),substation_list)
        plt.ylabel('区县')
        plt.legend(loc='upper middle')
        plt.title(country+'各支局4G用户数环比变化')
        plt.savefig(pic_path + country  +"各支局4G用户数环比变化.png",format='png', dpi=200)  
        plt.close()
        
        # =============================================================================
        # 画各支局4G流量图
        # =============================================================================
        y1 = df_country_pivot['4G流量'][df_country_pivot['week'] == week1 ].T.values
        y2 = df_country_pivot['4G流量'][df_country_pivot['week'] == week2 ].T.values
        substation_list = df_country_pivot['支局'][df_country_pivot['week'] == week1 ].T.values
        plt.figure(figsize=(6, 4))
        x_substation = range(0,len(substation_list)) 
        x_substation1 = [i+0.35 for i in x_substation] 
        plt.bar(x_substation,y1,color='g',width = 0.3,alpha=0.6,label='上周4G流量')
        plt.bar(x_substation1,y2,color='b',width = 0.3,alpha=0.6,label='本周4G流量')
        for x,y in zip(x_substation,y1):
            plt.text(x, y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=8)
        for x,y in zip(x_substation1,y2 ):
            plt.text(x, y*1.001, '%d' % y, ha='center', va= 'bottom',fontsize=8)
        plt.xlabel(country+'各支局4G流量')
        plt.xticks(range(0,len(substation_list)),substation_list)
        plt.ylabel('支局')
        plt.legend(loc='upper middle')
        plt.title(country+'各支局4G流量')
        plt.savefig(pic_path + country  + "各支局4G流量.png",format='png', dpi=200)  
        plt.close()

        # =============================================================================
        # 各支局支局4G流量环比变化图
        # =============================================================================
        y1 = df_country_pivot['4G流量'][df_country_pivot['week'] == week1 ].T.values
        y2 = df_country_pivot['4G流量'][df_country_pivot['week'] == week2 ].T.values
        y3 =  [(b-a)/a for a, b in zip(y1,y2)]
        substation_list = df_country_pivot['支局'][df_country_pivot['week'] == week1 ].T.values
        plt.figure(figsize=(6, 4))
        x_substation = range(0,len(substation_list)) 
        plt.bar(x_substation,y3,color='b',width = 0.3,alpha=0.6,label='各支局4G流量环比变化')
        for x,y in zip(x_substation,y3):
            plt.text(x, y*1.001, '%.2f%%' % (y*100), ha='center', va= 'bottom',fontsize=10)
        plt.xlabel(country+'各支局4G流量环比')
        plt.xticks(range(0,len(substation_list)),substation_list)
        plt.ylabel('区县')
        plt.legend(loc='upper middle')
        plt.title(country+'各支局4G流量环比')
        plt.savefig(pic_path + country  +"各支局4G流量环比变化.png",format='png', dpi=200)  
        plt.close()

        sheet.insert_image('A2' , pic_path + country  + "各支局4G基站数量.png")
        sheet.insert_image('A23', pic_path + country  + "各支局4G用户数.png")
        sheet.insert_image('K23', pic_path  + country + "各支局4G用户数环比变化.png")
        sheet.insert_image('A44', pic_path + country  + "各支局4G流量.png")
        sheet.insert_image('K44', pic_path + country  + "各支局4G流量环比变化.png")

# =============================================================================
# 按县划小到支局基站清单
# =============================================================================
for country in country_list :
    df_country = df_4G_ALL[(df_4G_ALL['区县'] == country)&(df_4G_ALL['week'] == week2)]
    substation_list = list(set(df_country['支局']))
    with  pd.ExcelWriter(out_path + country + '.xlsx')  as writer:  #输出到excel
        df_country = df_country.sort_values(by='总流量(GB)',ascending = True)
        df_country = df_country.reset_index()
        del df_country['index']
        df_traffic_low = df_country.loc[0:20,['网元名称', '厂家','总流量(GB)']]
        df_traffic_low['TOP类型'] ='4G低流量基站'
        df_traffic_low.to_excel(writer, '4G低流量')
        
        df_country = df_country.sort_values(by='总流量(GB)',ascending = False)
        df_country = df_country.reset_index()
        del df_country['index']
        df_traffic_high = df_country.loc[0:20,['网元名称', '厂家','总流量(GB)']]
        df_traffic_high['TOP类型'] ='4G高流量基站'
        df_traffic_high.to_excel(writer, '4G高流量')
        
        df_country = df_country.sort_values(by='RRC连接用户数',ascending = True)            
        df_country = df_country.reset_index()
        del df_country['index']
        df_user_low = df_country.loc[0:20,['网元名称', '厂家','RRC连接用户数']]
        df_user_low['TOP类型'] = '4G低用户数基站'
        df_user_low.to_excel(writer, '4G低用户数')
        
        df_country = df_country.sort_values(by='RRC连接用户数',ascending = False)            
        df_country = df_country.reset_index()
        del df_country['index']
        df_user_high = df_country.loc[0:20,['网元名称', '厂家','RRC连接用户数']]
        df_user_high['TOP类型'] = '4G高用户数基站'
        df_user_high.to_excel(writer, '4G高用户数')
        
        for substation in substation_list :
            df_substation = df_country[(df_country['支局'] == substation)&(df_country['week'] == week2)]
            df_substation = df_substation[['week','网元名称', '厂家','RRC连接用户数','总流量(GB)']]
            df_substation.rename(columns={'week':'周',
                                          'RRC连接用户数':'4G用户数',
                                          '总流量(GB)':'4G流量(GB)'},inplace =True)
            df_substation.to_excel(writer, substation)             
            
#with  pd.ExcelWriter(out_path + 'df_4G_ALL.xlsx')  as writer:  #输出到excel
#    df_4G_ALL.to_excel(writer, 'df_4G_ALL') 
        
        
        




