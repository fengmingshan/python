# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 21:41:30 2018

@author: Administrator
"""
import pandas as pd


data_path = r'd:\制作修改参数脚本' + '\\'
cell_info = '质差小区_2.xlsx'

df_cell = pd.read_excel(data_path + bad_quality,encoding='utf-8')

with open(path + 'bad_quality_2.txt','w') as f:
    for i in range(0,len(df_bad),1):
        line = r'UPDATE:MOC="PhyChannel",MOI="SubNetwork={0},MEID={1},ENBFunctionFDD={2},EUtranCellFDD={3},PhyChannel=1",ATTRIBUTES="cqiRptPeriod=\"3;4;5\"",EXTENDS="";'\
        .format(df_bad.loc[i,'SubNetwork'],
                df_bad.loc[i,'MEID'],
                df_bad.loc[i,'ENBFunctionFDD'],
                df_bad.loc[i,'EUtranCellFDD']
)
        f.write(line+'\n') 


        