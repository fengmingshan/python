# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-09-07 11:17:31
# @Last Modified by:   Administrator
# @Last Modified time: 2019-09-07 16:10:16

import pandas as pd
import os

data_path = 'D:/2019年工作/2019年8月4G网络扩频方案/诺基亚大数据平台/'
user_files = ['qujing_rmk1_temp_20190903.csv','qujing_rmk1_temp_20190808.csv']
os.chdir(data_path)

df_uesr = pd.DataFrame()
for file in user_files:
    reader  = pd.read_csv(file, engine = 'python',encoding='utf-8',chunksize = 100000)
    for df_tmp in reader:
        df_uesr = df_uesr.append(df_tmp)
df_uesr = df_uesr[['rmk1','brand','product']]
df_uesr = df_uesr[(~df_uesr['rmk1'].isnull())&(~df_uesr['brand'].isnull())]
df_uesr.drop_duplicates(['rmk1','brand','product'],keep='first',inplace=True)
df_uesr.reset_index(inplace = True)
df_uesr['是否支持800M'] = ''
df_uesr['备注（芯片）'] = ''
df_uesr['rmk1'] = df_uesr['rmk1'].astype(int)
df_uesr.rename(columns = {'rmk1':'号码',
    'brand':'厂家','product':'型号'},inplace=True)

with open('曲靖手机型号库.csv','w') as writer:
    df_uesr.to_csv(writer,index=False)