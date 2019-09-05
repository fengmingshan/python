# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 15:27:13 2019

@author: Administrator
"""

import pandas as pd
import os

# 修改小区邻区指令
# APPLY CMRIGHT:SYSTEM=102;

# ADD 1X_LINKCELL_L:POS="1"-"0"-"21",NCELLSYSTEM=1,NCELL=1,ISEACHOTHER=0;
# DEL 1X_LINKCELL:POS="1"-"0"-"24";

# 修改载频邻区指令
# ADD 1X_NGHBRLIST_L:POS="1"-"0"-"0"-"32",NCELLSYSTEM=,NCELL=,NGHBR_CONFIG=0,SEARCH_PRIORITY=0,ACCESS_ENTRY_HO=Disable,FREQ_INCL=NOT_INC,ACCESS_HO_ALLOWED=Disable,TIMING_INCL=NOT_INC,NGHBR_TX_OFFSET=0,NGHBR_TX_DURATION=3,NGHBR_TX_PERIOD=0,ADD_PILOT_REC_INCL=NOT_INC,NGHBR_PILOT_REC_TYPE=0,SRCH_OFFSET_NGHBR=0;
# DEL 1X_NGHBRLIST:POS="1"-"0"-"0"-"21",ISEACHOTHER=NO;

# 修改载频功率脚本

# =============================================================================
# 设置环境变量
# =============================================================================
data_path = 'd:/test/'
out_path = r'd:/test/指令输出/'

if not os.path.exists(data_path):
    os.mkdir(data_path)
if not os.path.exists(out_path):
    os.mkdir(out_path)

os.chdir(data_path)

file_name = '载频参数表.xlsx'

df_carrier_info = pd.read_excel(file_name)

with open(out_path + '修改DO载频功率.txt', 'w') as f:
    for i in range(0, len(df_carrier_info), 1):
        line = r'SET DO_CARRIERSTATE:POS="{system}"-"{cellid}"-"{carrierid}",FORWARDTRANSMITPOWER=50;'\
        .format(system = df_carrier_info.loc[i, 'system'],
             cellid = df_carrier_info.loc[i, 'cellid'],
             carrierid = df_carrier_info.loc[i, 'carrierid'])
        f.write(line+'\n')
