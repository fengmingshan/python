# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 14:28:13 2018
电压日报表排序
@author: Administrator
"""
import pandas as pd
import os 

report_path = r'd:\test' + '\\'
all_files = os.listdir(report_path)
for file in all_files:
    df_report = pd.read_excel(report_path + file,encoding='utf-8') 
    cols = ['eNodeB','网元名称']
    for i in range(1,int(len(df_report.columns)/2),1):
        cols.append('时间_' + str(i))
        cols.append('电压_' + str(i))
    df_report = df_report[cols]

with pd.ExcelWriter(report_path + file) as writer:
    df_report.to_excel(writer,file.split('.')[0])