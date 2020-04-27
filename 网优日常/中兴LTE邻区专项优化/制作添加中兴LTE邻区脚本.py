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


work_path = 'D:/2020年工作/2020年4月4G邻区专项优化/'
os.chdir(work_path)
if not os.path.exists('./结果输出'):
    os.mkdir('./结果输出')

df_ext = pd.read_csv('./结果输出/外部邻区.csv')
df_rela = pd.concat([x for x in tqdm(read_csv_partly('./结果输出/邻接关系_合.csv'))], axis=0)
df_rela['relation'] = df_rela['srcENBId'].map(
    str) + '_' + df_rela['CellId'].map(str) + '-' + df_rela['eNBId'].map(str) + '_' + df_rela['NCellId'].map(str)

add_ExternalCell_cmd = r'CREATE:MOC="ExternalEUtranCellFDD",\
MOI="SubNetwork={subnet},\
MEID={meid},\
ENBFunctionFDD={enb}",\
ATTRIBUTES="\
mcc=460,\
mnc=11,\
eNBId={enb2},\
cellLocalId={ncellid},\
plmnIdList=(OBJ)[{mcc=460,mnc=11}],\
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
    enb=enb,
    antport=antport,
    cell=cell,
    celltp=celltp,
    tac=tac,
    userlabel=userlabel,
    fcndl=fcndl,
    pci=pci,
    fcnul=fcnul,
    bandwidthul=bandwidthul,
    bandwidthdl=bandwidthdl,
    freqbandind=freqbandind,
    enb2 = enb2
)
    for subnet, meid, enb, antport, cell, celltp, tac, userlabel, fcndl,
        pci, fcnul, bandwidthul, bandwidthdl, freqbandind, enb2 in zip(
        df_ext['SubNetwork'],
        df_ext['MEID'],
        df_ext['eNBId'],
        df_ext['antPort1'],
        df_ext['cellLocalId'],
        df_ext['cellType'],
        df_ext['tac'],
        df_ext['userLabel'],
        df_ext['earfcnDl'],
        df_ext['pci'],
        df_ext['earfcnUl'],
        df_ext['bandWidthUl'],
        df_ext['bandWidthDl'],
        df_ext['freqBandInd'],
        df_ext['eNBId']
        )
]


add_Relation_cmd = r'CREATE:MOC="EUtranRelation",\
MOI="SubNetwork={subnet},\
MEID={meid},\
ENBFunctionFDD={srcenb},\
EUtranCellFDD={cell},\
ATTRIBUTES="\
refExternalEUtranCellFDD=\"SubNetwork={subnet},MEID={meid},ConfigSet=0,ENBFunctionFDD={end2},ExternalEUtranCellFDD={extcell}\",\
userLabel={userlabel},\
isRemoveAllowed=1,\
isX2HOAllowed=1,\
isHOAllowed=1,\
shareCover=0,\
qofStCell={qofstcell},\
isAnrCreated=0,\
s1DataFwdFlag=0,\
cellIndivOffset={cellindivoffset},\
stateInd=2,\
coperType=0,\
overlapCoverage=50,\
EXTENDS="";'


Relation_cmds = [add_Relation_cmd.format(
    subnet=subnet,
    meid=meid,
    enb=enb,
    cell=cell,
    isremove=isremove,
    ishoallow=ishoallow,
    userlabel=userlabel,
    sharecov=sharecov,
    qofstcell=qofstcell,
    isanrcre=isanrcre,
    isx2hoallow=isx2hoallow,
    cellindivoffset=cellindivoffset,
    ncellsubnet=ncellsubnet,
    ncellmeid=ncellmeid,
    ncellenb = ncellenb
)
    for subnet, meid, srcenb, cell, isremove, ishoallow, userlabel, sharecov, qofstcell,
        isanrcre, isx2hoallow, cellindivoffset, ncellsubnet, ncellmeid, ncellenb in zip(
        df_rela['SubNetwork'],
        df_rela['MEID'],
        df_rela['srcENBId'],
        df_rela['CellId'],
        df_rela['isRemoveAllowed'],
        df_rela['isHOAllowed'],
        df_rela['userLabel'],
        df_rela['shareCover'],
        df_rela['qofStCell'],
        df_rela['isAnrCreated'],
        df_rela['isX2HOAllowed'],
        df_rela['cellIndivOffset'],
        df_rela['SubNetwork'],
        df_rela['eNBId'],
        df_rela['eNBId']
        )
]
