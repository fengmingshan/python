# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 14:41:20 2019

@author: Administrator
"""

import pandas as pd      #导入pandas库
import os    

data_path = r'd:\test' + '\\'
files  =  os.listdir(data_path)
df_all = pd.DataFrame()
for file in files:
    df_tmp = pd.read_csv(data_path + file)
    df_all = df_all.append(df_tmp)

df_all = df_all.drop('Offset',axis = 1)
df_all.rename(columns={'MS1_RSRP':'ServingCell_RSRP',
                       'MS1_RSRQ':'ServingCell_RSRQ',
                       'MS1_PCI':'ServingCell_PCI',
                       'MS1_Neighbor Cell RSRP[1]':'Neighbor1_RSRP',
                       'MS1_Neighbor Cell RSRQ[1]':'Neighbor1_RSRQ',
                       'MS1_Neighbor Cell PCI[1]':'Neighbor1_PCI',
                       'MS1_Neighbor Cell RSRP[2]':'Neighbor2_RSRP',
                       'MS1_Neighbor Cell RSRQ[2]':'Neighbor2_RSRQ',
                       'MS1_Neighbor Cell PCI[2]':'Neighbor2_PCI',
                       'MS1_Neighbor Cell RSRP[3]':'Neighbor3_RSRP',
                       'MS1_Neighbor Cell RSRQ[3]':'Neighbor3_RSRQ',
                       'MS1_Neighbor Cell PCI[3]':'Neighbor3_PCI',
                       'MS1_Neighbor Cell RSRP[4]':'Neighbor4_RSRP',
                       'MS1_Neighbor Cell RSRQ[4]':'Neighbor4_RSRQ',
                       'MS1_Neighbor Cell PCI[4]':'Neighbor4_PCI',
                       'MS1_Neighbor Cell RSRP[5]':'Neighbor5_RSRP',
                       'MS1_Neighbor Cell RSRQ[5]':'Neighbor5_RSRQ',
                       'MS1_Neighbor Cell PCI[5]':'Neighbor5_PCI',
                       'MS1_Neighbor Cell RSRP[6]':'Neighbor6_RSRP',
                       'MS1_Neighbor Cell RSRQ[6]':'Neighbor6_RSRQ',
                       'MS1_Neighbor Cell PCI[6]':'Neighbor6_PCI',
                       'MS1_Neighbor Cell RSRP[7]':'Neighbor7_RSRP',
                       'MS1_Neighbor Cell RSRQ[7]':'Neighbor7_RSRQ',
                       'MS1_Neighbor Cell PCI[7]':'Neighbor7_PCI',
                       'MS1_Neighbor Cell RSRP[8]':'Neighbor8_RSRP',
                       'MS1_Neighbor Cell RSRQ[8]':'Neighbor8_RSRQ',
                       'MS1_Neighbor Cell PCI[8]':'Neighbor8_PCI',
                       'MS1_SINR':'SINR'
                       },inplace =True)
    
def Judge_MOD3(a,b,c,d):
	if a%3 == b % 3  and d-c <= 3:
		return 1
	else:
		return 0

df_all['Neighbor1_IS_MOD3'] = df_all.apply(lambda x: Judge_MOD3(x.ServingCell_PCI,x.Neighbor1_PCI,x.Neighbor1_RSRP,x.ServingCell_RSRP),axis =1 )
df_all['Neighbor2_IS_MOD3'] = df_all.apply(lambda x: Judge_MOD3(x.ServingCell_PCI,x.Neighbor2_PCI,x.Neighbor2_RSRP,x.ServingCell_RSRP),axis =1 )
df_all['Neighbor3_IS_MOD3'] = df_all.apply(lambda x: Judge_MOD3(x.ServingCell_PCI,x.Neighbor3_PCI,x.Neighbor3_RSRP,x.ServingCell_RSRP),axis =1 )
df_all['Neighbor4_IS_MOD3'] = df_all.apply(lambda x: Judge_MOD3(x.ServingCell_PCI,x.Neighbor4_PCI,x.Neighbor4_RSRP,x.ServingCell_RSRP),axis =1 )
df_all['Neighbor5_IS_MOD3'] = df_all.apply(lambda x: Judge_MOD3(x.ServingCell_PCI,x.Neighbor5_PCI,x.Neighbor5_RSRP,x.ServingCell_RSRP),axis =1 )
df_all['Neighbor6_IS_MOD3'] = df_all.apply(lambda x: Judge_MOD3(x.ServingCell_PCI,x.Neighbor6_PCI,x.Neighbor6_RSRP,x.ServingCell_RSRP),axis =1 )
df_all['Neighbor7_IS_MOD3'] = df_all.apply(lambda x: Judge_MOD3(x.ServingCell_PCI,x.Neighbor7_PCI,x.Neighbor7_RSRP,x.ServingCell_RSRP),axis =1 )
df_all['Neighbor8_IS_MOD3'] = df_all.apply(lambda x: Judge_MOD3(x.ServingCell_PCI,x.Neighbor8_PCI,x.Neighbor8_RSRP,x.ServingCell_RSRP),axis =1 )

df_all = df_all[['ServingCell_RSRP',
                'ServingCell_RSRQ',
                'ServingCell_PCI',
                'Neighbor1_RSRP',
                'Neighbor1_RSRQ',
                'Neighbor1_PCI',
                'Neighbor1_IS_MOD3',
                'Neighbor2_RSRP',
                'Neighbor2_RSRQ',
                'Neighbor2_PCI',
                'Neighbor2_IS_MOD3',
                'Neighbor3_RSRP',
                'Neighbor3_RSRQ',
                'Neighbor3_PCI',
                'Neighbor3_IS_MOD3',
                'Neighbor4_RSRP',
                'Neighbor4_RSRQ',
                'Neighbor4_PCI',
                'Neighbor4_IS_MOD3',
                'Neighbor5_RSRP',
                'Neighbor5_RSRQ',
                'Neighbor5_PCI',
                'Neighbor5_IS_MOD3',
                'Neighbor6_RSRP',
                'Neighbor6_RSRQ',
                'Neighbor6_PCI',
                'Neighbor6_IS_MOD3',
                'Neighbor7_RSRP',
                'Neighbor7_RSRQ',
                'Neighbor7_PCI',
                'Neighbor7_IS_MOD3',
                'Neighbor8_RSRP',
                'Neighbor8_RSRQ',
                'Neighbor8_PCI',
                'Neighbor8_IS_MOD3',
                'SINR']]

df_all.to_csv(data_path + '曲靖DT数据高速.csv',index = False) 
