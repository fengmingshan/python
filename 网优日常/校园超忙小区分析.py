# -*- coding: utf-8 -*-
# @Author: fengmingshan
# @Date:   2019-09-02 15:15:02
# @Last Modified by:   Administrator
# @Last Modified time: 2019-09-02 15:47:05

import pandas as pd
import numpy as np
import os

data_path = 'd:/2019年工作/2019年9月校园超忙小区分析/'
file = '能源学校_曲靖KPI指标_08-29_09.02.csv'
df_content = pd.read_csv(data_path + file, engine='python', skiprows=5)

df_content = df_content[['开始时间', '结束时间', '网元', '网元名称', '小区', '小区名称', '空口上行用户面流量（MByte）_1', '空口下行用户面流量（MByte）_1477070755617-11',
                         '分QCI用户体验下行平均速率（Mbps）_1', '下行PRB平均占用率_1', 'PDCCH信道CCE占用率_1', '最大RRC连接用户数_1', '平均RRC连接用户数_1', '下行平均激活用户数_1', '最大激活用户数_1', 'CQI优良比(>=7比例)']]
df_users = df_content.pivot_tabke()