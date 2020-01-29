# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 14:22:56 2019

@author: Administrator
"""
import pandas as pd
import os
import numpy as np

data_path = 'C:/Users/Administrator/Desktop/log'
os.chdir(data_path)

files = os.listdir()
log_files = [x for x in files if '.log' in x ]

# 定义提取用户号码的函数
def extract_num(log_files):
    df = pd.DataFrame()
    for n,file in enumerate(log_files):
        print('共有{files}个文件，开始处理第{N}个文件'.format(files = len(log_files),N = n+1))
        content = np.loadtxt(file,delimiter = '<',dtype = str)
        content = content[:,1]
        df_tmp = pd.DataFrame(content,columns =['content'])
        df_tmp = df_tmp[df_tmp['content'].str.contains('SEND IMS BOSS')]
        df_tmp['IMSI'] = df_tmp['content'].map(lambda x:x.split('IMSI=')[1][:15])
        df_tmp['MSISDN'] = df_tmp['content'].map(lambda x:x.split('MSISDN=')[1][:13])
        df = df.append(df_tmp)
    return df

# 针对多个文件log_files，调用函数提取用户号码
df = pd.DataFrame()
df_res = extract_num(log_files)

df_res['次数'] = df_res['IMSI']
df_res_pivot = pd.pivot_table(df_res, index=['IMSI','MSISDN'],
                                 values=['次数'],
                                 aggfunc={'次数': len})
df_res_pivot.reset_index(inplace =True)
with open('提取结果.csv','w') as writer:
    df_res_pivot.to_csv(writer,index = False)
    print('表格已输出到:{path},请到该目录查看！'.format(path = data_path))
