# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 15:42:54 2018

@author: Administrator
"""
import pandas as pd
import numpy as np
import os
from datetime import datetime

data_path = r'd:\test\原始数据' + '\\'
out_path = r'd:\test' + '\\'

zte_files = os.listdir(data_path) 
df_zte_4G_user = pd.DataFrame()
for file in zte_files:    
    df_tmp = pd.read_csv(data_path + file,skiprows = 5,engine = 'python', encoding = 'gbk')
    df_tmp.fillna(0,inplace=True)
    df_zte_4G_user = df_zte_4G_user.append(df_tmp)
    # =============================================================================
    # 计算每日实际忙时确定RRC连接用户数
    # =============================================================================
df_pivot_rrc = pd.pivot_table(df_zte_4G_user, index=['开始时间'], values = '最大RRC连接用户数_1', aggfunc = {'最大RRC连接用户数_1':np.sum})                                                  
df_pivot_rrc = df_pivot_rrc.sort_values(by='最大RRC连接用户数_1',ascending = False)
df_pivot_rrc = df_pivot_rrc.reset_index()
busy_hour =  df_pivot_rrc.loc[0,'开始时间']
df_max_rrc =  df_zte_4G_user[df_tmp['开始时间'] == busy_hour]    

df_max_rrc.to_csv(out_path + "4G.csv",encoding ='gbk' )

