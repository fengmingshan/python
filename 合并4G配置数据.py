# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 12:50:42 2018

@author: Administrator
"""

import pandas as pd
import os

data_path = r'D:\_python小程序\合并表格'
os.chdir(data_path)
files =  os.listdir()

df_content = pd.DataFrame()
for file in files:
    df_tmp  = pd.read_excel('./'+ file , encoding = 'utf-8', sheet_name = 'ECellEquipmentFunctionNB' )
    df_tmp.drop([0,1,2],axis = 0,inplace =True)
    df_content = df_content.append(df_tmp)

with  pd.ExcelWriter('配置数据汇总.xlsx')  as writer:  #输出到excel
    df_content.to_excel(writer,'配置数据汇总',index=False)

help(pd.read_excel)