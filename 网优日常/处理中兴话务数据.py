# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 15:45:16 2019

@author: Administrator
"""

import pandas as pd
import numpy as np
import os

path =  r'D:\_非标带宽扩容\zte'+'\\'
out_path = r'D:\_非标带宽扩容\结果输出' +'\\'
zte_files = os.listdir(path)

df_zte = pd.DataFrame()
for file in zte_files:
     df_tmp = pd.read_csv(path + file,engine = 'python')
     df_zte = df_zte.append(df_tmp)
df_zte = df_zte.sort_values(by='序号',ascending = True) # 按时间顺序升序排列
df_zte.reset_index(inplace = True)
df_zte.drop('index',axis = 1,inplace =True)
df_zte['日期'] = df_zte['开始时间'].map(lambda x:x.split(' ')[0])
df_zte['下行PRB平均占用率_1'] = df_zte['下行PRB平均占用率_1'].map(lambda x:x.replace('%',''))
df_zte['下行PRB平均占用率_1'] = df_zte['下行PRB平均占用率_1'].astype(float)
df_zte['下行PRB平均占用率_1'] = df_zte['下行PRB平均占用率_1'].map(lambda x:x/100)

df_zte_pivot = pd.pivot_table(df_zte, index=['网元','日期','小区名称'],
                                  values =['最大RRC连接用户数_1' ,
                                           '下行PRB平均占用率_1',
                                           'Total DL Data Volume(GB)'],
                                  aggfunc = {'最大RRC连接用户数_1':np.max,
                                             '下行PRB平均占用率_1':np.max,
                                             'Total DL Data Volume(GB)':np.max})

df_zte_pivot = df_zte_pivot.reset_index()
df_zte_busy  = df_zte_pivot[((df_zte_pivot['下行PRB平均占用率_1']>= 0.5) & (df_zte_pivot['Total DL Data Volume(GB)']>= 1.5))
                              |((df_zte_pivot['下行PRB平均占用率_1']>= 0.5) & (df_zte_pivot['最大RRC连接用户数_1']>= 50))]

busy_counts = df_zte_busy['小区名称'].value_counts()
dict_busy = busy_counts.to_dict()
df_zte_busy['上月超忙天数']  = df_zte_busy['小区名称'].map(dict_busy)

with pd.ExcelWriter(out_path + '中兴话务量汇总.xlsx') as writer:
     df_zte_busy.to_excel(writer,'超忙小区',index =False)
     df_zte_pivot.to_excel(writer,'原始数据',index =False)


