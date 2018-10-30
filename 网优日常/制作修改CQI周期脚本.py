# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 21:41:30 2018

@author: Administrator
"""
import pandas as pd


path = r'd:\制作修改参数脚本' + '\\'
bad_quality = '质差小区_2.xlsx'
good_quality = '质优小区_2.xlsx'

df_bad = pd.read_excel(path + bad_quality,encoding='utf-8')

with open(path + 'bad_quality_2.txt','w') as f:
    for i in range(0,len(df_bad),1):
        line = r'UPDATE:MOC="PhyChannel",MOI="SubNetwork={0},MEID={1},ENBFunctionFDD={2},EUtranCellFDD={3},PhyChannel=1",ATTRIBUTES="cqiRptPeriod=\"3;4;5\"",EXTENDS="";'\
        .format(df_bad.loc[i,'SubNetwork'],
                df_bad.loc[i,'MEID'],
                df_bad.loc[i,'ENBFunctionFDD'],
                df_bad.loc[i,'EUtranCellFDD']
)
        f.write(line+'\n') 

with open(path + 'apply_right_bad_2.txt','w') as f:
    for i in range(0,len(df_bad),1):
        line = r'APPLY MUTEXRIGHT:SUBNET="{0}",NE="{1}";'\
        .format(df_bad.loc[i,'SubNetwork'],
                df_bad.loc[i,'MEID'],
)
        f.write(line+'\n')         
        
        
df_good = pd.read_excel(path + good_quality,encoding='utf-8')

with open(path + 'good_quality_2.txt','w') as f:
    for i in range(0,len(df_good),1):
        line = r'UPDATE:MOC="PhyChannel",MOI="SubNetwork={0},MEID={1},ENBFunctionFDD={2},EUtranCellFDD={3},PhyChannel=1",ATTRIBUTES="cqiRptPeriod=\"1;2;3\"",EXTENDS="";'\
        .format(df_good.loc[i,'SubNetwork'],
                df_good.loc[i,'MEID'],
                df_good.loc[i,'ENBFunctionFDD'],
                df_good.loc[i,'EUtranCellFDD']
)
        f.write(line+'\n') 

with open(path + 'apply_right_good_2.txt','w') as f:
    for i in range(0,len(df_good),1):
        line = r'APPLY MUTEXRIGHT:SUBNET="{0}",NE="{1}";'\
        .format(df_good.loc[i,'SubNetwork'],
                df_good.loc[i,'MEID'],
)
        f.write(line+'\n')         


        