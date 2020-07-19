# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 08:56:10 2020

@author: Administrator
"""
import pandas as pd
import os

path = r'C:\Users\Administrator\Desktop\复杂文本处理'
# 切换工作目录
os.chdir(path)
files = os.listdir()
alarm_files = [x for x in files if '.txt' in x]
# 创建空的数据表格df_alarm准备装数据
df_alarm = pd.DataFrame(columns = ['基站名称', '告警级别', '告警名称', '告警原因', '发生时间' ,'附加信息'])

# 定义list容器准备装告警详细数据
bts_name = []
alarm_level = []
alarm_name = []
alarm_cause = []
alarm_start_time = []
problem_text = []

for file in alarm_files:
    f = open(file,'r')
    content = f.readlines()

    for num in range(0,len(content)):
        if 'ObjectOfReference:' in content[num]:
            bts_name.append(content[num].split(',')[2].split('=')[1])
            alarm_level.append(content[num+1].split(': ')[1])
            if 'SpecificProblem' in content[num+28]:
                alarm_name.append(content[num+28].split(': ')[1])
            elif 'SpecificProblem' in content[num+31]:
                alarm_name.append(content[num+31].split(': ')[1])
            elif 'SpecificProblem' in content[num+33]:
                alarm_name.append(content[num+33].split(': ')[1])
            else:
                alarm_name.append('')
            if 'ProbableCause' in content[num+22]:
                alarm_cause.append(content[num+22].split(': ')[1])
            else:
                alarm_cause.append('')
            alarm_start_time.append(content[num+16].split(': ')[1])
            problem_text.append(content[num+24].split(': ')[1])

df_alarm['基站名称'] = bts_name
df_alarm['告警级别'] = alarm_level
df_alarm['告警名称'] = alarm_name
df_alarm['告警原因'] = alarm_cause
df_alarm['发生时间'] = alarm_start_time
df_alarm['附加信息'] = problem_text

f = pd.ExcelWriter('统计结果.xlsx')
df_alarm.to_excel(f,index =False)
f.close()