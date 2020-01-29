# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-09-20 16:21:24
# @Last Modified by:   Administrator
# @Last Modified time: 2019-09-20 16:27:40

import pandas as pd
import os

data_path = 'D:/_python小程序/3GCI数据库制作'

os.chdir(data_path)
ci_files = [x for x in os.listdir('./data/') if '全球小区' in x]
df_ci = pd.DataFrame()
for file in ci_files:
    df_tmp = pd.read_excel('./data/' + file)
    df_ci = df_ci.append(df_tmp)

df_ci = df_ci[df_ci['BSC局号'].isin([1001,1002,1003])]
df_ci['全球小区号'] = df_ci['全球小区号'].apply(
    lambda x: x.split('(')[1].replace(')', ''))
df_ci = df_ci[['BSC局号', '虚拟MSC索引', 'MSCID索引', '移动国家码', '移动网号', '位置区识别码', '全球小区号', '类型',
       '边界区标识', '边界区名称', '地域', '备份局局向号', '全球小区名称', '纬度(类型-度-分-秒)',
       '经度(类型-度-分-秒)', '区域编号']]
with open( './输出/全球小区.csv','w',encoding ='utf-8')  as writer:  #输出到excel
    df_ci.to_csv(writer,index = False)

