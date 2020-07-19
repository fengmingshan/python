# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 15:27:13 2019

@author: Administrator
"""

import pandas as pd
import os

# 申请权限
# APPLY CMRIGHT:SYSTEM=275;

# 删除DO载频邻区指令
# DEL DO_CARRIER:POS="275"-"0"-"2";


# =============================================================================
# 设置环境变量
# =============================================================================
path = r'D:\_python小程序\删除DO载频'
os.chdir(path)

if not os.path.exists('./指令输出'):
    os.mkdir('./指令输出')

file_name = '曲靖BSS2_CM_载频无线参数表(DO).xls'
del_file = '会泽退网小区.xlsx'
df_delete = pd.read_excel(del_file)
df_delete.drop_duplicates('cell_ind', keep ='first', inplace = True)

df_carrier_info = pd.read_excel(file_name,skiprows= 1)
df_carrier_info['cell_ind'] = df_carrier_info['system'].map(str)  + '_' + df_carrier_info['cellid'].map(str)
df_carrier_info = df_carrier_info[df_carrier_info['cell_ind'].isin(df_delete['cell_ind'])]
df_carrier_info.reset_index(drop = True,inplace =True)
# 参数修改脚本
with open('./指令输出/'+'删除DO载波.txt', 'w') as f:
    for i in range(0, len(df_carrier_info), 1):
        line = r'DEL DO_CARRIER:POS="{system}"-"{cellid}"-"{carrierid}";'.format(
            system = df_carrier_info.loc[i, 'system'],
            cellid = df_carrier_info.loc[i, 'cellid'],
            carrierid = df_carrier_info.loc[i, 'carrierid'])
        f.write(line+'\n')

# 申请网元权限脚本
df_system = df_carrier_info[['system','cellid']]
df_system.drop_duplicates('system', keep ='first', inplace = True)
df_system.reset_index(inplace = True)
with open('./指令输出/' + '申请权限.txt','w') as f:
    for i in range(0, len(df_system), 1):
        line = 'APPLY CMRIGHT:SYSTEM={system};'.format(
            system = df_system.loc[i, 'system'])
        f.write(line+'\n')

