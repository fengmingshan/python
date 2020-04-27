# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 15:33:05 2020

@author: Administrator
"""

# 添加邻接小区
add_ExternalCell_cmd = r'CREATE:MOC="ExternalEUtranCellFDD",\
MOI="SubNetwork=530306,MEID=730593,\
ENBFunctionFDD=730593,\
ExternalEUtranCellFDD=11",\
ATTRIBUTES="antPort1=1,\
cellLocalId=17,\
cellType=0,\
mcc=460,\
tac=0,\
userLabel=cell_name,\
voLTESwch=1,\
freqBandPriSwch=0,\
earfcnDl=879,\
plmnIdList=(OBJ)[{mcc=460,mnc=11}],\
mnc=11,\
pci=3,\
emtcSwch=0,\
earfcnUl=834,\
rsrpThrPrachInfoList=\"-118;-123;-127\",\
cellMbsfnAtt=0,\
massiveMIMOInd=0,\
addiFreqBand=\"0;0;0;0;0;0;0;0\",\
bandWidthUl=2,\
esCellNum=0,\
nbrEnDcAnchorInd=0,\
bandWidthDl=2,\
freqBandInd=5,\
eNBId=730593,\
ExternalEUtranCellFDD=11,\
freqBandPriInd=0",\
EXTENDS="";'

# 添加邻接关系
add_EUtranRelation_cmd = r'CREATE:MOC="EUtranRelation",\
MOI="SubNetwork=530306,\
MEID=730593,\
ENBFunctionFDD=730593,\
EUtranCellFDD=1,\
EUtranRelation=14",\
ATTRIBUTES="\
refExternalEUtranCellFDD=\"SubNetwork={subnet},MEID={meid},ConfigSet=0,ENBFunctionFDD={end2},ExternalEUtranCellFDD={extcell}\",\
coperType=0,\
isRemoveAllowed=1,\
switchonTimeWindow=1,\
isESCoveredBy=0,\
s1DataFwdFlag=0,\
isHOAllowed=1,\
coverESCell=0,\
EUtranRelation=14,\
userLabel=cell_name,\
overlapCoverage=50,\
shareCover=0,\
qofStCell=15,\
bigSRVHOIndUL=1,\
isAnrCreated=0,\
resPRBDown=50,\
isX2HOAllowed=1,\
resPRBUp=50,\
bigSRVHOIndDL=1,\
lbIntraMeasureOffset=-3,\
stateInd=2,\
cellIndivOffset=15,\
refExternalEUtranCellTDD=null,\
coperModSwch=0,\
supportMRO=1,\
hSpeedRailCellInd=0,\
noSupMobilitySwch=0,\
numRRCCntNumCov=100,\
isBasicCoverageCell=0",\
EXTENDS="";'

print(command2)