# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 11:00:10 2020

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 16:16:05 2020

@author: Administrator
"""


import pandas as pd
import os

substution_list = [
    '双龙',
    '南宁',
    '寥廓',
    '古城',
    '丹凤',
    '开发区',
    '乐熙',
    '宛水',
    '中安',
    '老城',
    '松毛山',
    '祥宁',
    '宝云',
    '西宁',
    '潇湘',
    '太和',
    '启秀',
    '文华',
    '建宁',
    '白石江',
    '胜境',
    '西关',
    '宛水']

work_path = r'D:\2020年工作\2020年投诉用户终端分析'
os.chdir(work_path)
df = pd.read_excel('曲靖投诉用户流量top5小区.xlsx')

df_user = pd.read_excel('曲靖1-4月投诉号码4776.xlsx')
df_user_count = df_user['曲靖投诉号码'].value_counts()
dict_user_count = df_user_count.to_dict()

df_substution = pd.read_excel('物理站址关联支局清单.xlsx')

df_substution.columns
df_substution['ENODEBID'] = df_substution['小区号'].map(lambda x: x.split('_')[0])
df_substution['CELLID'] = df_substution['小区号'].map(lambda x: x.split('_')[1])
df_substution['ENODEBID'] = df_substution['ENODEBID'].astype(int)
df_substution['CELLID'] = df_substution['CELLID'].astype(int)
df_substution['ECI'] = df_substution['ENODEBID'] * 256 + df_substution['CELLID']

df_substution.set_index('ECI', inplace=True)
dict_enb = df_substution['ENODEBID'].to_dict()
dict_cellid = df_substution['CELLID'].to_dict()

df_substution.set_index('小区号', inplace=True)
country_dict = df_substution['区县'].to_dict()
substution_dict = df_substution['支局'].to_dict()
name_dict = df_substution['中文站名'].to_dict()

df['小区'] = df['小区'].astype(str)
df['ECI'] = df['小区'].map(lambda x: x[6:])
df['ECI'] = df['ECI'].astype(int)

df['eNodeBID'] = df['ECI'].map(dict_enb)
df['CELLID'] = df['ECI'].map(dict_cellid)
df['cell_index'] = df['eNodeBID'].map(lambda x: str(
    x)[:-2]) + '_' + df['CELLID'].map(lambda x: str(x)[:-2])
df['中文站名'] = df['cell_index'].map(name_dict)

df['区县'] = df['cell_index'].map(country_dict)
df['支局'] = df['cell_index'].map(substution_dict)
df = df[~df['CELLID'].isnull()]
df.set_index('cell_index', inplace=True)
cell_flow_dict = df['小区流量'].to_dict()
df.reset_index(inplace=True)
df_gr = df.groupby(['号码', 'IMEI', '区县', '支局', '终端厂家', '终端型号',
                    'cell_index', '中文站名'], as_index=False)['总流量'].sum()
df_gr.sort_values(['号码', '总流量'], ascending=[True, False], inplace=True)
df_gr = df_gr.groupby(['号码'], as_index=False).head(3)
df_gr['小区流量'] = df_gr['cell_index'].map(cell_flow_dict)
df_gr['小区流量'] = (round(df_gr['小区流量'] / (1024 * 1024), 1))
df_gr['总流量'] = (round(df_gr['总流量'] / (1024 * 1024), 1))


df_gr['历史投诉次数'] = df_gr['号码'].map(dict_user_count)
df_gr.sort_values(['历史投诉次数'], ascending=[False], inplace=True)
df_gr['城区农村'] = ''
df_gr['城区农村'][df_gr['支局'].isin(substution_list)] = '城区'
df_gr['城区农村'][~df_gr['支局'].isin(substution_list)] = '农村'
df_city_country =  df_gr.groupby(['城区农村'], as_index=False)['号码'].count()
df_city_country.rename(columns={'号码': '数量'}, inplace=True)
df_city_country['百分比'] = round(df_city_country['数量']/df_city_country['数量'].sum(),1)*100
df_city_country['百分比'] =df_city_country['百分比'].map(str)+'%'

df_mobile = df.groupby(['终端厂家', '终端型号'], as_index=False)['号码'].count()
df_mobile.rename(columns={'号码': '数量'}, inplace=True)
df_mobile['百分比'] = round(df_mobile['数量']/df_mobile['数量'].sum(),3)*100
df_mobile['百分比'] =df_mobile['百分比'].map(str)+'%'
df_mobile.sort_values(['数量'], ascending=[False], inplace=True)

df_substution = df_gr.groupby(['区县', '支局'], as_index=False)['号码'].count()
df_substution.rename(columns={'号码': '数量'}, inplace=True)
df_substution['百分比'] = round(df_substution['数量']/df_substution['数量'].sum(),3)*100
df_substution['百分比'] =df_substution['百分比'].map(str)+'%'
df_substution.sort_values(['数量'], ascending=[False], inplace=True)

df_country = df_gr.groupby(['区县'], as_index=False)['号码'].count()
df_country.rename(columns={'号码': '数量'}, inplace=True)
df_country['百分比'] = round(df_country['数量']/df_country['数量'].sum(),2)*100
df_country['百分比'] =df_country['百分比'].map(str)+'%'
df_country.sort_values(['数量'], ascending=[False], inplace=True)

with pd.ExcelWriter('1-4月投诉用户终端分析.xlsx') as f:
    df_city_country.to_excel(f, '按区域类型统计', index=False)
    df_country.to_excel(f, '按区县统计', index=False)
    df_substution.to_excel(f, '按支局统计', index=False)
    df_mobile.to_excel(f, '按终型号端统计', index=False)
    df_gr.to_excel(f, '所有用户清单', index=False)
