# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-09-12 09:48:12
# @Last Modified by:   Administrator
# @Last Modified time: 2019-09-12 11:00:39

import pandas as pd
import os

data_path = 'd:/Test/福彩用户分析'
os.chdir(data_path)

YN_lottery_file = '云南福彩清单2019-08.xlsx'
QJ_billing_file = '划小清单201908.csv'


df_billing = pd.read_csv(QJ_billing_file, engine='python')

df_billing = df_billing[~df_billing['用户号码'].map(
    lambda x:str(x)[:4] == '0874' or str(x)[:3] == '874')]
df_billing['号码位长'] = df_billing['用户号码'].apply(lambda x:len(x))

df_lottery = pd.read_excel(YN_lottery_file)
df_lottery = df_lottery[[
    '号码', '合账号码(计费)', '激活时间', '卡类型', '客户名称', '是否开通2G', '是否开通3G', '产品状态', '总流量']]
df_lottery = df_lottery[df_lottery['产品状态'] != '拆机']
df_QJ_lottery = df_lottery[df_lottery['号码'].isin(df_billing['用户号码'])]

df_duration = df_billing[df_billing['用户号码'].isin(
    df_QJ_lottery['号码'])][['用户号码', '上网时长']]

df_thoughtput = df_billing[df_billing['用户号码'].isin(
    df_QJ_lottery['号码'])][['用户号码', '上网流量']]

df_times = df_billing[df_billing['用户号码'].isin(
    df_QJ_lottery['号码'])][['用户号码', '上网次数']]

df_duration.set_index('用户号码',inplace = True)
dict_duration = df_duration['上网时长'].to_dict()
df_thoughtput.set_index('用户号码',inplace = True)
dict_thoughtput = df_thoughtput['上网流量'].to_dict()
df_times.set_index('用户号码',inplace = True)
dict_times = df_times['上网次数'].to_dict()

df_QJ_lottery['上网时长'] = df_QJ_lottery['号码'].map(dict_duration)
df_QJ_lottery['上网流量'] = df_QJ_lottery['号码'].map(dict_thoughtput)
df_QJ_lottery['上网次数'] = df_QJ_lottery['号码'].map(dict_times)

with pd.ExcelWriter('曲靖福彩数据.xlsx') as writer:
    df_QJ_lottery.to_excel(writer,index = False)





