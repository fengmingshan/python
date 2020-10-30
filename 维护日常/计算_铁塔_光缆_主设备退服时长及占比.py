# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 10:33:33 2020

@author: Administrator
"""


import os
import pandas as pd


path = r'D:\2020年工作\2020年维护指标年底收官\退服详单'
os.chdir(path)
df_not_choose = pd.read_excel('物理站址与铁塔站址对应关系信息表 （2020.10.14改）待确认.xlsx', sheet_name='曲靖')
df_not_choose = df_not_choose[df_not_choose['是否选择铁塔发电服务（2019年与铁塔签订，现实施中）']=='否']
list_not_choose = list(df_not_choose['铁塔站址编码'])

df = pd.read_excel('曲靖2020年9月故障明细记录表（合并）.xlsx', sheet_name='基站故障明细表')
df = df[(df['3G/LTE'].str.contains('LTE'))&(~df['站址编码'].isin(list_not_choose))]

df['故障中断历时（分钟）'].fillna(df['故障中断历时（分钟）'].mean(), inplace=True)
df_ab = df[(df['基站等级'] == 'A类站') | (df['基站等级'] == 'B类站')]
df_cd = df[(df['基站等级'] == 'C类站') | (df['基站等级'] == 'D类站')]
avg_ab = df_ab['故障中断历时（分钟）'].mean()
avg_cd = df_cd['故障中断历时（分钟）'].mean()


df_tower = df[(df['责任判断'] == '铁塔责任') & (df['3G/LTE'].str.contains('LTE'))]
df_equipment = df[(df['责任判断'] == '主设备责任') & (df['3G/LTE'].str.contains('LTE'))]
df_optical = df[(df['责任判断'] == '光缆组责任') & (df['3G/LTE'].str.contains('LTE'))]

df_tower_ab = df_tower[(df_tower['基站等级'] == 'A类站') | (df_tower['基站等级'] == 'B类站')]
df_tower_cd = df_tower[(df_tower['基站等级'] == 'C类站') | (df_tower['基站等级'] == 'D类站')]
tower_percentage_ab = sum(df_tower_ab['故障中断历时（分钟）']) / sum(df_ab['故障中断历时（分钟）'])
tower_ab = df_tower_ab['故障中断历时（分钟）'].mean()
tower_percentage_cd = sum(df_tower_cd['故障中断历时（分钟）']) / sum(df_cd['故障中断历时（分钟）'])
tower_cd = df_tower_cd['故障中断历时（分钟）'].mean()

df_optical_ab = df_optical[(df_optical['基站等级'] == 'A类站') | (df_optical['基站等级'] == 'B类站')]
df_optical_cd = df_optical[(df_optical['基站等级'] == 'C类站') | (df_optical['基站等级'] == 'D类站')]
optical_percentage_ab = sum(df_optical_ab['故障中断历时（分钟）']) / sum(df_ab['故障中断历时（分钟）'])
optical_ab = df_optical_ab['故障中断历时（分钟）'].mean()
optical_percentage_cd = sum(df_optical_cd['故障中断历时（分钟）']) / sum(df_cd['故障中断历时（分钟）'])
optical_cd = df_optical_cd['故障中断历时（分钟）'].mean()

df_equipment_ab = df_equipment[(df_equipment['基站等级'] == 'A类站') | (df_equipment['基站等级'] == 'B类站')]
df_equipment_cd = df_equipment[(df_equipment['基站等级'] == 'C类站') | (df_equipment['基站等级'] == 'D类站')]
equipment_percentage_ab = sum(df_equipment_ab['故障中断历时（分钟）']) / sum(df_ab['故障中断历时（分钟）'])
equipment_ab = df_equipment_ab['故障中断历时（分钟）'].mean()
equipment_percentage_cd = sum(df_equipment_cd['故障中断历时（分钟）']) / sum(df_cd['故障中断历时（分钟）'])
equipment_cd = df_equipment_cd['故障中断历时（分钟）'].mean()

