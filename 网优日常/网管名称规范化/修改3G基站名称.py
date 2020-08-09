# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 11:38:15 2020

@author: Administrator
"""

import pandas as pd
import os

path =r'D:\_python小程序\网管名称规范化'
os.chdir(path)

files =os.listdir()
files

df_3g_bts = pd.read_excel('3g_change_name.xlsx',sheet_name = 'bts_name')
df_3g_bts.columns

df_bsc1 = df_3g_bts[df_3g_bts['BSC'] == 'BSC1']
df_bsc1.reset_index(drop = True,inplace = True)

df_bsc2 = df_3g_bts[df_3g_bts['BSC'] == 'BSC2']
df_bsc2.reset_index(drop = True,inplace = True)

apply_rights_cmd = []
change_name_cmd = []
for i in range(0,len(df_bsc1)):
    apply_right_line ='APPLY CMRIGHT:SYSTEM={bts};'.format(
            bts = df_bsc1.loc[i,'system'],
            )

    change_line = 'SET BTS INFORMATION:POS="{bts}",ALIAS_B="{name}";'.format(
        bts = df_bsc1.loc[i,'system'],
        name = df_bsc1.loc[i,'new_name'],
        )

    apply_rights_cmd.append(apply_right_line)
    change_name_cmd.append(change_line)

apply_rights_cmd = list(set(apply_rights_cmd))
change_name_cmd = list(set(change_name_cmd))


with open('./脚本输出/修改3G基站名称_bsc1.txt','w') as f:
    for line in apply_rights_cmd:
         f.writelines(line+ '\n')

    f.writelines('\n')

    for line in change_name_cmd:
         f.writelines(line+ '\n')



apply_rights_cmd = []
change_name_cmd = []
for i in range(0,len(df_bsc2)):
    apply_right_line ='APPLY CMRIGHT:SYSTEM={bts};'.format(
            bts = df_bsc2.loc[i,'system'],
            )

    change_line = 'SET BTS INFORMATION:POS="{bts}",ALIAS_B="{name}";'.format(
        bts = df_bsc2.loc[i,'system'],
        name = df_bsc2.loc[i,'new_name'],
        )

    apply_rights_cmd.append(apply_right_line)
    change_name_cmd.append(change_line)

apply_rights_cmd = list(set(apply_rights_cmd))
change_name_cmd = list(set(change_name_cmd))


with open('./脚本输出/修改3G基站名称_bsc2.txt','w') as f:
    for line in apply_rights_cmd:
         f.writelines(line+ '\n')

    f.writelines('\n')

    for line in change_name_cmd:
         f.writelines(line+ '\n')
