# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 10:50:17 2020

@author: Administrator
"""

import pandas as pd
import os
from tqdm import tqdm

def read_csv_partly(file):
    import pandas as pd
    file_data = pd.read_csv(file, engine='python', encoding='utf-8', chunksize=100000)
    for df_tmp in file_data:
        yield df_tmp

work_path = 'D:/2020年工作/2020年4月中兴LTE邻区专项优化/'
os.chdir(work_path)
if not os.path.exists('./结果输出'):
    os.mkdir('./结果输出')
if not os.path.exists('./脚本输出'):
    os.mkdir('./脚本输出')

df_ext_info = pd.read_csv('./结果输出/外部邻区_info.csv')
df_ext_info['Ncell'] = df_ext_info['eNBId'].map(str) + '_' +df_ext_info['cellLocalId'].map(str)
df_ext = pd.concat([x for x in tqdm(read_csv_partly('./结果输出/外部邻区.csv'))],axis =0)

df_rela = pd.concat([x for x in tqdm(read_csv_partly('./结果输出/邻接关系.csv'))],axis =0)

df_add = pd.read_csv('./结果输出/添加邻区.csv',engine = 'python')
df_add['ext_ind'] = df_add['Scell'].map(lambda x:x.split('_')[0]) + '-'+df_add['Ncell']

df_add_extcell = df_add[~df_add['ext_ind'].isin(df_ext['ext_ind'])]
df_add_extcell = pd.merge(df_add_extcell[['Scell','Ncell']],df_ext_info,how ='left', on = 'Ncell')
df_tmp = df_add_extcell[pd.isnull(df_add_extcell['SubNetwork'])]

with open('./脚本输出/无信息.csv','w',newline = '') as f:
    df_tmp.to_csv(f,index=False)

with pd.ExcelWriter('./脚本输出/添加邻接关系.xlsx') as f:
    df_add_extcell.to_exce(f,'ExternalEUtranCellFDD',index=False)
    df_add_relation.to_exce(f,'EUtranRelation',index=False)
