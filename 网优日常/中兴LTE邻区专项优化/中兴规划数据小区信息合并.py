# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 17:40:50 2020

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

files =os.listdir('./规划数据导出')

file_cell_sheets = []
for file in tqdm(files):
    with pd.ExcelFile('./规划数据导出/'+file) as df:
        df_tmp = pd.read_excel('./规划数据导出/'+file,encoding = 'gbk', sheet_name = 'EUtranCellFDD')
        df_tmp.drop(index = [0,1,2,3],inplace = True)
        file_cell_sheets.append(df_tmp)

df_cell = pd.concat(file_cell_sheets,axis =0)

with open('./结果输出/小区信息.csv', 'w', newline = '', encoding = 'utf-8') as f:
    df_cell.to_csv(f,index =False)

df_cell = pd.concat([x for x in tqdm(read_csv_partly('./结果输出/小区信息.csv'))],axis =0)
