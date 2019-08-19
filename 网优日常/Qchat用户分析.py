# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 14:24:25 2019

@author: Administrator
"""

import pandas as pd
from numpy import int64
data_path = r'd:\test' + '\\'
billing_data = r'd:\test\划小清单201907.csv'

df_bill = pd.read_csv(billing_data,engine = 'python',chunksize = 10000)

uesr_bill_record = pd.read_csv(billing_data , engine = 'python',  chunksize = 100000)
df_bill = pd.DataFrame()
i = 0
for df_tmp in uesr_bill_record:
     i += 1
     df_bill = df_bill.append(df_tmp)
     if i%100 == 0:
          print('finished: ', i )

df_bill_mobile = df_bill[df_bill['用户号码'].map(lambda x:x[:4] != '0874')]

qchat_uesr_data = r'd:\test\曲靖QCchat用户状态.xlsx'
df_qchat_uesr = pd.read_excel(qchat_uesr_data )
df_qchat_uesr['用户号码'] = df_qchat_uesr['用户号码'].astype(int64)
df_bill_mobile['用户号码'] = df_bill_mobile['用户号码'].astype(int64)

df_qchat_uesr = pd.merge(df_qchat_uesr,df_bill_mobile,how = 'left',on = '用户号码')

with pd.ExcelWriter(data_path + 'Qchat用户清单.xlsx') as writer:
    df_qchat_uesr.to_excel(writer,'Qchat用户清单',index =False)
