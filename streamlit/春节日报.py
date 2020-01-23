# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 23:29:41 2020

@author: Administrator
"""

import streamlit as st
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

path = 'D:/Test'
os.chdir(path)
df = pd.read_excel('./日报原始数据.xlsx')

today = datetime.today().strftime("%Y-%m-%d")

option = st.sidebar.selectbox(
    '你要查看那个县的报表?',
     ['麒麟','沾益','马龙','陆良','师宗','罗平','宣威','会泽','富源'])

st.title('春节期间4G话务日报 {day}'.format(day = today))
'你选择的是：', option
country = option

df_tmp = df[df['区县'] == country]
substation = df_tmp['支局'].unique()

option = st.sidebar.selectbox(
    '你要查看那个支局的报表?',
     substation)

st.header('{coun}县全天用户变化情况'.format(coun = country))


st.header('{coun}县各支局用户数'.format(coun = country))

df_provit = df_tmp.groupby(by = '支局')['忙时RRC最大连接用户数'].sum()
df_provit = df_provit.reset_index()
df_provit.sort_values(by='忙时RRC最大连接用户数', ascending=True, inplace=True)


fig = plt.figure(figsize=(10,8))
bar_labels = df_provit['支局'].values
y_pos = np.arange(len(bar_labels))
data = df_provit['忙时RRC最大连接用户数'].values
plt.yticks(y_pos, bar_labels, fontsize=16)
bars = plt.barh(y_pos,data,alpha = 0.5,color='g')
for b,d in zip(bars,data):
    plt.text(b.get_width()+b.get_width()*0.05,b.get_y()+b.get_height()/2,'{}'.format(d))
st.pyplot()

st.header('{coun}县各支局用户数占比'.format(coun = country))

fig = plt.figure(figsize=(20,20))
labels = df_provit['支局'].values
sizes = [x/sum(df_provit['忙时RRC最大连接用户数']) for x in df_provit['忙时RRC最大连接用户数']]
plt.pie(sizes,labels=labels,autopct='%1.1f%%',shadow=False,startangle=150,textprops={'fontsize':30,'color':'black'})
plt.title("各支局用户数占比（%）",fontsize=40)
plt.axis('equal')
st.pyplot()



st.header('{coun}县各支局流量'.format(coun = country))


st.header('{coun}县各支局PRB利用率'.format(coun = country))
