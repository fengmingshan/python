# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 09:01:14 2020

@author: Administrator
"""

"""
命令样例
Set PakList:ISDN=8618087366487,PAKINSTIDLIST=710104857952,PAKNameList=800000,PBEGINDATEList=20200311130751,PENDDATEList=20200311133751;

源对应关系
ISDN=ISDN
PAKID=PAKNameList
PAKINSTID=PAKINSTIDLIST
PBEGINDATEList=有效期结束时间
"""

import pandas as pd
import numpy as np
import os
import sys

work_path = 'D:/_python/python/网优日常/修改套餐失效日期脚本'

os.chdir(work_path)
if not os.path.exists('结果输出'):
    os.mkdir('结果输出')

files = os.listdir()
user_files = [x for x in files if ('.py' not in x and os.path.isfile(x))]

df_list = []
for file in user_files:
    df_tmp = pd.read_csv(file, engine='python', encoding='utf-8')
    df_tmp1 = df_tmp[['ISDN', 'PAKID']]
    df_tmp1 = df_tmp1.drop('PAKID', axis=1).join(df_tmp1['PAKID'].str.split(
        '$', expand=True).stack().reset_index(level=1, drop=True).rename('PAKID'))
    df_tmp2 = df_tmp['PAKINSTID'].str.split('$', expand=True).stack(
    ).reset_index(level=1, drop=True).rename('PAKINSTID')
    df_tmp3 = df_tmp['BEGINDATE'].str.split('$', expand=True).stack(
    ).reset_index(level=1, drop=True).rename('BEGINDATE')
    df_tmp4 = df_tmp['ENDDATE'].str.split('$', expand=True).stack(
    ).reset_index(level=1, drop=True).rename('ENDDATE')
    df_tmp = pd.concat([df_tmp1, df_tmp2, df_tmp3, df_tmp4], axis=1)
    df_list.append(df_tmp)

df = pd.concat(df_list, axis=1)
df.reset_index(drop=True, inplace=True)
df['BEGINDATE'] = df['BEGINDATE'].map(
    lambda x: x.replace('-', '').replace(' ', '').replace(':', ''))
df['ENDDATE'] = df['ENDDATE'].map(lambda x: x.replace('-', '').replace(' ', '').replace(':', ''))

while True:
    try:
        invalid_date = str(input('请输入失效时间，格式为20200311130751，长度为14位: '))
        if len(invalid_date) == 14 and invalid_date.isdigit():
            df['invalid_date'] = invalid_date
            print('你输入的时间是：' + invalid_date)
            break
    except:
        print('您输入的日期不合规,格式为20200311130751,请重新输入: ')

df_78 = df[(df['PAKID'] == '70000') | (df['PAKID'] == '80000')]

with open('./结果输出/回滚脚本.txt', 'w') as f:
    for i in range(len(df_78)):
        line = 'Set PakList:ISDN={ISDN},PAKINSTIDLIST={PAKINSTID},PAKNameList={PAKID},PBEGINDATEList={BEGINDATE},PENDDATEList={ENDDATE};'.format(
            ISDN = df_78.loc[i, 'ISDN'], PAKINSTID = df_78.loc[i, 'PAKINSTID'], PAKID = df_78.loc[i, 'PAKID'], BEGINDATE=df_78.loc[i, 'BEGINDATE'], ENDDATE=df_78.loc[i, 'ENDDATE'])
        f.writelines(line + '\n')

with open('./结果输出/割接脚本.txt', 'w') as f:
    for i in range(len(df_78)):
        line = 'Set PakList:ISDN={ISDN},PAKINSTIDLIST={PAKINSTID},PAKNameList={PAKID},PBEGINDATEList={BEGINDATE},PENDDATEList={ENDDATE};'.format(
            ISDN = df_78.loc[i, 'ISDN'], PAKINSTID = df_78.loc[i, 'PAKINSTID'], PAKID = df_78.loc[i, 'PAKID'], BEGINDATE=df_78.loc[i, 'BEGINDATE'], ENDDATE=df_78.loc[i, 'invalid_date'])
        f.writelines(line + '\n')

