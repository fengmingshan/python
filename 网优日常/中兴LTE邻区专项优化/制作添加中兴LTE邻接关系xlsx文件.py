# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 10:50:17 2020

@author: Administrator
"""

import pandas as pd
import os
from tqdm import tqdm

work_path = 'D:/2020年工作/2020年4月中兴LTE邻区专项优化/'
os.chdir(work_path)
if not os.path.exists('./结果输出'):
    os.mkdir('./结果输出')
if not os.path.exists('./脚本输出'):
    os.mkdir('./脚本输出')

def read_csv_partly(file):
    import pandas as pd
    file_data = pd.read_csv(file, engine='python', encoding='utf-8', chunksize=100000)
    for df_tmp in file_data:
        yield df_tmp

col = ['SubNetwork','MEID','ExternalEUtranCellFDD','srcENBId','mcc','mnc','eNBId','cellLocalId','plmnIdList','userLabel','freqBandInd','earfcnUl','earfcnDl','pci','tac','bandWidthDl','bandWidthUl','antPort1','cellType','addiFreqBand','emtcSwch']

df_cell_info = pd.read_csv('./结果输出/小区信息.csv',engine ='python')
SubNetwork_dict = df_cell_info[['SubNetwork','MEID']].set_index('MEID').to_dict()
df_cell_info['mcc'] = 460
df_cell_info['mnc'] = 11
df_cell_info['eNBId'] = df_cell_info['MEID']
df_cell_info['plmnIdList'] = '460,11'
df_cell_info['antPort1'] = 1
df_cell_info['cellType'] = 0
df_cell_info['cell_ind'] = df_cell_info['eNBId'].map(str) + '_' + df_cell_info['cellLocalId'].map(str)
df_cell_info = df_cell_info[['cell_ind','mcc','mnc','eNBId','cellLocalId','plmnIdList','userLabel','freqBandInd','earfcnUl','earfcnDl','pci','tac','bandWidthDl','bandWidthUl','antPort1','cellType','addiFreqBand','emtcSwch']]

df_ext_info = pd.read_csv('./结果输出/外部邻区_info.csv')
df_ext_info['Ncell'] = df_ext_info['eNBId'].map(str) + '_' +df_ext_info['cellLocalId'].map(str)
df_ext = pd.concat([x for x in tqdm(read_csv_partly('./结果输出/外部邻区.csv'))],axis =0)

df_rela = pd.concat([x for x in tqdm(read_csv_partly('./结果输出/邻接关系.csv'))],axis =0)

df_add = pd.read_csv('./结果输出/添加邻区.csv',engine = 'python')
df_add['ext_ind'] = df_add['Scell'].map(lambda x:x.split('_')[0]) + '-'+df_add['Ncell']

df_add_extcell = df_add[~df_add['ext_ind'].isin(df_ext['ext_ind'])]
df_add_extcell = df_add_extcell[['Scell','Ncell']]
df_add_extcell['cell_ind'] = df_add_extcell['Ncell']
df_add_extcell = pd.merge(df_add_extcell,df_cell_info,how ='left', on = 'cell_ind')


#with pd.ExcelWriter('./脚本输出/添加邻接关系.xlsx') as f:
#    df_add_excel.to_exce(f,'ExternalEUtranCellFDD',index=False)
#    df_add_relation.to_excel(f,'EUtranRelation',index=False)
