# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 09:39:28 2020

@author: Administrator
"""

import pandas as pd
import numpy as np
import os

path = 'D:/2020年工作/2020年2月固定资产闲置'
os.chdir(path)

df = pd.read_excel('./移动资产_汇总.xlsx')
df.fillna('', inplace = True)
df['__最终处置情况'] = ''

df['资产名称'].unique()

len(df['__最终处置情况'][df['资产名称']== 'CDMA/PHS'])
len(df['__最终处置情况'][df['资产名称']== 'CDMA干放10W(A型)'])
len(df['__最终处置情况'][df['资产名称']== 'CDMA干放5W(B型)'])
len(df['__最终处置情况'][df['资产名称'].str.contains('TDD-')])
len(df['规格程式'].unique())
df_tmp = df[df['规格程式'].str.contains('改造')]
df_tmp = df[df['规格程式']=='35米']

df['__最终处置情况'][df['资产名称'].str.contains('微波')] = '闲置'
df['__最终处置情况'][df['资产名称']== 'wlan/(CDMA、PHS)'] = '闲置'
df['__最终处置情况'][df['资产名称']== 'CDMA/PHS'] = '闲置'
df['__最终处置情况'][df['资产名称']== '干放'] = '闲置'
df['__最终处置情况'][df['资产名称']== '宏蜂窝基站设备（MACROCELLBTS)'] = '闲置'
df['__最终处置情况'][df['资产名称'].str.contains('TDD-')] = '闲置'
df['__最终处置情况'][df['资产名称'].str.contains('干线放大器')] = '闲置'
df['__最终处置情况'][df['资产名称'].str.contains('全向天线')] = '闲置'
df['__最终处置情况'][df['资产名称'].str.contains('近端')] = '闲置'
df['__最终处置情况'][df['资产名称'].str.contains('远端')] = '闲置'
df['__最终处置情况'][df['资产名称'].str.contains('PHS')] = '闲置'
df['__最终处置情况'][df['资产名称'].str.contains('计算机终端')] = '闲置'
df['__最终处置情况'][df['资产名称'].str.contains('WLAN')] = '闲置'
df['__最终处置情况'][df['资产名称'].str.contains('基带处理板') & df['规格程式'].str.contains('CHD') = '闲置'
df['__最终处置情况'][df['规格程式'].str.contains('大唐')] = '闲置'
df['__最终处置情况'][df['规格程式'].str.contains('H型')] = '闲置'
df['__最终处置情况'][df['规格程式'].str.contains('围拢')] = '闲置'
df['__最终处置情况'][df['规格程式'].str.contains('围笼')] = '闲置'
df['__最终处置情况'][df['规格程式'].str.contains('30米')] = '闲置'
df['__最终处置情况'][df['规格程式'].str.contains('28m')] = '闲置'
df['__最终处置情况'][df['规格程式']=='35米'] = '闲置'
df['__最终处置情况'][df['规格程式'].str.contains('塔')] = '闲置'
df['__最终处置情况'][df['规格程式'].str.contains('拉线钢管')] = '闲置'
df['__最终处置情况'][df['规格程式'].str.contains('支臂')] = '闲置'
df['__最终处置情况'][df['规格程式'].str.contains('吨')] = '闲置'
df['__最终处置情况'][df['规格程式'].str.contains('吨')] = '闲置'
df['__最终处置情况'][df['规格程式'].str.contains('吨')] = '闲置'
df['__最终处置情况'][df['规格程式'].str.contains('吨')] = '闲置'

with pd.ExcelWriter('./无线资产确认结果.xlsx') as writer:
    df.to_excel(writer, index = False)
