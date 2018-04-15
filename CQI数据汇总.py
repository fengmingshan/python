# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 13:21:05 2018

@author: Administrator
"""
import pandas as pd 
import os


path = r'd:\2018年工作\2018年4月CQI专项\原始数据' + '\\'
outpath = r'd:\2018年工作\2018年4月CQI专项' + '\\'
files = os.listdir(path)
df_result = pd.DataFrame(columns=[])


for file in files:
    df_tmp = pd.read_csv(path + file ,engine= 'python',encoding='gbk')
    df_result = df_result.append(df_tmp)
    
df_result['CQI1-6求和'] = df_result['12.2 CQI0上报数量(次)'] +  df_result['12.2 CQI1上报数量(次)'] +  df_result['12.2 CQI2上报数量(次)'] +  df_result['12.2 CQI3上报数量(次)'] +  df_result['12.2 CQI4上报数量(次)'] +  df_result['12.2 CQI5上报数量(次)']+  df_result['12.2 CQI6上报数量(次)'] 
df_result['优良率'] =  1-(df_result['CQI1-6求和']/df_result['12.2 CQI上报总数量(次)'])
        
df_eric = df_result[(df_result['厂家']=='爱立信')&(df_result['优良率']>0.88)]    
df_eric = df_eric.groupby(by='小区名称',as_index=False)[['基站名称','12.2 CQI上报总数量(次)','CQI1-6求和']].mean()  

df_zte_good = df_result[(df_result['厂家']=='中兴')&(df_result['优良率']>0.88)]    
df_zte_good = df_zte_good.groupby(by='小区名称',as_index=False)[['基站名称','12.2 CQI上报总数量(次)','CQI1-6求和']].mean()  
df_zte_good['优良率'] = 1 - df_zte_good['CQI1-6求和']/ df_zte_good['12.2 CQI上报总数量(次)']
df_zte_good.loc['合计'] = df_zte_good.apply(lambda x: x.sum()) 
df_zte_good['质差共享比重'] = ''
for i in range(0,len(df_zte_good)-1,1):
    df_zte_good.loc[i,'质差贡献比重'] = df_zte_good.loc[i,'CQI1-6求和']/df_zte_good.loc['合计','CQI1-6求和']
df_zte_good.loc['合计','小区名称'] = '合计'
df_zte_good.loc['合计','质差贡献比重'] = 0
df_zte_good = df_zte_good.sort_values(by='质差贡献比重',ascending = False) # 按质差贡献比重降序排列 

df_zte_worse = df_result[(df_result['厂家']=='中兴')&(df_result['优良率']<0.88)]    
df_zte_worse = df_zte_worse.groupby(by='小区名称',as_index=False)[['基站名称','12.2 CQI上报总数量(次)','CQI1-6求和']].mean()  
df_zte_worse['优良率'] = 1 - df_zte_worse['CQI1-6求和']/ df_zte_worse['12.2 CQI上报总数量(次)']
df_zte_worse.loc['合计'] = df_zte_worse.apply(lambda x: x.sum()) 
df_zte_worse['质差共享比重'] = ''
for i in range(0,len(df_zte_worse)-1,1):
    df_zte_worse.loc[i,'质差贡献比重'] = df_zte_worse.loc[i,'CQI1-6求和']/df_zte_worse.loc['合计','CQI1-6求和']
df_zte_worse.loc['合计','小区名称'] = '合计'
df_zte_worse.loc['合计','质差贡献比重'] = 0
df_zte_worse = df_zte_worse.sort_values(by='质差贡献比重',ascending = False) # 按质差贡献比重降序排列


#with pd.ExcelWriter(outpath + 'eric.xlsx') as writer: #不用保存和退出，系统自动会完成
    #df_eric.to_excel(writer,'爱立信优良扇区') 
with pd.ExcelWriter(outpath + '全网.xlsx') as writer: #不用保存和退出，系统自动会完成
    df_result.to_excel(writer,'全网指标') 
with pd.ExcelWriter(outpath + '中兴质差.xlsx') as writer: #不用保存和退出，系统自动会完成
    df_zte_worse.to_excel(writer,'中兴质差') 
    df_zte_good.to_excel(writer,'中兴优良扇区') 


