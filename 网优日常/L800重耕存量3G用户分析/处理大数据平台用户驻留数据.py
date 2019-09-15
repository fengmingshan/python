# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 09:28:00 2019

@author: Administrator
"""
import pandas as pd
import os
import numpy as np

out_path = r'd:\2019年工作\2019年8月4G网络扩频方案\结果输出' + '\\'
data_path = r'D:\2019年工作\2019年8月4G网络扩频方案\诺基亚大数据平台' + '\\'
file = 'qujing_rmk1_20190802.csv'

bts_info_path = r'd:\2019年工作\2019年8月4G网络扩频方案\基站信息表'  + '\\'
L1800_info = 'L1800_info.xlsx'
L800_info = 'L800_info.xlsx'
df_L1800 = pd.read_excel(bts_info_path + L1800_info,encoding = 'utf-8')
df_L800 = pd.read_excel(bts_info_path + L800_info,encoding = 'utf-8')

billing_path = r'd:\2019年工作\2019年8月4G网络扩频方案\计费系统导出' + '\\'
normal_user = '移动号码正常状态.csv'
abnormal_user = '移动号码非正常.csv'
df_normal = pd.read_csv(billing_path + normal_user,engine = 'python')
df_abnormal = pd.read_csv(billing_path + abnormal_user,engine = 'python')
df_valid_user  = df_abnormal[~df_abnormal['状态'].isin(['用户申请拆机(移动业务)','用户要求停机','双停','挂失'])]

df_normal_user = df_normal.append(df_valid_user)
df_3G_user = df_normal_user[(~df_normal_user['IMSI码'].isnull())&(df_normal_user['LTE_4GIMSI'].isnull())]
df_4G_user = df_normal_user[~df_normal_user['LTE_4GIMSI'].isnull()]
df_noIMSI_user = df_normal_user[df_normal_user['IMSI码'].isnull()]
billing_user_ALL = set(df_normal_user['ACC_NBR'])
billing_user_3G = set(df_3G_user['ACC_NBR'])
billing_user_4G = set(df_4G_user['ACC_NBR'])
billing_user_noIMSI = set(df_noIMSI_user['ACC_NBR'])

df_town = df_L1800.append(df_L800)[['eNodeB','town']]
df_town.drop_duplicates('eNodeB', keep='first', inplace = True)
df_town.set_index('eNodeB', inplace = True)
town_dict = df_town['town'].to_dict()

df_net_type = df_L1800.append(df_L800)[['eNodeB','net_type']]
df_net_type.drop_duplicates('eNodeB', keep='first', inplace = True)
df_net_type.set_index('eNodeB', inplace = True)
net_type_dict = df_net_type['net_type'].to_dict()

user_data = pd.read_csv(data_path + file,engine = 'python',encoding = 'utf-8',  chunksize = 100000)
df_user_record = pd.DataFrame()
i = 0
for df_tmp in user_data:
    i += 1
    df_user_record = df_user_record.append(df_tmp)
    if i%100 == 0:
        print('finished: ', i )

df_user_record['town'] = df_user_record['wirelessid'].map(town_dict)
df_user_record['net_type'] = df_user_record['wirelessid'].map(net_type_dict)
df_user_record['country'] = df_user_record['town'].map(lambda x:x[:2])
df_user_record['brand_product'] = df_user_record['brand'] + '_' +  df_user_record['product']


df_1800 =  df_user_record[(df_user_record['net_type'] == 'L1800')&(~df_user_record['brand'].isnull())]
df_800 =  df_user_record[(df_user_record['net_type'] == 'L800')&(~df_user_record['brand'].isnull())]

all_active_uesr = set(df_user_record['rmk1'])
L1800_user = set(df_1800['rmk1'])
L800_user = set(df_800['rmk1'])

ALL_phone = set(df_user_record[~df_user_record['brand'].isnull()]['brand_product'])
L1800_phone = set(df_1800['brand_product'])
L800_phone = set(df_800['brand_product'])
non_L800_phone = ALL_phone - L800_phone

non_L800_user = (all_active_uesr - L800_user) & billing_user_4G
non_4G_user = billing_user_ALL - all_active_uesr
active_4G_user = billing_user_ALL&all_active_uesr


df_active_uesr_phone = df_user_record[df_user_record['rmk1'].isin(billing_user_ALL)][['rmk1','brand','product']]
df_active_uesr_phone.drop_duplicates(['rmk1','brand','product'] , keep='first', inplace = True)
df_non_L800 = df_user_record[df_user_record['rmk1'].isin(non_L800_user)]
df_non_4G_user = df_normal_user[df_normal_user['ACC_NBR'].isin(non_4G_user)]

df_L800_phone = pd.DataFrame()
df_NonL800_phone = pd.DataFrame()
df_4G_user = pd.DataFrame()

df_4G_user['4G用户清单'] = list(active_4G_user)
df_L800_phone['800M终端'] = list(L800_phone)
df_NonL800_phone['非800M终端'] = list(non_L800_phone)


with pd.ExcelWriter(out_path + '非L800用户清单输出.xlsx') as writer:
    df_non_L800.to_excel(writer,'Non_L800',index = False)


with pd.ExcelWriter(out_path + '4G用户清单输出.xlsx') as writer:
     df_4G_user.to_excel(writer,'4G_user',index = False)


with pd.ExcelWriter(out_path + '非4G用户清单输出.xlsx') as writer:
     df_non_4G_user.to_excel(writer,'non_4G_user',index = False)

with pd.ExcelWriter(out_path + '手机型号清单输出.xlsx') as writer:
    df_L800_phone.to_excel(writer,'800M终端',index = False)
    df_NonL800_phone.to_excel(writer,'非800M终端',index = False)

with pd.ExcelWriter(out_path + '全网用户手机型号.xlsx') as writer:
    df_active_uesr_phone.to_excel(writer,'全网用户手机型号',index = False)
