#!/usr/bin/env python
# coding: utf-8

# In[66]:


import pandas as pd
import os
from datetime import datetime
from dateutil.parser import parse
from dateutil.rrule import *
from interval import Interval


# In[4]:


data_path = 'D:/Notebook/4G小区退服计算'
if not os.path.exists(data_path):
    os.mkdir(data_path)
if not os.path.exists(data_path + './报表输出'):
    os.mkdir(data_path + './报表输出')
os.chdir(data_path)


# In[5]:


block_cell = '屏蔽小区.xlsx'


# In[6]:


# 需要使用到的自定义函数
def 填写退服小区(a, b):
    if pd.isnull(a):
        return b.split('_')[0] + '_' + b.split('_')[1]
    else:
        return a


# In[23]:


df_block = pd.read_excel(block_cell)
df_block['退服小区标识'] = df_block.apply(
    lambda x: 填写退服小区(x.关联小区标识, x.告警对象名称), axis=1)
df_block['告警清除时间'] = df_block['告警清除时间'].map(str)
df_block.head(5)


# In[8]:


df_block.columns


# In[9]:


df_block = df_block[['退服小区标识','告警发生时间', '告警清除时间','退服时长(分钟)', '6-8点退服时长（分钟）', '8-22点退服时长（分钟）',
       '22-24点退服时长（分钟）']]


# In[33]:


df_block.dtypes


# In[63]:


date_list = list(rrule(DAILY, dtstart=parse(
    df_block.loc[0, '告警发生时间']), until=parse(df_block.loc[0, '告警清除时间'])))
day_list = [x.strftime('%Y-%m-%d') for x in  date_list]
print(df_block.loc[0, '告警发生时间'])
print(df_block.loc[0, '告警清除时间'])
print(day_list)
print(type(day_list[0]))


# In[71]:


start_time = datetime.strptime(df_block.loc[0, '告警发生时间'], '%Y-%m-%d %H:%M:%S')
end_time = datetime.strptime(df_block.loc[0, '告警清除时间'],'%Y-%m-%d %H:%M:%S')
print(start_time)
print(end_time)
print(type(start_time))
for day in day_list:
    Interval(day + ' '+'00:00:00')
    print(datetime.strptime(day +' 00:00:00',"%Y-%m-%d %H:%M:%S"))  
    


# In[ ]:





# In[ ]:




