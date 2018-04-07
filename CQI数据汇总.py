# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 13:21:05 2018

@author: Administrator
"""
import pandas as pd 
import os

path = r'D:\CQI专项' + '\\'
outpath = r'D:\cqi结果' + '\\'
files = os.listdir(path)
df_result = pd.DataFrame(columns=[])


for file in files:
    df_tmp = pd.read_csv(path + file ,engine= 'python',encoding='gbk')
    df_result = df_result.append(df_tmp)
    
df_result['CQI1-6求和'] = df_result['12.2 CQI0上报数量(次)'] +  df_result['12.2 CQI1上报数量(次)'] +  df_result['12.2 CQI2上报数量(次)'] +  df_result['12.2 CQI3上报数量(次)'] +  df_result['12.2 CQI4上报数量(次)'] +  df_result['12.2 CQI5上报数量(次)']+  df_result['12.2 CQI6上报数量(次)'] 
df_result['优良率'] =  1-(df_result['CQI1-6求和']/df_result['12.2 CQI上报总数量(次)'])
        
df_eric = df_result[(df_result['厂家']=='爱立信')&(df_result['优良率']>0.90)]    
#df_eric = df_eric.groupby(by='小区名称',as_index=False)[['基站名称','12.2 CQI上报总数量(次)','CQI1-6求和','优良率']].max()

df_zte = df_result[(df_result['厂家']=='中兴')&(df_result['优良率']>0.90)]    
df_zte_worse = df_result[(df_result['厂家']=='中兴')&(df_result['优良率']<0.80)]    
df_zte_worse = df_zte_worse.groupby(by='小区名称',as_index=False)[['基站名称','12.2 CQI上报总数量(次)','CQI1-6求和']].sum()
df_zte_worse['12.2 CQI上报总数量(次)'] = df_zte_worse['12.2 CQI上报总数量(次)']/18
df_zte_worse['CQI1-6求和'] = df_zte_worse['CQI1-6求和']/18

df_sum = df_result[(df_result['时间']=='2018-03-28 22:00:00')]    


with pd.ExcelWriter(outpath + 'eric.xls') as writer: #不用保存和退出，系统自动会完成
    df_eric.to_excel(writer,'爱立信优良扇区') 
with pd.ExcelWriter(outpath + '全网.xls') as writer: #不用保存和退出，系统自动会完成
    df_sum.to_excel(writer,'全网指标') 
with pd.ExcelWriter(outpath + '中兴质差.xls') as writer: #不用保存和退出，系统自动会完成
    df_zte_worse.to_excel(writer,'中兴质差') 
    df_zte.to_excel(writer,'中兴优良扇区') 


