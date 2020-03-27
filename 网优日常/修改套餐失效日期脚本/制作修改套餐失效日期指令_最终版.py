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
from math import ceil


def read_csv_partly(file,names):
    file_data = pd.read_csv(file, engine='python', encoding='utf-8', chunksize=100000)
    for df_tmp in file_data:
        yield df_tmp


def split_to_mutilines(df, col):
    df_tmp = df[col].str.split('$', expand=True).stack(
    ).reset_index(level=1, drop=True).rename(col)
    return df_tmp


while True:
    try:
        invalid_date = str(input('请输入失效时间，格式为20200311130751，长度为14位: '))
        if len(invalid_date) == 14 and invalid_date.isdigit():
            print('你输入的时间是：' + invalid_date)
            break
    except BaseException:
        print('您输入的日期不合规,格式为 20200311130751 ,请重新输入: ')


work_path = 'D:/_python/python/网优日常/修改套餐失效日期脚本'
os.chdir(work_path)
if not os.path.exists('结果输出'):
    os.mkdir('结果输出')

files = os.listdir()
user_files = [x for x in files if ('.py' not in x and os.path.isfile(x))]
print('共发现{}个原始文件!'.format(len(user_files)))
# 迭代打开文件，每一个文件对应一张表格
list_df_file = []
list_df_lose = []
for i, file in enumerate(user_files):
    list_df_tmp = []
    list_lost_tmp = []
    for j, df_chunk in enumerate(read_csv_partly(file)):
        df_lose_tmp = df_chunk[pd.isnull(df_chunk.ISDN) | pd.isnull(df_chunk.PAKID) | pd.isnull(
            df_chunk.PAKINSTID) | pd.isnull(df_chunk.BEGINDATE) | pd.isnull(df_chunk.ENDDATE)]
        df_chunk = df_chunk[~pd.isnull(df_chunk.ISDN) & ~pd.isnull(df_chunk.PAKID) & ~pd.isnull(
            df_chunk.PAKINSTID) & ~pd.isnull(df_chunk.BEGINDATE) & ~pd.isnull(df_chunk.ENDDATE)]
        df_tmp1 = df_chunk['ISDN'].to_frame()
        df_tmp2 = split_to_mutilines(df_chunk, 'PAKID')
        df_tmp3 = split_to_mutilines(df_chunk, 'PAKINSTID')
        df_tmp4 = split_to_mutilines(df_chunk, 'BEGINDATE')
        df_tmp5 = split_to_mutilines(df_chunk, 'ENDDATE')
        df_tmp = df_tmp1.join(df_tmp2)
        df_tmp = pd.concat([df_tmp, df_tmp3, df_tmp4, df_tmp5], axis=1)
        list_df_tmp.append(df_tmp)
        if len(df_lose_tmp) > 0:
            list_lost_tmp.append(df_lose_tmp)
        print('读取:{}W 行!'.format((j + 1) * 10))
    df_file = pd.concat(list_df_tmp, axis=0)
    if len(list_lost_tmp) > 0:
        df_lose_file = pd.concat(list_lost_tmp, axis=0)
    list_df_file.append(df_file)
    if len(list_lost_tmp) > 0:
        list_df_lose.append(df_lose_file)
    print('完成第{}个文件，共{}行!'.format(i + 1, len(df_file)))

# 将所有打开文件产生的表格合并成一张表
if len(list_df_file) > 1:
    df = pd.concat(list_df_file, axis=0)
else:
    df = df_file

if len(list_df_lose) > 1:
    df_lose = pd.concat(list_df_lose, axis=0)
else:
    df_lose = df_lose_file

df.reset_index(drop=True, inplace=True)
df['invalid_date'] = invalid_date
df['BEGINDATE'] = df['BEGINDATE'].map(
    lambda x: x.replace('-', '').replace(' ', '').replace(':', ''))
df['ENDDATE'] = df['ENDDATE'].map(lambda x: x.replace('-', '').replace(' ', '').replace(':', ''))

df_78 = df[(df['PAKID'] == '70000') | (df['PAKID'] == '80000')]

