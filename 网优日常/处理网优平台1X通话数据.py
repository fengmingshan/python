# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 16:06:41 2019

@author: Administrator
"""

import pandas as pd
import os
import numpy as np

out_path = r'd:\2019年工作\2019年8月4G网络扩频方案\结果输出' + '\\'

call_file_1X = r'd:\2019年工作\2019年8月4G网络扩频方案\网优平台导出1X通话数据\小区下面用户通话次数(不分释放原因).csv'
df_1X_call = pd.read_csv(call_file_1X ,engine = 'python')
df_1X_call = df_1X_call[(df_1X_call['cell_name'].str.contains('QJ'))&(~df_1X_call['cell_name'].str.contains('六螺蛳'))]
df_1X_call['imsi'] = df_1X_call['imsi'].astype(str)
call_user_set = set(df_1X_call['imsi'])

billing_path = r'd:\2019年工作\2019年8月4G网络扩频方案\计费系统导出' + '\\'
normal_user = '移动号码正常状态.csv'
abnormal_user = '移动号码非正常.csv'
state_file = '移动用户状态字典.xlsx'

df_state = pd.read_excel(billing_path + state_file)
df_state.set_index('状态码' , inplace =True )
state_dict = df_state['状态'].to_dict()

df_normal = pd.read_csv(billing_path + normal_user,engine = 'python',dtype =str )
df_abnormal = pd.read_csv(billing_path + abnormal_user,engine = 'python',dtype =str )
df_normal['IMSI码'] = df_normal['IMSI码'].str.replace('nan','-')
df_abnormal['IMSI码'] = df_abnormal['IMSI码'].str.replace('nan','-')

df_normal['状态'] = df_normal['STATE'].map(state_dict)
df_abnormal['状态'] = df_abnormal['STATE'].map(state_dict)
df_valid_user  = df_abnormal[~df_abnormal['状态'].isin(['用户申请拆机(移动业务)','用户要求停机','双停','挂失'])]
df_normal_user = df_normal.append(df_valid_user)

df_user_state = df_normal_user[df_normal_user['IMSI码'] != '-'][['IMSI码','状态']]
df_user_state['IMSI码'] = df_user_state['IMSI码'].astype(str)
df_user_state.set_index('IMSI码' , inplace =True )
user_state_dict = df_user_state['状态'].to_dict()

df_user_imsi = df_normal_user[df_normal_user['IMSI码'] != '-'][['ACC_NBR','IMSI码']]
df_user_imsi['IMSI码'] = df_user_imsi['IMSI码'].astype(str)
df_user_imsi.set_index('IMSI码' , inplace =True )
imsi_dict = df_user_imsi['ACC_NBR'].to_dict()

df_1X_call['区县'] = df_1X_call['cell_name'].map(lambda x:x.split('QJ')[1][:2])
df_1X_call['乡镇'] = df_1X_call['cell_name'].map(lambda x:x.split('QJ')[1][2:4])

df_1X_call['乡镇'] = df_1X_call['乡镇'].map(lambda x:x.replace('十八','十八连山'))
df_1X_call['乡镇'] = df_1X_call['乡镇'].map(lambda x:x.replace('黄泥','黄泥河'))
df_1X_call['乡镇'] = df_1X_call['乡镇'].map(lambda x:x.replace('大莫','大莫古'))
df_1X_call['乡镇'] = df_1X_call['乡镇'].map(lambda x:x.replace('小百','小百户'))
df_1X_call['乡镇'] = df_1X_call['乡镇'].map(lambda x:x.replace('三岔','三岔河'))
df_1X_call['乡镇'] = df_1X_call['乡镇'].map(lambda x:x.replace('八大','八大河'))
df_1X_call['乡镇'] = df_1X_call['乡镇'].map(lambda x:x.replace('大水','大水井'))
df_1X_call['乡镇'] = df_1X_call['乡镇'].map(lambda x:x.replace('旧屋','旧屋基'))
df_1X_call['乡镇'] = df_1X_call['乡镇'].map(lambda x:x.replace('鲁布','鲁布革'))
df_1X_call['乡镇'] = df_1X_call['乡镇'].map(lambda x:x.replace('王家','王家庄'))
df_1X_call['乡镇'] = df_1X_call['乡镇'].map(lambda x:x.replace('马过','马过河'))
df_1X_call['乡镇'] = df_1X_call['乡镇'].map(lambda x:x.replace('白石','白石江'))

df_1X_call['用户状态'] = df_1X_call['imsi'].map(user_state_dict)
df_1X_call['用户号码'] = df_1X_call['imsi'].map(imsi_dict)

df_1X_has_number = df_1X_call[df_1X_call['用户号码'].notnull()]
df_1X_no_number = df_1X_call[df_1X_call['用户号码'].isnull()]
user_number_set = set(df_1X_has_number['用户号码'])


with pd.ExcelWriter(out_path + '用户1X通话记录.xlsx') as writer:
    df_1X_has_number.to_excel(writer,'有号码用户记录')
    df_1X_no_number.to_excel(writer,'无号码用户记录')

with pd.ExcelWriter(out_path + '用户状态和IMSI.xlsx') as writer:
    df_user_state.to_excel(writer,'用户状态')
    df_user_imsi.to_excel(writer,'IMSI')




