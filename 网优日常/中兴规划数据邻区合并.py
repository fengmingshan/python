# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 17:40:50 2020

@author: Administrator
"""

import pandas as pd
import os

work_path = 'D:/Test/邻区'
os.chdir(work_path)
files =os.listdir('./')
file_list = []
for file in files:
    df = pd.ExcelFile(file)
    nei_sheets = [x for x in df.sheet_names if 'EUtranRelation' in x]
    df_list = []
    for sheet in nei_sheets:
        df_tmp = pd.read_excel(file,sheet_name = sheet)
        df_tmp.drop([0,1,2,3],axis =0)
        df_list.append(df_tmp)
    df_tmp_all = pd.concat(df_list,axis = 0)
    file_list.append(df_tmp_all)
df = pd.concat(file_list,axis =0)

df2 = df[['MEID','CellId','eNBId','NCellId']]
with pd.ExcelWriter('./邻区合并.xlsx') as f:
    df.to_excel(f,'邻区合并',index =False)

with pd.ExcelWriter('./邻区合并_简.xlsx') as f:
    df2.to_excel(f,'邻区合并',index =False)