with open('./结果输出/回滚脚本.txt', 'w') as f:
    for i in range(ceil(len(df_78) / 200000)):
        if (i + 1) * 200000 < len(df_78):
            line_list = ['Set PakList:ISDN={ISDN},PAKINSTIDLIST={PAKINSTID},PAKNameList={PAKID},PBEGINDATEList={BEGINDATE},PENDDATEList={ENDDATE};'.format(ISDN=isdn, PAKINSTID=pakinsrid, PAKID=pakid, BEGINDATE=begindate, ENDDATE=endate) for isdn, pakinsrid, pakid, begindate, endate in zip(
                df_78.ISDN[i * 200000: (i + 1) * 200000], df_78.PAKINSTID[i * 200000: (i + 1) * 200000], df_78.PAKID[i * 200000: (i + 1) * 200000], df_78.BEGINDATE[i * 200000: (i + 1) * 200000], df_78.ENDDATE[i * 200000: (i + 1) * 200000])]
        elif (i + 1) * 200000 >=  len(df_78):
            line_list = ['Set PakList:ISDN={ISDN},PAKINSTIDLIST={PAKINSTID},PAKNameList={PAKID},PBEGINDATEList={BEGINDATE},PENDDATEList={ENDDATE};'.format(ISDN=isdn, PAKINSTID=pakinsrid, PAKID=pakid, BEGINDATE=begindate, ENDDATE=endate) for isdn, pakinsrid, pakid, begindate, endate in zip(
                df_78.ISDN[i * 200000: len(df_78)], df_78.PAKINSTID[i * 200000: len(df_78)], df_78.PAKID[i * 200000: len(df_78)], df_78.BEGINDATE[i * 200000: len(df_78)], df_78.ENDDATE[i * 200000:len(df_78)])]
        lines = '\n'.join(line_list)
        f.writelines(lines + '\n')
        print('制作回滚脚本，总共{}行，已写入{}行，剩余{}行'.format(len(df_78),
                                                 (i + 1) * 200000, len(df_78) - (i + 1) * 200000))

with open('./结果输出/割接脚本.txt', 'w') as f:
    for i in range(ceil(len(df_78) / 200000)):
        if (i + 1) * 200000 < len(df_78):
            line_list = ['Set PakList:ISDN={ISDN},PAKINSTIDLIST={PAKINSTID},PAKNameList={PAKID},PBEGINDATEList={BEGINDATE},PENDDATEList={ENDDATE};'.format(ISDN=isdn, PAKINSTID=pakinsrid, PAKID=pakid, BEGINDATE=begindate, ENDDATE=endate) for isdn, pakinsrid, pakid, begindate, endate in zip(
                df_78.ISDN[i * 200000: (i + 1) * 200000], df_78.PAKINSTID[i * 200000: (i + 1) * 200000], df_78.PAKID[i * 200000: (i + 1) * 200000], df_78.BEGINDATE[i * 200000: (i + 1) * 200000], df_78.invalid_date[i * 200000: (i + 1) * 200000])]
        elif (i + 1) * 200000 >=  len(df_78):
            line_list = ['Set PakList:ISDN={ISDN},PAKINSTIDLIST={PAKINSTID},PAKNameList={PAKID},PBEGINDATEList={BEGINDATE},PENDDATEList={ENDDATE};'.format(ISDN=isdn, PAKINSTID=pakinsrid, PAKID=pakid, BEGINDATE=begindate, ENDDATE=endate) for isdn, pakinsrid, pakid, begindate, endate in zip(
                df_78.ISDN[i * 200000: len(df_78)], df_78.PAKINSTID[i * 200000: len(df_78)], df_78.PAKID[i * 200000: len(df_78)], df_78.BEGINDATE[i * 200000: len(df_78)], df_78.invalid_date[i * 200000:len(df_78)])]
        lines = '\n'.join(line_list)
        f.writelines(lines + '\n')
        print('制作割接脚本，总共{}行，已写入{}行，剩余{}行'.format(len(df_78),
                                                 (i + 1) * 200000, len(df_78) - (i + 1) * 200000))

with open('./结果输出/缺失数据.csv', 'w', newline='') as writer:
    df_lose.to_csv(writer, index=False)

out_path = work_path + '/结果输出'
print('*'*60)
print('脚本已输出到{}：回滚脚本.txt 、割接脚本.txt ,请到对应文件夹查看!'.format(out_path))
print('*'*60)
print('共有{}行数据有缺失无法处理,请查看：缺失数据.csv !'.format(len(df_lose)))

os.startfile(out_path)
