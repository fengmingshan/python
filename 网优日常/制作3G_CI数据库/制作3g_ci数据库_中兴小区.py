# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-09-20 16:21:24
# @Last Modified by:   Administrator
# @Last Modified time: 2019-09-20 16:27:40

import pandas as pd
import os

data_path = 'D:/_python小程序/3GCI数据库制作'

os.chdir(data_path)
zte_files = [x for x in os.listdir('./data/') if '小区实体参数表' in x]
df_zte = pd.DataFrame()
for file in zte_files:
    df_tmp = pd.read_excel('./data/' + file, skiprows=1)
    df_zte = df_ci.append(df_tmp)

df_zte.rename(columns = {'ci':'全球小区号'},inplace=True)
df_zte['区县'] = df_zte['alias_b'].map(lambda x:x.split('QJ')[1][:2])
df_zte = df_zte[['bssid', '区县', 'system', 'cellid', 'sid', 'nid', 'lac',
                 '全球小区号', 'pilot_pn', 'alias_b', 'base_lat_b', 'base_long_b', 'btsalias']]
with open('./输出/中兴小区.csv', 'w', encoding='utf-8') as writer:  # 输出到excel
    df_zte.to_csv(writer, index=False)
