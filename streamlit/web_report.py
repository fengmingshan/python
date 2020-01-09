# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 23:52:22 2020

@author: Administrator
"""

import streamlit as st
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

path = 'D:/Test'
os.chdir(path)
df = pd.read_excel('./4G周报.xlsx')

df

st.title('话务周报2020年1月第一周')
st.header('各县总体情况')

st.subheader('一、总流量')
df[['总流量(TB)_上周','总流量(TB)_本周']].plot()
st.pyplot()

st.subheader('二、PRB利用率')
df[['下行PRB利用率_上周','下行PRB利用率_本周']].plot(kind='bar')
st.pyplot()

st.subheader('三、激活用户数')
df[['下行最大激活用户数_上周','下行最大激活用户数_本周']].plot(kind='bar')
st.pyplot()

radio = st.radio(
        '显示用户 体验速率 or 用户面时延',
        ('体验速率', '时延'))
if radio =='体验速率':
    df_speed = df[['用户体验速率_上周','用户体验速率_本周']]
    df_speed.plot(kind='bar')
    st.pyplot()
elif radio =='时延':
    df_time = df[['下行用户面时延_上周','下行用户面时延_本周']]
    df_time.plot(kind='bar')
    st.pyplot()

