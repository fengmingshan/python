# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-09-23 11:29:27
# @Last Modified by:   Administrator
# @Last Modified time: 2019-09-24 17:12:42

import pandas as pd
import os
path = 'd:/2019年工作/2019年9月集团无线网优工作巡查/_备查资料汇总/基站巡检记录表_2019'
os.chdir(path)

files = os.listdir(path)

def month_2_quarter(month):
    if month in ['01','02','03']:
         quarter = '一季度'
    elif month in ['04','05','06']:
         quarter = '二季度'
    elif month in ['07','08','09']:
         quarter = '三季度'
    else:
        quarter = '四季度'
    return quarter

bts_quarter_list = [x.split('_')[0] +' '+ month_2_quarter(x.split('_')[1][5:7]) for x in files]

df1 = pd.DataFrame()
for i , bts_quarter in enumerate(bts_quarter_list):
    df1.loc[i,'站址名称'] = bts_quarter_list[i].split(' ')[0]
    df1.loc[i,'季度巡检次数'] = bts_quarter_list.count(bts_quarter)
    df1.loc[i,'站址_月'] = bts_quarter
    df1.loc[i,'文件名称'] = files[i]

df_twice = df1[df1['季度巡检次数'] > 1]
df_res = pd.DataFrame()
reset_index = pd.DataFrame.reset_index()
drop = pd.DataFrame.drop()
for item in df_twice['站址_月'].unique():
    df_tmp = df_twice[df_twice['站址_月']==item]
    reset_index(df_tmp,inplace =True)
    drop(df_tmp,'index',axis =1)
    df_res = df_res.append(df_tmp.loc[0])

with pd.ExcelWriter('_数量统计.xlsx')as writer:
    df_res.to_excel(writer,'巡检数量统计', index = False)


