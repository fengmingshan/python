# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 15:51:14 2019

@author: Administrator
"""

import pandas as pd
import os
from datetime import datetime
import re

data_path = r'D:\test' + '\\'
all_files = os.listdir(data_path)
files = [x for x in all_files if '.txt' in x ]
content = []
for file in files:
     file_tmp = open(data_path + file)
     lines = file_tmp.readlines()
for line in lines:
     content.append(line)

df_alarm =pd.DataFrame()
df_alarm['网元'] = ''
df_alarm['告警名称'] = ''
df_alarm['告警级别'] = ''
df_alarm['发生时间'] = ''
df_alarm['恢复时间'] = ''
df_alarm['故障原因'] = ''

p1 = r'Critical(.*[\s\S]+?)*?FDN2:'  # 匹配一条告警的正则表达式正则表达式
pattern1 = re.compile(p1) # 编译
ls1 = re.findall(pattern1,file_tmp)
i = 0
for j in range(0,len(content)):
     if '===========' in content[j]:
          df_alarm.loc[i,'网元'] = content[j-1].split('=')[3].replace('\n','')
          df_alarm.loc[i,'告警名称'] = content[j+30].split(':')[1].replace('\n','')
          df_alarm.loc[i,'告警级别'] = content[j+3].split(':')[1].replace('\n','')
          df_alarm.loc[i,'发生时间'] = content[j+18].split(':')[1].replace('\n','')
          df_alarm.loc[i,'恢复时间'] = content[j+13].split(':')[1].replace('\n','')
          df_alarm.loc[i,'故障原因'] = content[j+24].split(':')[1].replace('\n','')
          i +=1

current_time = str(datetime.now()).split(' ')[0]

with pd.ExcelWriter(data_path + '爱立信存留告警' + current_time + '.xlsx' ) as writer:
     df_alarm.to_excel(writer,'爱立信存留告警')





