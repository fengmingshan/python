# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 15:03:09 2020

@author: Administrator
"""

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime
import streamlit as st

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

path = 'D:/Test/春节日报'

os.chdir(path)
df_country_flow = pd.read_excel('./节日原始数据.xlsx',sheet_name = 'country_flow')
df_country_users = pd.read_excel('./节日原始数据.xlsx',sheet_name = 'country_user')
df_suboffice_flow = pd.read_excel('./节日原始数据.xlsx',sheet_name = 'suboffice_flow')
df_suboffice_uesr = pd.read_excel('./节日原始数据.xlsx',sheet_name = 'suboffice_uesr')
df_user_busy = pd.read_excel('./节日原始数据.xlsx',sheet_name = 'user_busy')
df_flow_busy = pd.read_excel('./节日原始数据.xlsx',sheet_name = 'flow_busy')
df_BTS_flow = pd.read_excel('./节日原始数据.xlsx',sheet_name = 'bts_flow')
df_suboffice_user_busy = pd.read_excel('./节日原始数据.xlsx',sheet_name = 'suboffice_user_busy')
df_suboffice_flow_day = pd.read_excel('./节日原始数据.xlsx',sheet_name = 'suboffice_flow_day')


#网页开始
country = '麒麟'
suboffice = '寥廓'
today = datetime.today().strftime("%Y-%m-%d")

option1 = st.sidebar.selectbox(
    '你要查看哪个区县的报表?',
     ['麒麟','沾益','马龙','陆良','师宗','罗平','宣威','会泽','富源'])

st.title('春节期间4G话务日报 {day}'.format(day = today))
'你选择的是：', option1
country = option1

suboffice_list = list(df_suboffice_user_busy['支局'].unique())

option2 = st.sidebar.selectbox(
    '你要查看哪个支局的报表?',
     suboffice_list)
'你选择的是：', option2
suboffice = option2

country = '麒麟'
suboffice = '开发区'

df_tmp = df_suboffice_user_busy[df_suboffice_user_busy['区县'] == country]

st.header('{coun}县各支局忙时用户数'.format(coun = country))
fig = plt.figure(figsize=(10,8))
bar_labels = df_tmp['支局'].values
y_pos = np.arange(len(bar_labels))
data = df_tmp['用户数'].values
plt.yticks(y_pos, bar_labels, fontsize=20)
bars = plt.barh(y_pos,data,alpha = 0.5,color='g')
for b,d in zip(bars,data):
    plt.text(b.get_width()+b.get_width()*0.05,b.get_y()+b.get_height()/2,'{}'.format(d))
st.pyplot()

st.header('{coun}县各支局用户数占比'.format(coun = country))
fig = plt.figure(figsize=(10,10))
labels = df_tmp['支局'].values
sizes = [x/sum(df_tmp['用户数']) for x in df_tmp['用户数']]
plt.pie(sizes,labels=labels,autopct='%1.1f%%',shadow=False,startangle=150,textprops={'fontsize':15,'color':'black'})
plt.title("各支局用户数占比（%）",fontsize=24)
plt.axis('equal')
st.pyplot()

df_tmp2 = df_suboffice_flow[df_suboffice_flow['区县'] == country]
df_tmp2 = df_tmp2.groupby(by=['区县', '支局'])['总流量(GB)'].sum()
df_tmp2.sort_values(ascending = True, inplace=True)
df_tmp2 = df_tmp2.reset_index()
df_tmp2['总流量(GB)'] = df_tmp2['总流量(GB)'].map(lambda x:round(x,1))

st.header('{coun}县各支局全天总流量(GB)'.format(coun = country))
fig = plt.figure(figsize=(10,8))
bar_labels = df_tmp2['支局'].values
y_pos = np.arange(len(bar_labels))
data = df_tmp2['总流量(GB)'].values
plt.yticks(y_pos, bar_labels, fontsize=14)
bars = plt.barh(y_pos,data,alpha = 0.5,color='g')
for b,d in zip(bars,data):
    plt.text(b.get_width()+b.get_width()*0.05,b.get_y()+b.get_height()/2,'{}'.format(d))
st.pyplot()

y = df_suboffice_uesr[(df_suboffice_uesr['区县'] == country)&(df_suboffice_uesr['支局'] == suboffice)]

st.header('{sub}支局全天用户数变化情况'.format(sub = suboffice))
y1 = y['用户数'].T.values
x1 = y['时间'].T.values
plt.figure(figsize=(12, 4))
plt.xticks(range(len(x1)), x1,fontsize=14)
plt.plot(range(len(x1)),y1,label='用户数',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=6)
for a,b in zip(range(len(x1)),y1):
    plt.text(a,b*1.001,  '%d' % b, ha='center', va= 'bottom',fontsize=12)
plt.xlabel('时间')
plt.ylabel('用户数')
plt.legend(loc='center right')
st.pyplot()

y = df_suboffice_flow[(df_suboffice_flow['区县'] == country)&(df_suboffice_flow['支局'] == suboffice)]
y['总流量(GB)'] = y['总流量(GB)'].map(lambda x:round(x,1))

st.header('{sub}支局全天流量变化情况(GB)'.format(sub = suboffice))
y1 = y['总流量(GB)'].T.values
x1 = y['时间'].T.values
plt.figure(figsize=(12, 6))
plt.xticks(range(len(x1)), x1,fontsize=14)
plt.plot(range(len(x1)),y1,label='总流量(GB)',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=6)
for a,b in zip(range(len(x1)),y1):
    plt.text(a,b*1.001,  '%d' % b, ha='center', va= 'bottom',fontsize=12)
plt.xlabel('时间')
plt.ylabel('总流量(GB)')
plt.legend(loc='center right')
st.pyplot()

df_sub = df_user_busy[(df_user_busy['区县'] ==country)&(df_user_busy['支局'] == suboffice)]

st.header('{sub}支局用户数最多top20小区'.format(sub = suboffice))
df_tmp = df_sub.head(20)
fig = plt.figure(figsize=(10,5))
bar_labels = df_tmp['中文站名'].values[::-1]
y_pos = np.arange(len(df_tmp))
data = df_tmp['用户数'].values[::-1]
plt.yticks(y_pos, bar_labels, fontsize=9)
bars = plt.barh(y_pos , data , alpha = 0.5,color='g')
for b,d in zip(bars,data):
    plt.text(b.get_width()+b.get_width()*0.05,b.get_y()+b.get_height()/2,'{}'.format(d))
st.pyplot()

df_sub = df_flow_busy[(df_flow_busy['区县'] ==country)&(df_flow_busy['支局'] == suboffice)]

st.header('{sub}支局流量top20小区(GB)'.format(sub = suboffice))
df_sub.sort_values(by='总流量(GB)', ascending= False, inplace=True)
df_sub['总流量(GB)'] = df_sub['总流量(GB)'].map(lambda x:round(x,1))
df_tmp =df_sub.head(20)
fig = plt.figure(figsize=(10,5))
bar_labels = df_tmp['中文站名'].values[::-1]
y_pos = np.arange(len(df_tmp))
data = df_tmp['总流量(GB)'].values[::-1]
plt.yticks(y_pos, bar_labels, fontsize=9)
bars = plt.barh(y_pos,data,alpha = 0.5,color='g')
for b,d in zip(bars,data):
    plt.text(b.get_width()+b.get_width()*0.05,b.get_y()+b.get_height()/2,'{}'.format(d))
st.pyplot()


st.header('{coun}支局无线带宽利用率最高top20小区(%)'.format(coun = country))
df_sub.sort_values(by='PRB利用率', ascending= False, inplace=True)
df_sub['PRB利用率'] = df_sub['PRB利用率'].map(lambda x:round(x,1))
df_tmp =df_sub.head(20)
fig = plt.figure(figsize=(10,5))
bar_labels = df_tmp['中文站名'].values[::-1]
y_pos = np.arange(len(df_tmp))
data = df_tmp['PRB利用率'].values[::-1]
plt.yticks(y_pos, bar_labels, fontsize=9)
bars = plt.barh(y_pos,data,alpha = 0.5,color='g')
for b,d in zip(bars,data):
    plt.text(b.get_width()+b.get_width()*0.05,b.get_y()+b.get_height()/2,'{}'.format(d))
st.pyplot()

st.header('{coun}支局忙时体验速率最差top20小区(Mbps)'.format(coun = country))
df_sub.sort_values(by='体验速率', ascending= True, inplace=True)
df_sub =df_sub[(df_sub['体验速率']>0)&~(df_sub['体验速率'].isnull())]
df_sub['体验速率'] = df_sub['体验速率'].map(lambda x:round(x,1))
df_tmp =df_sub.head(20)
fig = plt.figure(figsize=(10,5))
bar_labels = df_tmp['中文站名'].values[::-1]
y_pos = np.arange(len(df_tmp))
data = df_tmp['体验速率'].values[::-1]
plt.yticks(y_pos, bar_labels, fontsize=9)
bars = plt.barh(y_pos,data,alpha = 0.5,color='g')
for b,d in zip(bars,data):
    plt.text(b.get_width()+b.get_width()*0.05,b.get_y()+b.get_height()/2,'{}'.format(d))
st.pyplot()


