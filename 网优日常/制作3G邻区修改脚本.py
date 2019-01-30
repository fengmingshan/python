# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 15:27:13 2019

@author: Administrator
"""

import pandas as pd 
import os

# 修改小区邻区指令
# ADD 1X_LINKCELL_L:POS="1"-"0"-"21",NCELLSYSTEM=1,NCELL=1,ISEACHOTHER=0;
# DEL 1X_LINKCELL:POS="1"-"0"-"24";

# 修改载频邻区指令
# SET 1X_NGHBRLIST:POS="1"-"0"-"0"-"21";
# DEL 1X_NGHBRLIST:POS="1"-"0"-"0"-"21",ISEACHOTHER=NO;

# =============================================================================
# 设置环境变量
# =============================================================================
data_path = r'd:\3G邻区自动优化' + '\\'
out_path = r'd:\3G邻区自动优化\修改脚本输出' + '\\'

cell_neighbor_file = [x for x in os.listdir(data_path) if '小区邻区检查结果' in x ]
carrie_neighbor_file = [x for x in os.listdir(data_path) if '载频邻区检查结果' in x ]

for file in cell_neighbor_file : 
    df_tmp1 = pd.read_excel(data_path + file, sheet_name='删除小区邻区')

    df_tmp2 = pd.read_excel(data_path + file, sheet_name='添加小区邻区')
