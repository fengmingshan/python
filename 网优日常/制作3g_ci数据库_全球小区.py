# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-09-20 16:21:24
# @Last Modified by:   Administrator
# @Last Modified time: 2019-09-20 16:27:40


import pandas as pd
import os

data_path = 'D:/Test/3GCI数据库制作'
ci_file = 'MSCE3--全球小区_1.XLS'

os.chdir(data_path)
df_ci = pd.read_excel(ci_file)
df_ci['全球小区号'] = df_ci['全球小区号'].apply(
    lambda x: x.split('(')[1].replace(')', ''))
df_ci = df_ci[['BSC局号', '虚拟MSC索引', 'MSCID索引', '移动国家码', '移动网号', '位置区识别码', '全球小区号', '类型',
       '边界区标识', '边界区名称', '地域', '备份局局向号', '全球小区名称', '纬度(类型-度-分-秒)',
       '经度(类型-度-分-秒)', '区域编号']]
with  pd.ExcelWriter( '全球小区.xls')  as writer:  #输出到excel
    df_ci.to_excel(writer,'全球小区',index = False)

