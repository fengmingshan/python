# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 15:51:14 2019

@author: Administrator
"""
from pandas import ExcelWriter,DataFrame
from os import listdir
from datetime import datetime
import re
from re import findall

data_path = r'd:\_小程序\爱立信告警统计' + '\\'
all_files = listdir(data_path)
files = [x for x in all_files if '.txt' in x ]
content_all = ''
for file in files:
     file_tmp = open(data_path + file)
     content = file_tmp.read()
     content_all = content_all + content


df_alarm = DataFrame()
df_alarm['网元'] = ''
df_alarm['告警名称'] = ''
df_alarm['告警级别'] = ''
df_alarm['告警当前状态'] = ''
df_alarm['发生时间'] = ''
df_alarm['恢复时间'] = ''
df_alarm['故障原因'] = ''
df_alarm['附加信息'] = ''

alarm_name_dict ={ 'Heartbeat Failure':'基站掉站',
                    'Service Unavailable':'小区服务不可用',
                    'No Connection':'',
                    'RET Failure':'',
                    'RET Not Calibrated':'',
                    'Service Degraded':'小区服务质量下降',
                    'VSWR Over Threshold':'',
                    'Link Failure':'',
                    'Power Loss':'',
                    'TimeSyncIO Reference Failed':'',
                    'Calendar Clock Misaligned':'',
                    'Synchronization End':'',
                    'Synchronization Start':'',
                    'PLMN Service Unavailable':'',
                    'SFP Stability Problem':''}

alarm_class_dict ={ 'Critical':'紧急告警',
                    'Major':'主要告警',
                    'Minor':'次要告警',
                    'Warning':'警告告警',
                    'Indeterminate':'不确定告警',
                    'Cleared':'已恢复告警'}

p1 = r'(AlarmId.*[\s\S]+?FDN2:)'  # 正则表达式，匹配一条完整的告警记录文件
alarm_list = findall(p1,content_all) # 通过正则匹配分割所有的告警记录

i = 0
for j in range(0,len(alarm_list)):
     lines = alarm_list[j].split('\n')
     for line in lines:
          if 'ObjectOfReference:' in line:
               df_alarm.loc[i,'网元'] = line.split(',')[2].split('=')[1]
          if 'SpecificProblem:' in line:
               df_alarm.loc[i,'告警名称'] = line.split(':')[1].replace('\n','')
          if 'PerceivedSeverity:' in line:
               df_alarm.loc[i,'告警级别'] = line.split(':')[1].replace('\n','')
          if 'EventTime:' in line:
               df_alarm.loc[i,'发生时间'] = line.split('EventTime:')[1].replace('\n','')
          if 'CeaseTime:' in line:
               df_alarm.loc[i,'恢复时间'] = line.split('CeaseTime:')[1].replace('\n','')
          if 'ProbableCause:' in line:
               df_alarm.loc[i,'故障原因'] = line.split(':')[1].replace('\n','')
          if 'eriAlarmNObjAdditionalText:' in line:
               df_alarm.loc[i,'附加信息'] = line.split(':')[1].replace('\n','')
     i +=1

df_alarm['告警名称'] = df_alarm['告警名称'].map(alarm_name_dict)
df_alarm['告警级别'] = df_alarm['告警级别'].map(alarm_class_dict)

current_time = str(datetime.now()).split('.')[0].replace(':','.')

with ExcelWriter(data_path + '爱立信当前告警' + current_time + '.xlsx' ) as writer:
     df_alarm.to_excel(writer,'当前告警',index = False)





