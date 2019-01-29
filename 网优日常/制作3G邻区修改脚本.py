# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 15:27:13 2019

@author: Administrator
"""

import pandas as pd 
import os


# =============================================================================
# 设置环境变量
# =============================================================================
data_path = r'd:\3G邻区自动优化' + '\\'
out_path = r'd:\3G邻区自动优化\修改脚本输出' + '\\'

BSC1_cell_neighbor_file = [x for x in os.listdir(data_path) if ('BSC1_' in x and '载频邻区检查结果' in x )][0]
BSC1_carrie_neighbor_file = [x for x in os.listdir(data_path) if ('BSC1_' in x and '小区邻区检查结果' in x )]

BSC2_cell_neighbor_file = [x for x in os.listdir(data_path) if ('BSC2_' in x and '载频邻区检查结果' in x )]
BSC2_carrie_neighborr_file = [x for x in os.listdir(data_path) if ('BSC2_' in x and '小区邻区检查结果' in x )]

print(BSC1_cell_neighbor_file)

ADD 1X_LINKCELL_L:POS="1"-"0"-"21",NCELLSYSTEM=1,NCELL=1,ISEACHOTHER=0;