# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 16:06:41 2019

@author: Administrator
"""

import pandas as pd
import os
import numpy as np
from numba import jit


def judge_uesr_type(voice,data,avg_data):
     user_info_list = []
     if (voice == 0)&(data == 0):
          uesr_type = '双零用户'
          uesr_level = '无'
     elif (voice < 10)& (data > 0) & (avg_data <30):
          uesr_type = '数据卡用户'
          uesr_level = '轻度'
     elif (voice < 10) & (data > 0) & (avg_data >=30):
          uesr_type = '数据卡用户'
          uesr_level = '重度'
     elif (voice < 10) & (data >= 0) & (data < 31457280):
          uesr_type = '纯语音用户'
          uesr_level = '无'
     elif (voice >= 10) & (data >= 0) & (data < 31457280):
          uesr_type = '纯语音用户'
          uesr_level = '无'
     elif (voice >= 10) & (data > 31457280) & (avg_data <30):
          uesr_type = '语音数据用户'
          uesr_level = '轻度'
     elif (voice >= 10) & (data > 31457280) & (avg_data >=30):
          uesr_type = '语音数据用户'
          uesr_level = '重度'
     else :
          uesr_type = '否'
          uesr_level = '否'
     user_info_list = [uesr_type,uesr_level]
     return user_info_list

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

number_imsi_file = r'd:\2019年工作\2019年8月4G网络扩频方案\HLR导出数据\number_imsi.csv'
df_number_imsi = pd.read_csv(number_imsi_file,engine ='python')
df_number_imsi['IMSI'] = df_number_imsi['IMSI'].astype(str)
df_number_imsi.set_index('IMSI',inplace = True)
imsi_number_dict1 = df_number_imsi['号码'].to_dict()

number_imsi_file2 = r'd:\2019年工作\2019年8月4G网络扩频方案\网优平台导出1X通话数据\imsi.csv'
df_number_imsi2 = pd.read_csv(number_imsi_file2,engine ='python')
df_number_imsi2 = df_number_imsi2.sort_values(by=['数据生成时间','ms_num'],ascending = False)
df_number_imsi2.drop_duplicates('ms_num', keep='first', inplace = True)
df_number_imsi2['imsi'] = df_number_imsi2['imsi'].astype(str)
df_number_imsi2.set_index('imsi',inplace = True)
imsi_number_dict2 = df_number_imsi2['ms_num'].to_dict()
for k,v in imsi_number_dict2.items():
     if k not in imsi_number_dict1.items():
          imsi_number_dict1[k] = v


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
df_1X_call['用户号码'] = df_1X_call['imsi'].map(imsi_number_dict1)
df_1X_call = df_1X_call[df_1X_call['用户号码'].notnull()]

df_number_pivot = pd.pivot_table(df_1X_call, index=['用户号码'],
                                            values =['通话次数'],
                                            aggfunc = {'通话次数':np.sum})
number_calls_dict = df_number_pivot['通话次数'].to_dict()

df_1X_call['无线接入次数'] = df_1X_call['用户号码'].map(number_calls_dict)

df_1X_call_pivot = pd.pivot_table(df_1X_call,
                                  index=['用户号码','imsi','用户状态','区县','乡镇','无线接入次数'],
                                  values =['通话次数'],
                                  aggfunc = {'通话次数':np.sum})
df_1X_call_pivot.reset_index(inplace = True)
df_1X_call_pivot['常驻地占比'] = round(df_1X_call_pivot['通话次数']/df_1X_call_pivot['无线接入次数'],4)
df_1X_call_pivot.rename(columns={'通话次数':'连接次数'
                                 },inplace =True)


@jit()
def calc_user_home(df):
     user_number_set = set(df['用户号码'])
     df_uesr_home_all = pd.DataFrame()
     Append = pd.DataFrame.append
     i = 0
     for number in user_number_set:
          i += 1
          df_user_calls = df[df['用户号码'] == number]
          max_call_number = df_user_calls['连接次数'].max()
          df_uesr_home_all = Append(df_uesr_home_all,df_user_calls[df_user_calls['连接次数'] == max_call_number])
          if i%100 == 0:
               print('finished: ', i ,' total: ', len(user_number_set))
     return df_uesr_home_all

df_uesr_home_all  =  calc_user_home(df_1X_call_pivot)

user_data_traffic = r'd:\2019年工作\2019年8月4G网络扩频方案\计费系统导出\划小清单201907.csv'
df_user_data_traffic = pd.read_csv(user_data_traffic,engine = 'python')
df_user_data_traffic = df_user_data_traffic[~df_user_data_traffic['用户号码'].map(lambda x:str(x)[:4] == '0874' or str(x)[:3] == '0874')]
df_user_data_traffic['用户号码'] = df_user_data_traffic['用户号码'].astype(np.int64)
df_user_data_traffic['日均流量_MB'] = round(df_user_data_traffic['上网流量']/(1024*1024*30),2)
df_user_data_traffic['平均网速_KBps'] = round(df_user_data_traffic['上网流量']/df_user_data_traffic['上网时长'],0)

df_user_data_traffic['user_info'] =  df_user_data_traffic.apply(lambda x:judge_uesr_type(x.通话次数,x.上网流量,x.日均流量_MB),axis = 1)
df_user_data_traffic['user_type'] = df_user_data_traffic['user_info'].map(lambda x:x[0])
df_user_data_traffic['user_level'] = df_user_data_traffic['user_info'].map(lambda x:x[1])

df_user_type = df_user_data_traffic[['用户号码','user_type']]
df_user_type.set_index('用户号码',inplace =True)
user_type_dict = df_user_type['user_type'].to_dict()

df_user_level = df_user_data_traffic[['用户号码','user_level']]
df_user_level.set_index('用户号码',inplace =True)
user_level_dict = df_user_level['user_level'].to_dict()

df_user_call_count = df_user_data_traffic[['用户号码','通话次数']]
df_user_call_count.set_index('用户号码',inplace =True)
user_call_count_dict = df_user_call_count['通话次数'].to_dict()

df_user_call_druation = df_user_data_traffic[['用户号码','通话时长']]
df_user_call_druation.set_index('用户号码',inplace =True)
user_call_druation_dict = df_user_call_druation['通话时长'].to_dict()

df_user_data = df_user_data_traffic[['用户号码','上网流量']]
df_user_data.set_index('用户号码',inplace =True)
user_data_dict = df_user_data['上网流量'].to_dict()

df_user_avg_data = df_user_data_traffic[['用户号码','日均流量_MB']]
df_user_avg_data.set_index('用户号码',inplace =True)
user_avg_data_dict = df_user_avg_data['日均流量_MB'].to_dict()

df_user_duration = df_user_data_traffic[['用户号码','上网时长']]
df_user_duration.set_index('用户号码',inplace =True)
user_duration_dict = df_user_duration['上网时长'].to_dict()

df_user_times = df_user_data_traffic[['用户号码','上网次数']]
df_user_times.set_index('用户号码',inplace =True)
user_times_dict = df_user_times['上网次数'].to_dict()

df_user_speed = df_user_data_traffic[['用户号码','平均网速_KBps']]
df_user_speed.set_index('用户号码',inplace =True)
user_speed_dict = df_user_speed['平均网速_KBps'].to_dict()

df_uesr_home_all['用户号码'] = df_uesr_home_all['用户号码'].astype(np.int64)
df_uesr_home_all['user_type'] = df_uesr_home_all['用户号码'].map(user_type_dict)
df_uesr_home_all['user_level'] = df_uesr_home_all['用户号码'].map(user_level_dict)
df_uesr_home_all['通话次数'] = df_uesr_home_all['用户号码'].map(user_call_count_dict)
df_uesr_home_all['通话时长'] = df_uesr_home_all['用户号码'].map(user_call_druation_dict)
df_uesr_home_all['上网流量_字节'] = df_uesr_home_all['用户号码'].map(user_data_dict)
df_uesr_home_all['日均流量_MB'] = df_uesr_home_all['用户号码'].map(user_avg_data_dict)
df_uesr_home_all['上网时长_秒_月'] = df_uesr_home_all['用户号码'].map(user_duration_dict)
df_uesr_home_all['上网次数_月'] = df_uesr_home_all['用户号码'].map(user_times_dict)
df_uesr_home_all['平均网速_KBps'] = df_uesr_home_all['用户号码'].map(user_speed_dict)

df_uesr_home_high_data = df_uesr_home_all[((df_uesr_home_all['user_type'] == '数据卡用户')|(df_uesr_home_all['user_type'] == '语音数据用户'))& \
                                          (df_uesr_home_all['user_level'] == '重度')]

country_set = set(df_uesr_home_high_data['区县'])
for country in country_set:
     df_country = df_uesr_home_high_data[df_uesr_home_high_data['区县'] == country]
     with pd.ExcelWriter(out_path + '各县常驻用户清单'+ '\\' +country + '_常驻纯3G用户清单.xlsx') as writer:
          town_set = set(df_country['乡镇'])
          for town in town_set:
               df_town = df_country[df_country['乡镇'] == town]
               df_town.to_excel(writer,town,index = False)

df_country_provit = pd.pivot_table(df_uesr_home_high_data,
                                  index=['区县','user_type'],
                                  values =['imsi'],
                                  aggfunc = {'imsi':len})
df_country_provit.reset_index(inplace = True)

df_town_provit_= pd.pivot_table(df_uesr_home_high_data,
                                  index=['区县','乡镇','user_type'],
                                  values =['imsi'],
                                  aggfunc = {'imsi':len})
df_town_provit_.reset_index(inplace = True)

with pd.ExcelWriter(out_path + '原始数据.xlsx') as writer:
    df_uesr_home_all.to_excel(writer,'3G用户原始数据',index =False)

with pd.ExcelWriter(out_path + '高流量3G用户清单.xlsx') as writer:
    df_uesr_home_high_data.to_excel(writer,'高流量3G用户',index =False)
    df_country_provit.to_excel(writer,'按县统计',index =False)
    df_town_provit_.to_excel(writer,'按乡镇统计',index =False)

#with pd.ExcelWriter(out_path + '用户1X通话记录.xlsx') as writer:
#    df_1X_has_number.to_excel(writer,'有号码用户记录')
#    df_1X_no_number.to_excel(writer,'无号码用户记录')
#
#with pd.ExcelWriter(out_path + '用户状态和IMSI.xlsx') as writer:
#    df_user_state.to_excel(writer,'用户状态')
#    df_user_imsi.to_excel(writer,'IMSI')




