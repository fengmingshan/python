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


work_path = 'D:/2020年工作/2020年4月4G邻区专项优化/'
os.chdir(work_path)
if not os.path.exists('./结果输出'):
    os.mkdir('./结果输出')

files =os.listdir('./规划数据导出')

file_relation_list = []
file_extcell_list = []
for file in tqdm(files):
    df = pd.ExcelFile('./规划数据导出/'+file)
    relation_sheets = [x for x in df.sheet_names if 'EUtranRelation' in x]
    extcell_sheets = [x for x in df.sheet_names if 'ExternalEUtranCellFDD' in x]

    relation_list = []
    for sheet in tqdm(relation_sheets):
        df_tmp = pd.read_excel('./规划数据导出/'+file,sheet_name = sheet)
        df_tmp.drop(index = [0,1,2,3],inplace = True)
        relation_list.append(df_tmp)

    extcell_list = []
    for sheet in tqdm(extcell_sheets):
        df_tmp = pd.read_excel('./邻区数据导出/'+file,sheet_name = sheet)
        df_tmp.drop(index = [0,1,2,3],axis = 0,inplace = True)
        extcell_list.append(df_tmp)

    df_relation_all = pd.concat(relation_list,axis = 0)
    df_extcell_all = pd.concat(extcell_list,axis = 0)
    file_relation_list.append(df_relation_all)
    file_extcell_list.append(df_extcell_all)

df_rela = pd.concat(file_relation_list,axis =0)
df_ext = pd.concat(file_extcell_list,axis =0)

df_rela = df_rela[['SubNetwork',
    'MEID',
    'CellId',
    'srcENBId',
    'mcc',
    'mnc',
    'eNBId',
    'NCellId',
    'isRemoveAllowed',
    'isHOAllowed',
    'userLabel',
    'shareCover',
    'qofStCell',
    'isAnrCreated',
    'isX2HOAllowed',
    'stateInd',
    'nCelPriority',
    's1DataFwdFlag',
    'cellIndivOffset',
    'coperType',
    'radioMode',
    'overlapCoverage']]

df_ext.drop_duplicates(['eNBId','cellLocalId'],inplace =True)
df_ext = df_ext[['SubNetwork',
    'MEID',
    'eNBId',
    'ExternalEUtranCellFDD',
    'antPort1',
    'cellLocalId',
    'cellType',
    'mcc',
    'tac',
    'userLabel',
    'earfcnDl',
    'mnc',
    'pci',
    'earfcnUl',
    'addiFreqBand',
    'bandWidthUl',
    'bandWidthDl',
    'freqBandInd'
    ]]

df_tmp = df_ext.head(10)
#df_nei_simp = df_relation_all[['MEID','CellId','eNBId','NCellId']]
#with pd.ExcelWriter('./结果输出/邻接关系_简.xlsx') as f:
#    df_nei_simp.to_excel(f,'邻区合并',index =False)

with open('./结果输出/外部邻区.csv', 'w',newline = '', encoding = 'utf-8') as f:
    df_ext.to_csv(f,index =False)

with open('./结果输出/邻接关系_合.csv', 'w', newline = '', encoding = 'utf-8') as f:
    df_rela.to_csv(f,index =False)


df_ext = pd.read_csv('./结果输出/外部邻区.csv')
df_rela = pd.concat([x for x in tqdm(read_csv_partly('./结果输出/邻接关系_合.csv'))],axis =0)
