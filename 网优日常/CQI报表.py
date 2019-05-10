# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 11:17:24 2018

@author: Administrator
"""

import pandas as pd 
import os
import numpy as np
from datetime import datetime 
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

current_date = str(datetime.now()).split('.')[0].split(' ')[0]

data_path = r'D:\CQI报表\原始数据' + '\\'
out_path = r'D:\CQI报表\脚本输出' + '\\'
pic_path = r'D:\CQI报表\pic' + '\\'
path = r'D:\CQI报表' + '\\'

config_files = [x for x in os.listdir(path) if 'PhyChannel' in x ]
df_PhyChannel = pd.DataFrame()
for file in config_files :
    df_tmp = pd.read_excel(path + file ,encoding='utf-8') 
    df_tmp = df_tmp.drop([0,1,2])
    df_tmp['OMMB'] = file.split('_')[1][0:5]
    df_PhyChannel = df_PhyChannel.append(df_tmp)
df_PhyChannel = df_PhyChannel[['OMMB','MOI','SubNetwork','MEID','description','cqiRptPeriod','cqiRptChNum',]]
df_PhyChannel['MOI'] = df_PhyChannel['MOI'].map(lambda x:x.replace('ConfigSet=0,',''))
df_PhyChannel['description'] = df_PhyChannel['description'].map(lambda x:x.split('=')[1])
df_PhyChannel['description'] = df_PhyChannel['MEID'] + '_' + df_PhyChannel['description']
df_PhyChannel.rename(columns={'description':'小区编码'},inplace =True)

files = os.listdir(data_path)
df_yunnan = pd.DataFrame()
for file in files:
    df_tmp = pd.read_csv(data_path + file ,engine= 'python',encoding='gbk')
    df_yunnan = df_yunnan.append(df_tmp)

df_yunnan_pivot = pd.pivot_table(df_yunnan, index=['区域'], 
                                  values =['CQI上报总次数' ,'CQI大于等于7次数'], 
                                  aggfunc = {'CQI上报总次数':np.sum,'CQI大于等于7次数':np.sum})     
df_yunnan_pivot['CQI优良比'] = df_yunnan_pivot['CQI大于等于7次数'] / df_yunnan_pivot['CQI上报总次数'] 
df_yunnan_pivot = df_yunnan_pivot.sort_values(by='CQI优良比',ascending = False)
df_yunnan_pivot = df_yunnan_pivot.reset_index()          


df_qujing = df_yunnan[(df_yunnan['区域'] == '曲靖市')]
df_qujing_pivot = pd.pivot_table(df_qujing, index=['日期'], 
                                          values =['CQI上报总次数' ,'CQI大于等于7次数'], 
                                          aggfunc = {'CQI上报总次数':np.sum,'CQI大于等于7次数':np.sum})     
df_qujing_pivot = df_qujing_pivot.reset_index()          
df_qujing_pivot.rename(columns={'CQI上报总次数':'CQI全天总数','CQI大于等于7次数':'CQI大于等于7全天总数'},inplace =True)
df_qujing_pivot['CQI优良比_全市'] =  df_qujing_pivot['CQI大于等于7全天总数']/df_qujing_pivot['CQI全天总数']


df_qujing_zte  = df_yunnan[(df_yunnan['区域'] == '曲靖市')&(df_yunnan['厂家'] == '中兴')]
df_zte_day = pd.pivot_table(df_qujing_zte, index=['日期','区域'], 
                                               values =['CQI上报总次数','CQI大于等于7次数' ], 
                                               aggfunc = {'CQI上报总次数':np.sum,'CQI大于等于7次数':np.sum})     
df_zte_day = df_zte_day.reset_index()    
df_zte_day['CQI优良比'] =  df_zte_day['CQI大于等于7次数']/df_zte_day['CQI上报总次数']

df_qujing_eric  = df_yunnan[(df_yunnan['区域'] == '曲靖市')&(df_yunnan['厂家'] == '爱立信')]
df_eric_day = pd.pivot_table(df_qujing_eric, index=['日期','区域'], 
                                               values =['CQI上报总次数','CQI大于等于7次数' ], 
                                               aggfunc = {'CQI上报总次数':np.sum,'CQI大于等于7次数':np.sum})     
df_eric_day = df_eric_day.reset_index()    
df_eric_day['CQI优良比'] =  df_eric_day['CQI大于等于7次数']/df_eric_day['CQI上报总次数']

    
# =============================================================================
# 质优小区
# =============================================================================
df_zte_good = df_qujing_zte[df_qujing_zte['CQI大于等于7比例']>=92]   
df_zte_good.rename(columns={'厂家':'小区编码','CQI大于等于7比例':'CQI优良比'},inplace =True)
df_zte_good['小区编码'] = df_zte_good['小区名'].map(lambda x:str(x).split('R')[0][:-1])
df_zte_good = pd.merge(df_zte_good,df_PhyChannel,how='left',on='小区编码')
df_zte_good = pd.merge(df_zte_good,df_qujing_pivot,how='left',on='日期')
df_zte_good = df_zte_good[['区域','日期','小区名','小区编码','是否800M设备','CQI上报总次数',\
                           'CQI大于等于7次数','CQI优良比','OMMB','MOI','SubNetwork','MEID',\
                           'cqiRptPeriod','cqiRptChNum','CQI全天总数','CQI大于等于7全天总数']]
df_zte_good['权重'] = df_zte_good['CQI上报总次数']/df_zte_good['CQI全天总数']
date_now = df_zte_good.loc[len(df_zte_good)-1,'日期']
df_zte_good = df_zte_good[df_zte_good['日期'] == date_now]
df_zte_good = df_zte_good.sort_values(by='权重',ascending = False) # 按权重降序排列  

# =============================================================================
# 正常小区
# =============================================================================
df_zte_normal = df_qujing_zte[(df_qujing_zte['CQI大于等于7比例']>91)&(df_qujing_zte['CQI大于等于7比例']<92)]   
df_zte_normal.rename(columns={'厂家':'小区编码','CQI大于等于7比例':'CQI优良比'},inplace =True)
df_zte_normal['小区编码'] = df_zte_normal['小区名'].map(lambda x:str(x).split('R')[0][:-1])
df_zte_normal = pd.merge(df_zte_normal,df_PhyChannel,how='left',on='小区编码')
df_zte_normal = pd.merge(df_zte_normal,df_qujing_pivot,how='left',on='日期')
df_zte_normal = df_zte_normal[['区域','日期','小区名','小区编码','是否800M设备','CQI上报总次数',\
                           'CQI大于等于7次数','CQI优良比','OMMB','MOI','SubNetwork','MEID',\
                           'cqiRptPeriod','cqiRptChNum','CQI全天总数','CQI大于等于7全天总数']]
df_zte_normal['权重'] = df_zte_normal['CQI上报总次数']/df_zte_normal['CQI全天总数']
date_now = df_zte_normal.loc[len(df_zte_normal)-1,'日期']
df_zte_normal = df_zte_normal[df_zte_normal['日期'] == date_now]
df_zte_normal = df_zte_normal.sort_values(by='权重',ascending = False) # 按权重降序排列  


# =============================================================================
# 质差小区
# =============================================================================
df_zte_worse = df_qujing_zte[df_qujing_zte['CQI大于等于7比例']<=91]  
df_zte_worse.rename(columns={'厂家':'小区编码','CQI大于等于7比例':'CQI优良比'},inplace =True)
df_zte_worse['小区编码'] = df_zte_worse['小区名'].map(lambda x:str(x).split('R')[0][:-1])
df_zte_worse = pd.merge(df_zte_worse,df_PhyChannel,how='left',on='小区编码')
df_zte_worse = pd.merge(df_zte_worse,df_qujing_pivot,how='left',on='日期')
df_zte_worse = df_zte_worse[['区域','日期','小区名','小区编码','是否800M设备','CQI上报总次数',\
                           'CQI大于等于7次数','CQI优良比','OMMB','MOI','SubNetwork','MEID',\
                           'cqiRptPeriod','cqiRptChNum','CQI全天总数','CQI大于等于7全天总数']]
df_zte_worse['权重'] = df_zte_worse['CQI上报总次数']/df_zte_worse['CQI全天总数']
date_now = df_zte_worse.loc[len(df_zte_worse)-1,'日期']
df_zte_worse = df_zte_worse[df_zte_worse['日期'] == date_now]
df_zte_worse = df_zte_worse.sort_values(by='权重',ascending = False) # 按权重降序排列  

# =============================================================================
# 画全省CQI优良率
# =============================================================================
y = df_yunnan_pivot['CQI优良比'].map(lambda x:x*100).T.values
city_list = df_yunnan_pivot['区域'].T.values
plt.figure(figsize=(12, 4))
x_city = range(0,len(city_list)) 
plt.bar(x_city,y,color='b',width = 0.3,alpha=0.6,label='全省CQI优良比')
for x,y in zip(x_city,y):
    plt.text(x, y*1.001,'%.2f%%' % y, ha='center', va= 'bottom',fontsize=8)
plt.xlabel('全省CQI优良比')
plt.xticks(range(0,len(city_list)),city_list)
plt.ylabel('城市')
plt.legend(loc='center right')
plt.title('全省CQI优良比')
plt.savefig(pic_path + "全省CQI优良比.png",format='png', dpi=200) 
plt.close()

# =============================================================================
# 画全市CQI优良率
# =============================================================================
y1 = df_qujing_pivot['CQI优良比_全市'].map(lambda x:x*100).T.values
df_qujing_pivot['日期'] = df_qujing_pivot['日期'].map(lambda x:x[5:])
x1 = df_qujing_pivot['日期'].T.values
plt.figure(figsize=(12, 4))
plt.xticks(range(len(x1)), x1,fontsize=8)
plt.plot(range(len(x1)),y1,label='CQI优良比',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=6) 
for a,b in zip(range(len(x1)),y1):
    plt.text(a,b*1.001,  '%.2f%%' % b, ha='center', va= 'bottom',fontsize=9)
plt.xlabel('日期')
plt.ylabel('全市CQI优良比')
plt.title('全市CQI优良比变化情况')
plt.legend(loc='center right')
plt.savefig(pic_path + "全市CQI优良比.png",format='png', dpi=400)  
plt.close()

# =============================================================================
# 画中兴CQI优良率
# =============================================================================
y1 = df_zte_day['CQI优良比'].map(lambda x:x*100).T.values
df_zte_day['日期'] = df_zte_day['日期'].map(lambda x:x[5:])
x1 = df_zte_day['日期'].T.values
plt.figure(figsize=(12, 4))
plt.xticks(range(len(x1)), x1,fontsize=8)
plt.plot(range(len(x1)),y1,label='CQI优良比',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=6) 
for a,b in zip(range(len(x1)),y1):
    plt.text(a,b*1.001,  '%.2f%%' % b, ha='center', va= 'bottom',fontsize=9)
plt.xlabel('日期')
plt.ylabel('中兴CQI优良比')
plt.title('中兴CQI优良比变化情况')
plt.legend(loc='center right')
plt.savefig(pic_path + "中兴CQI优良比.png",format='png', dpi=400)  
plt.close()

# =============================================================================
# 画爱立信CQI优良率
# =============================================================================
y1 = df_eric_day['CQI优良比'].map(lambda x:x*100).T.values
df_eric_day['日期'] = df_eric_day['日期'].map(lambda x:x[5:])
x1 = df_eric_day['日期'].T.values
plt.figure(figsize=(12, 4))
plt.xticks(range(len(x1)), x1,fontsize=8)
plt.plot(range(len(x1)),y1,label='CQI优良比',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=6) 
for a,b in zip(range(len(x1)),y1):
    plt.text(a,b*1.001,  '%.2f%%' % b, ha='center', va= 'bottom',fontsize=9)
plt.xlabel('日期')
plt.ylabel('爱立信CQI优良比')
plt.title('爱立信CQI优良比变化情况')
plt.legend(loc='center right')
plt.savefig(pic_path + "爱立信CQI优良比.png",format='png', dpi=400)  
plt.close()




# =============================================================================
# 生成修改指令
# =============================================================================
for x in ['OMMB1','OMMB2','OMMB3']:
    df_good_ommb = df_zte_good[(df_zte_good['cqiRptChNum'] != '6;0;0')&(df_zte_good['OMMB'] == x)]
    df_normal_ommb = df_zte_normal[(df_zte_normal['cqiRptChNum'] != '1;0;5')&(df_zte_normal['OMMB'] == x)]
    df_worse_ommb = df_zte_worse[(df_zte_worse['cqiRptChNum'] != '1;0;5')&(df_zte_worse['OMMB'] == x)]
    df_good_ommb = df_good_ommb.reset_index()
    df_normal_ommb = df_normal_ommb.reset_index()
    df_worse_ommb = df_worse_ommb.reset_index()

    df_good_eNodeB = df_good_ommb.drop_duplicated('MEID',keep='first')
    with open(out_path + 'apply_right_' + x +'.txt','a') as f:
        for i in range(0,len(df_good_eNodeB),1):
            line = r'APPLY MUTEXRIGHT:SUBNET="{0}",NE="{1}";'\
            .format(df_good_ommb.loc[i,'SubNetwork'],
                    df_good_ommb.loc[i,'MEID'],
    )
            f.write(line+'\n')         
    
    df_normal_eNodeB = df_normal_ommb.drop_duplicated('MEID',keep='first')    
    with open(out_path + 'apply_right_'+ x + '.txt','a') as f:
        for i in range(0,len(df_normal_ommb),1):
            line = r'APPLY MUTEXRIGHT:SUBNET="{0}",NE="{1}";'\
            .format(df_normal_ommb.loc[i,'SubNetwork'],
                    df_normal_ommb.loc[i,'MEID'],
    )
            f.write(line+'\n')         

    df_worse_eNodeB = df_worse_ommb.drop_duplicated('MEID',keep='first')        
    with open(out_path + 'apply_right_' + x + '.txt','a') as f:
        for i in range(0,len(df_worse_ommb),1):
            line = r'APPLY MUTEXRIGHT:SUBNET="{0}",NE="{1}";'\
            .format(df_worse_ommb.loc[i,'SubNetwork'],
                    df_worse_ommb.loc[i,'MEID'],
    )
            f.write(line+'\n')         
    
    with open(out_path + x + '_modify_CQI.txt','a') as f:
        for i in range(0,len(df_good_ommb),1):
            line = r'UPDATE:MOC="PhyChannel",MOI="{0}",ATTRIBUTES="cqiRptPeriod=\"0;3;5\",cqiRptChNum=\"6;0;0\"",EXTENDS="";'\
            .format(df_good_ommb.loc[i,'MOI'])
            f.write(line+'\n') 
            
    with open(out_path + x + '_modify_CQI.txt','a') as f:
        for i in range(0,len(df_normal_ommb),1):
            line = r'UPDATE:MOC="PhyChannel",MOI="{0}",ATTRIBUTES="cqiRptPeriod=\"1;3;5\",cqiRptChNum=\"1;0;5\"",EXTENDS="";'\
            .format(df_normal_ommb.loc[i,'MOI'])
            f.write(line+'\n') 
    
    
    with open(out_path + x + '_modify_CQI.txt','a') as f:
        for i in range(0,len(df_worse_ommb),1):
            line = r'UPDATE:MOC="PhyChannel",MOI="{0}",ATTRIBUTES="cqiRptPeriod=\"1;3;5\",cqiRptChNum=\"1;0;5\"",EXTENDS="";'\
            .format(df_worse_ommb.loc[i,'MOI'])
            f.write(line+'\n') 

# =============================================================================
# 输出报表
# =============================================================================

with  pd.ExcelWriter(out_path + '曲靖CQI优良率' + current_date + '.xlsx')  as writer:  #输出到excel
    book = writer.book 
    sheet = book.add_worksheet('本月MR指标')
    sheet.insert_image('A2' , pic_path + "全省CQI优良比.png")
    sheet.insert_image('A23', pic_path + "全市CQI优良比.png")
    sheet.insert_image('A44', pic_path + "中兴CQI优良比.png")
    sheet.insert_image('A65', pic_path + "爱立信CQI优良比.png")
    df_zte_good.to_excel(writer,'质优小区',index=False) 
    df_zte_normal.to_excel(writer,'正常小区',index=False) 
    df_zte_worse.to_excel(writer,'质差小区',index=False) 


