# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 14:18:41 2020

@author: Administrator
"""
import pandas as pd
import os

path = 'D:/2020年工作/2020年1月春节返乡用户分析'
os.chdir(path)

df = pd.read_excel('./曲靖返乡用户v2.xlsx',skiprows =1, header = None,names= ['手机号', '终端', '归属省', '归属地市', 'CID', '总流量(MB)', '在本小区驻留天数'])

df['CID'] = df['CID'].map(lambda x: int(str(x)[6:]))

df_cell_info = pd.read_excel('./物理站址与支局对应清单.xlsx')
df_cell_info['eNodeB'] = df_cell_info['小区号'].map(lambda x: int(x.split('_')[0]))
df_cell_info['cell'] = df_cell_info['小区号'].map(lambda x: int(x.split('_')[1]))
df_cell_info['CID'] = df_cell_info['eNodeB'] * 256 + df_cell_info['cell']

df_user = pd.merge(df, df_cell_info, how='left', on='CID')
df_user = df_user[~df_user['支局'].isnull()]
df_user.sort_values(by=['手机号', '在本小区驻留天数'], ascending=[True, False], inplace=True)  # 按时间顺序升序排列
df_user.reset_index(inplace=True, drop=True)
df_user['总流量(MB)'] = df_user['总流量(MB)'] / (1024 * 1024)
df_user['总流量(MB)'] = round(df_user['总流量(MB)'], 1)
df_user = df_user[['手机号', '终端', '归属省', '归属地市', '总流量(MB)', '小区号',
                   '中文站名', '区县', '区域', '频段', '支局', '在本小区驻留天数', 'eNodeB', 'cell']]

df_substation = df_user.groupby(by=['手机号', '支局'], as_index=False)['在本小区驻留天数'].max()
df_substation.sort_values(by=['手机号', '在本小区驻留天数'], ascending=[True, False], inplace=True)
df_substation.rename(columns = {'在本小区驻留天数':'近7天在本支局驻留天数'}, inplace=True)

df_user = pd.merge(df_user, df_substation, how='left', on=['手机号', '支局'])
df_user.sort_values(by=['手机号','近7天在本支局驻留天数', '支局'],
                    ascending=[True, False, True], inplace=True)

df_flow = df_user.groupby(by='手机号', as_index=False)['总流量(MB)'].sum()
df_flow = df_flow.set_index('手机号')
flow_dict = df_flow['总流量(MB)'].to_dict()

df_home = df_user.groupby(by='手机号', as_index=False).head(1)
df_home['周总流量(MB)'] = df_home['手机号'].map(flow_dict)

df_home = df_home[df_home['近7天在本支局驻留天数']>=6]

with pd.ExcelWriter('./结果输出/全市总表.xlsx') as writer:
    df_home.to_excel(writer, index=False)

country_set = set(df_home.区县)
for country in country_set:
    with pd.ExcelWriter('./结果输出/' + country + '_清单.xlsx') as writer:
        df_country = df_home[df_home['区县'] == country]
        df_country.to_excel(writer, country + '县总', index=False)
        town_set = set(df_country.支局)
        for town in town_set:
            df_town = df_country[df_country['支局'] == town]
            df_town.to_excel(writer, town, index=False)
