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
file_relation_list = []
file_extcell_list = []
for file in files:
    df = pd.ExcelFile(file)
    relation_sheets = [x for x in df.sheet_names if 'EUtranRelation' in x]
    extcell_sheets = [x for x in df.sheet_names if 'ExternalEUtranCellFDD' in x]
    
    relation_list = []
    for sheet in relation_sheets:
        df_tmp = pd.read_excel(file,sheet_name = sheet,header= 4)
        neighbor_list.append(df_tmp)
        
    extcell_list = []
    for sheet in extcell_sheets:
        df_tmp = pd.read_excel(file,sheet_name = sheet,header= 4)
        extcell_list.append(df_tmp)
        
    df_relation_all = pd.concat(relation_list,axis = 0)
    df_extcell_all = pd.concat(extcell_list,axis = 0)
    file_relation_list.append(df_relation_all)
    file_extcell_list.append(df_extcell_all)
    
df_rela = pd.concat(file_relation_list,axis =0)
df_ext = pd.concat(file_extcell_list,axis =0)

df_nei_simp = df[['MEID','CellId','eNBId','NCellId']]

with pd.ExcelWriter('./邻接关系合并.xlsx') as f:
    df_rela.to_excel(f,'邻区合并',index =False)

with pd.ExcelWriter('./外部邻区.xlsx') as f:
    df_ext.to_excel(f,'外部邻区',index =False)


with pd.ExcelWriter('./邻接关系_简.xlsx') as f:
    df_nei_simp.to_excel(f,'邻区合并',index =False)