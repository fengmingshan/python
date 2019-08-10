# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 16:06:41 2019

@author: Administrator
"""

import pandas as pd
import os
import numpy as np

out_path = r'd:\2019年工作\2019年8月4G网络扩频方案\结果输出' + '\\'

user_data_traffic = r'd:\2019年工作\2019年8月4G网络扩频方案\计费系统导出\曲靖存量纯3G用户上网清单_2019-07.xlsx'
df_user_data_traffic = pd.read_excel(user_data_traffic)
def judge_uesr_type(voice,data,avg_data):
     if voice == 0 & data == 0:
          uesr_type = '双零用户',lever = '无'
     elif voice == 0 & data != 0 & avg_data <30:
          uesr_type = '数据卡用户',lever = '轻度'
     elif voice == 0 & data != 0 & avg_data >=30:
          uesr_type = '数据卡用户',lever = '重度'
     elif voice != 0 & data < 31457280:
          uesr_type = '纯语音用户',lever = '无'
     elif voice != 0 & data > 31457280:
          uesr_type = '语音数据用户'





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

df_number_pivot = pd.pivot_table(df_1X_has_number, index=['用户号码'],
                                                 values =['通话次数'],
                                                 aggfunc = {'通话次数':np.sum})
number_calls_dict = df_number_pivot['通话次数'].to_dict()

df_imsi_pivot = pd.pivot_table(df_1X_no_number, index=['imsi'],
                                                 values =['通话次数'],
                                                 aggfunc = {'通话次数':np.sum})
imsi_calls_dict = df_imsi_pivot['通话次数'].to_dict()

df_1X_has_number['通话总次数'] = df_1X_has_number['用户号码'].map(number_calls_dict)
df_1X_has_number_pivot = pd.pivot_table(df_1X_has_number,
                                       index=['用户号码','imsi','用户状态','区县','乡镇','通话总次数'],
                                       values =['通话次数'],
                                       aggfunc = {'通话次数':np.sum})
df_1X_has_number_pivot.reset_index(inplace = True)
df_1X_has_number_pivot['占比'] = round(df_1X_has_number_pivot['通话次数']/df_1X_has_number_pivot['通话总次数'],4)

df_1X_no_number['通话总次数'] = df_1X_no_number['imsi'].map(imsi_calls_dict)
df_1X_no_number_pivot = pd.pivot_table(df_1X_no_number,
                                       index=['imsi','区县','乡镇','通话总次数'],
                                       values =['通话次数'],
                                       aggfunc = {'通话次数':np.sum})
df_1X_no_number_pivot.reset_index(inplace = True)
df_1X_no_number_pivot['占比'] = round(df_1X_no_number_pivot['通话次数']/df_1X_no_number_pivot['通话总次数'],4)
df_1X_no_number_pivot['用户号码'] = ''
df_1X_no_number_pivot['用户状态'] = ''
df_1X_no_number_pivot = df_1X_no_number_pivot[['用户号码','imsi','用户状态','区县','乡镇','通话总次数','通话次数','占比']]

user_number_set = set(df_1X_has_number['用户号码'])
no_number_user_set =  set(df_1X_no_number['imsi'])

df_uesr_home_all = pd.DataFrame()
Reset_index = pd.DataFrame.reset_index
Drop = pd.DataFrame.drop
Append = pd.DataFrame.append
i = 0
for number in user_number_set:
     i += 1
     df_user_calls = df_1X_has_number_pivot[df_1X_has_number_pivot['用户号码'] == number]
     max_call_number = df_user_calls['通话次数'].max()
     df_uesr_home_all = Append(df_uesr_home_all,df_user_calls[df_user_calls['通话次数'] == max_call_number])
     if i%100 == 0:
          print('finished: ', i ,' tatla: ', len(user_number_set))

j = 0
for imsi in no_number_user_set:
     j += 1
     df_user_calls = df_1X_no_number_pivot[df_1X_no_number_pivot['imsi'] == imsi]
     max_call_number = df_user_calls['通话次数'].max()
     df_uesr_home_all = Append(df_uesr_home_all,df_user_calls[df_user_calls['通话次数'] == max_call_number])
     if j%100 == 0:
          print('finished: ', j ,' tatla: ', len(user_number_set))

country_set = set(df_uesr_home_all['区县'])
for country in country_set:
     df_country = df_uesr_home_all[df_uesr_home_all['区县'] == country]
     with pd.ExcelWriter(out_path + '常驻用户'+ '\\' +country + '_常驻纯3G用户清单.xlsx') as writer:
          town_set = set(df_country['乡镇'])
          for town in town_set:
               df_town = df_country[df_country['乡镇'] == town]
               df_town.to_excel(writer,town,index = False)

df_country_provit = pd.pivot_table(df_uesr_home_all,
                                  index=['区县'],
                                  values =['imsi'],
                                  aggfunc = {'imsi':len})
df_country_provit.reset_index(inplace = True)

df_town_provit_= pd.pivot_table(df_uesr_home_all,
                                  index=['区县','乡镇'],
                                  values =['imsi'],
                                  aggfunc = {'imsi':len})
df_town_provit_.reset_index(inplace = True)



with pd.ExcelWriter(out_path + '常驻3G用户清单.xlsx') as writer:
    df_uesr_home_all.to_excel(writer,'常驻3G用户清单',index =False)
    df_country_provit.to_excel(writer,'按县统计',index =False)
    df_town_provit_.to_excel(writer,'按乡镇统计',index =False)


with pd.ExcelWriter(out_path + '用户1X通话记录.xlsx') as writer:
    df_1X_has_number.to_excel(writer,'有号码用户记录')
    df_1X_no_number.to_excel(writer,'无号码用户记录')

with pd.ExcelWriter(out_path + '用户状态和IMSI.xlsx') as writer:
    df_user_state.to_excel(writer,'用户状态')
    df_user_imsi.to_excel(writer,'IMSI')




