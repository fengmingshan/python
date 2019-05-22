# -*- coding: utf-8 -*-
"""
Created on Wed May 22 11:32:01 2019

@author: Administrator
"""

import pandas as pd

data_path = r'd:\_爱立信全网邻区核查' + '\\'
file = r'd:\_爱立信全网邻区核查\PARA_ERBS_371.csv'

df_eric = pd.read_csv(file,engine = 'python')

df_result = pd.DataFrame()
df_result['ManagedElement'] = df_eric['NE']
df_result['eNodeB'] = df_eric['NE']
df_result['CELL'] = df_eric['CELL']

df_result['Neighbor_Freq'] = df_eric['MO'].map(lambda x:x.split(';')[6].replace('EUtranFreqRelation=',''))
df_result['Neighbor_Index'] = df_eric['MO'].map(lambda x:x.split(';')[7].replace('EUtranCellRelation=46011-',''))
df_result['Ncell_name'] = df_eric['MO'].map(lambda x:x.split(';')[7].replace('EUtranCellRelation=46011-',''))

with pd.ExcelWriter(data_path + '爱立信全网邻区输出.xlsx') as writer: #不用保存和退出，系统自动会完成
    df_eric.to_excel(writer,'Sheet1',index =False)


