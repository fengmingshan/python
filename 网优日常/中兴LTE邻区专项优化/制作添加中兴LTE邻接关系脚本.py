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
df_ext['ExternalEUtranCellFDD'] = df_ext['ExternalEUtranCellFDD'].map(int)

df_rela = pd.concat([x for x in tqdm(read_csv_partly('./结果输出/邻接关系_合.csv'))],axis =0)
df_rela = pd.concat([x for x in tqdm(read_csv_partly('./结果输出/邻接关系_合.csv'))],axis =0)

df_add = pd.read_csv('./结果输出/添加邻区.csv',engine = 'python')
df_add['ext_ind'] = df_add['Scell'].map(lambda x:x.split('_')[0]) + '-'+df_add['Ncell']

df_add_extcell = df_add[~df_add['ext_ind'].isin(df_ext['ext_ind'])]
df_add_extcell = pd.merge(df_add_extcell[['Scell','Ncell']],df_ext_info,how ='left', on = 'Ncell')

with open('添加外部邻区.csv','w',newline = '') as f:
    df_add_extcell.to_csv(f,index=False)

add_ExternalCell_cmd = r'CREATE:MOC="ExternalEUtranCellFDD",\
MOI="SubNetwork={subnet},\
MEID={meid},\
ATTRIBUTES="\
mcc=460,\
mnc=11,\
eNBId={enb2},\
cellLocalId={celllocalid},\
plmnIdList=(OBJ)[{{mcc=460,mnc=11}}],\
userLabel={userlabel},\
freqBandInd={freqbandind},\
earfcnUl={fcnul},\
earfcnDl={fcndl},\
pci={pci},\
tac={tac},\
bandWidthDl={bandwidthdl},\
bandWidthUl={bandwidthul},\
antPort1={antport},\
cellType=0,\
addiFreqBand=\"0;0;0;0;0;0;0;0\",\
emtcSwch=0,\
EXTENDS="";'

ExternalCell_cmds = [add_ExternalCell_cmd.format(
    subnet=subnet,
    meid=meid,
    enb2 = enb2,
    celllocalid=celllocalid,
    userlabel=userlabel,
    freqbandind=freqbandind,
    fcnul=fcnul,
    fcndl=fcndl,
    pci=pci,
    tac=tac,
    bandwidthul=bandwidthul,
    bandwidthdl=bandwidthdl,
    antport= antport
)
    for subnet, meid, enb2, celllocalid, userlabel, freqbandind, fcnul, fcndl,
        pci, tac, bandwidthul, bandwidthdl, antport in zip(
        df_add_extcell['SubNetwork'],
        df_add_extcell['MEID'],
        df_add_extcell['eNBId'],
        df_add_extcell['cellLocalId'],
        df_add_extcell['userLabel'],
        df_add_extcell['freqBandInd'],
        df_add_extcell['earfcnUl'],
        df_add_extcell['earfcnDl'],
        df_add_extcell['pci'],
        df_add_extcell['tac'],
        df_add_extcell['bandWidthUl'],
        df_add_extcell['bandWidthDl'],
        df_add_extcell['antPort1']
        )
]


Relation_cmd = r'CREATE:MOC="EUtranRelation",\
MOI="SubNetwork={subnet1},\
MEID={meid},\
ENBFunctionFDD={srcenb},\
EUtranCellFDD={srccell},\
ATTRIBUTES="\
refExternalEUtranCellFDD=\
"SubNetwork={subnet},\
MEID={meid},\
ConfigSet=0,\
ENBFunctionFDD={nenb},\
ExternalEUtranCellFDD={extcell}\",\
userLabel={userlabel},\
isRemoveAllowed=1,\
isX2HOAllowed=1,\
isHOAllowed=1,\
shareCover=0,\
qofStCell=15,\
isAnrCreated=0,\
s1DataFwdFlag=0,\
cellIndivOffset=15,\
stateInd=2,\
coperType=0,\
overlapCoverage=50,\
EXTENDS="";'


Relation_cmds = [add_Relation_cmd.format(
    subnet=subnet,
    meid=meid,
    srcenb=srcenb,
    srccell=srccell,
    subnet1=subnet1,
    meid1 = meid1,
    nenb=nenb,
    extcell=extcell
)
    for subnet, meid, srcenb, srccell, subnet1, meid1, nenb, extcell in zip(
        df_rela['SubNetwork'],
        df_rela['MEID'],
        df_rela['srcENBId'],
        df_rela['CellId'],
        df_rela['SubNetwork'],
        df_rela['MEID'],
        df_rela['eNBId'],
        df_rela['eNBId']
        )
]
