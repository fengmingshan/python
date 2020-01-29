import  pandas as pd
import  os

data_path = r'd:\_邻区自动规划' + '\\'
cell_info ='全网小区.csv'
neighbor_file = '邻区规划结果.xlsx'
eric_nieghbor = 'PARA_ERBS_371.csv'
zte_nieghbor = '中兴LTE全量邻区导出.xlsx'
whole_network ='全网工程参数(合).xlsx'
eric_info = '爱立信云南曲靖电信工参表20190428.xlsx'
zte_info = 'EUtranCellFDD.xlsx'

def calc_PCI_group(pci):
     if pci % 3 == 0:
          groupID = pci/3
     elif (pci-1) % 3 == 0:
          groupID = (pci-1)/3
     elif (pci-2) % 3 == 0:
          groupID = (pci-2)/3
     return groupID


def calc_PCI_SubCellId(pci):
     if pci % 3 == 0:
          SubCellId = 0
     elif (pci-1) % 3 == 0:
          SubCellId = 1
     elif (pci-2) % 3 == 0:
          SubCellId = 2
     return SubCellId


df_cell_info = pd.read_csv(data_path + cell_info,engine = 'python')
df_manufacturers = df_cell_info[['Cell_index','manufacturers']]
df_manufacturers = df_manufacturers.set_index('Cell_index')
dict_manufacturers = df_manufacturers.to_dict()['manufacturers']

df_eNodeB = df_cell_info[['Cell_index','name']]
df_eNodeB['eNodeB'] = df_eNodeB['name'].map(lambda x:x.split('_')[0])
df_eNodeB = df_eNodeB[['Cell_index','eNodeB']]
df_eNodeB = df_eNodeB.set_index('Cell_index')
dict_eNodeB = df_eNodeB.to_dict()['eNodeB']

df_neighbor = pd.read_excel(data_path + neighbor_file)
df_neighbor = df_neighbor[['Scell_name','Scell_index','Ncell_name','Ncell_index']]
df_neighbor['relations'] = df_neighbor['Scell_index'].map(str) + '_' +df_neighbor['Ncell_index'].map(str)

df_neighbor['源基站'] = df_neighbor['Scell_index'].map(dict_eNodeB)
df_neighbor['目标基站'] = df_neighbor['Ncell_index'].map(dict_eNodeB)
df_neighbor = df_neighbor[df_neighbor['源基站'] != df_neighbor['目标基站']]

df_neighbor['源小区厂家'] = df_neighbor['Scell_index'].map(dict_manufacturers)
df_neighbor['目标小区厂家'] = df_neighbor['Ncell_index'].map(dict_manufacturers)


# =============================================================================
# 检查爱立信的邻区
# =============================================================================
df_eric = pd.read_csv(data_path + eric_nieghbor,engine = 'python')
df_eric['Scell_index'] = df_eric['ENBCELL'].map(lambda x:x.split('_')[4] + x.split('_')[5])
df_eric['Ncell_index'] = df_eric['EUTRANCELLRELATIONID'].map(lambda x:x.split('-')[1] + x.split('-')[2])
df_eric['relations'] = df_eric['Scell_index'].map(str) + '_' + df_eric['Ncell_index'].map(str)
df_eric['neighbor_check'] = 'YES'
df_eric = df_eric[['relations','neighbor_check']]

df_eric_neighbor = df_neighbor[df_neighbor['源小区厂家'] == 'ERIC']

df_eric_check = pd.merge(df_eric_neighbor,df_eric, how ='left', on = 'relations')
df_eric_check = df_eric_check[df_eric_check['neighbor_check'].isnull()]

df_eric_add = pd.DataFrame(columns= ['Serving Site ID','Serving eNBId','Serving Cell Name',
                                     'Serving cellId','Serving PhysicalLayerCellIdGroup','Serving physicalLayerSubCellId',
                                     'S_FDD_TDD','Neighbor Site ID','Neighbor eNBId','Neighbor Cell Name',
                                     'DL EARFCN','UL EARFCN','Neighbor cellId','Neighbor PhysicalLayerCellIdGroup',
                                     'Neighbor physicalLayerSubCellId','plmnId','tac','Neighbor eNB IP',
                                     'E_FDD_TDD','Serving eNB IP'
                                     ])

df_eric_info = pd.read_excel(data_path + eric_info)
df_eric_info.set_index('Cell_index',inplace =True)

ServingeNode_dict = df_eric_info.to_dict()['eNBId']
ServingSiteID_dict = df_eric_info.to_dict()['SiteID']
ServingCellName_dict = df_eric_info.to_dict()['CellName']
ServingCellId_dict = df_eric_info.to_dict()['cellId']
ServingPCIGroup_dict = df_eric_info.to_dict()['physicalLayerCellIdGroup']
ServingPCISubCellId_dict = df_eric_info.to_dict()['physicalLayerSubCellId']
ServingeNBIP_dict = df_eric_info.to_dict()['eNb_IP']

df_eric_add['Serving eNBId'] = df_eric_check['Scell_index'].map(ServingeNode_dict)
df_eric_add['Serving Site ID'] = df_eric_check['Scell_index'].map(ServingSiteID_dict)
df_eric_add['Serving Cell Name'] = df_eric_check['Scell_index'].map(ServingCellName_dict)
df_eric_add['Serving cellId'] = df_eric_check['Scell_index'].map(ServingCellId_dict)
df_eric_add['Serving PhysicalLayerCellIdGroup'] = df_eric_check['Scell_index'].map(ServingPCIGroup_dict)
df_eric_add['Serving physicalLayerSubCellId'] = df_eric_check['Scell_index'].map(ServingPCISubCellId_dict)
df_eric_add['S_FDD_TDD'] = 'FDD'
df_eric_add['E_FDD_TDD'] = 'FDD'
df_eric_add['Serving eNB IP'] = df_eric_check['Scell_index'].map(ServingeNBIP_dict)


df_whole_network = pd.read_excel(data_path + whole_network,sheet_name = '邻区基础信息')
df_whole_network.set_index('CELLID',inplace =True)
df_whole_network['Neighbor PhysicalLayerCellIdGroup'] = df_whole_network['pci'].map(lambda x:calc_PCI_group(x))
df_whole_network['Neighbor physicalLayerSubCellId'] = df_whole_network['pci'].map(lambda x:calc_PCI_SubCellId(x))

NeighborSiteID_dict = df_whole_network.to_dict()['SiteID']
NeighboreNBId_dict = df_whole_network.to_dict()['eNodeB_ID']
NeighborCellName_dict = df_whole_network.to_dict()['CELLNAME']
DLEARFCN_dict = df_whole_network.to_dict()['DL_EARFCN']
ULEARFCN_dict = df_whole_network.to_dict()['UL_EARFCN']
NeighborCellId_dict = df_whole_network.to_dict()['CELL_id']
NeighborPCIGroup_dict = df_whole_network.to_dict()['Neighbor PhysicalLayerCellIdGroup']
NeighborPCISubCellId_dict = df_whole_network.to_dict()['Neighbor physicalLayerSubCellId']
tac_dict = df_whole_network.to_dict()['TAC']
NeighboreNBIP_dict = df_whole_network.to_dict()['SiteIP']

df_eric_add['Neighbor Site ID'] = df_eric_check['Ncell_index'].map(NeighborSiteID_dict)
df_eric_add['Neighbor eNBId'] = df_eric_check['Ncell_index'].map(NeighboreNBId_dict)
df_eric_add['Neighbor Cell Name'] = df_eric_check['Ncell_index'].map(NeighborCellName_dict)
df_eric_add['DL EARFCN'] = df_eric_check['Ncell_index'].map(DLEARFCN_dict)
df_eric_add['UL EARFCN'] = df_eric_check['Ncell_index'].map(ULEARFCN_dict)
df_eric_add['Neighbor cellId'] = df_eric_check['Ncell_index'].map(NeighborCellId_dict)
df_eric_add['Neighbor PhysicalLayerCellIdGroup'] = df_eric_check['Ncell_index'].map(NeighborPCIGroup_dict)
df_eric_add['Neighbor physicalLayerSubCellId'] = df_eric_check['Ncell_index'].map(NeighborPCISubCellId_dict)
df_eric_add['plmnId'] = 46011
df_eric_add['tac'] = df_eric_check['Ncell_index'].map(tac_dict)
df_eric_add['Neighbor eNB IP'] = df_eric_check['Ncell_index'].map(NeighboreNBIP_dict)

with pd.ExcelWriter(data_path + '爱立信邻区漏配检查结果.xlsx') as writer:
     df_eric_check.to_excel(writer,index =False)

with pd.ExcelWriter(data_path + '爱立信邻区添加.xlsx') as writer:
     df_eric_add.to_excel(writer,index =False)

# =============================================================================
# 检查中兴的邻区
# =============================================================================
df_zte = pd.read_excel(data_path + zte_nieghbor)
df_zte['relations'] = df_zte['Scell_index'].map(str) + '_' + df_zte['Ncell_index'].map(str)
df_zte['neighbor_check'] = 'YES'
df_zte = df_zte[['relations','neighbor_check']]

df_zte_neighbor = df_neighbor[df_neighbor['源小区厂家'] == 'ZTE']

df_zte_check = pd.merge(df_zte_neighbor,df_zte, how ='left', on = 'relations')
df_zte_check = df_zte_check[df_zte_check['neighbor_check'].isnull()]

df_zte_add = pd.DataFrame(columns= ['MODIND','SubNetwork','MEID','mcc','mnc',
                                     'eNBId','cellLocalId','plmnIdList',
                                     'userLabel','freqBandInd','earfcnUl','earfcnDl',
                                     'pci','tac','bandWidthDl','bandWidthUl','antPort1',
                                     'cellType','addiFreqBand'
                                     ])

df_zte_info = pd.read_excel(data_path + zte_info)
df_zte_info.set_index('CELLID',inplace =True)

SubNetwork_dict = df_zte_info.to_dict()['SubNetwork']
MEID_dict = df_zte_info.to_dict()['MEID']
CELLID_dict = df_zte_info.to_dict()['cellLocalId']


freqBandInd_dict = df_whole_network.to_dict()['频段指示']
earfcnUl_dict = df_whole_network.to_dict()['上行频点']
earfcnDl_dict = df_whole_network.to_dict()['下行频点']
pci_dict = df_whole_network.to_dict()['pci']
tac_dict = df_whole_network.to_dict()['TAC']
bandWidthDl_dict = df_whole_network.to_dict()['bandWidthDl']
bandWidthUl_dict = df_whole_network.to_dict()['bandWidthUl']

df_zte_add['SubNetwork'] = df_zte_check['Scell_index'].map(SubNetwork_dict)
df_zte_add['MEID'] = df_zte_check['Scell_index'].map(MEID_dict)
df_zte_add['mcc'] = 460
df_zte_add['mnc'] = 11

df_zte_add['eNBId'] = df_zte_check['Ncell_index'].map(NeighboreNBId_dict)
df_zte_add['cellLocalId'] = df_zte_check['Ncell_index'].map(NeighborCellId_dict)
df_zte_add['plmnIdList'] = '460,11'
df_zte_add['userLabel'] = df_zte_check['Ncell_index'].map(NeighborCellName_dict)
df_zte_add['freqBandInd'] = df_zte_check['Ncell_index'].map(freqBandInd_dict)
df_zte_add['earfcnUl'] = df_zte_check['Ncell_index'].map(earfcnUl_dict)
df_zte_add['earfcnDl'] = df_zte_check['Ncell_index'].map(earfcnDl_dict)
df_zte_add['pci'] = df_zte_check['Ncell_index'].map(pci_dict)
df_zte_add['tac'] = df_zte_check['Ncell_index'].map(tac_dict)
df_zte_add['bandWidthDl'] = df_zte_check['Ncell_index'].map(bandWidthDl_dict)
df_zte_add['bandWidthUl'] = df_zte_check['Ncell_index'].map(bandWidthUl_dict)
df_zte_add['antPort1'] = 1
df_zte_add['cellType'] = 0
df_zte_add['addiFreqBand'] = '0;0;0;0;0;0;0;0'
df_zte_add['MODIND'] = 'A'

df_zte_relation = pd.DataFrame(columns= ['MODIND','SubNetwork','MEID','CellId','srcENBId',
                                          'mcc','mnc','eNBId','NCellId','userLabel',
                                          'isRemoveAllowed','isX2HOAllowed','isHOAllowed','shareCover','qofStCell',
                                          'isAnrCreated','nCelPriority','s1DataFwdFlag','cellIndivOffset',
                                          'stateInd','coperType','radioMode','overlapCoverage'
                                          ])

df_zte_relation['SubNetwork'] = df_zte_check['Scell_index'].map(SubNetwork_dict)
df_zte_relation['MEID'] = df_zte_check['Scell_index'].map(MEID_dict)
df_zte_relation['CellId'] = df_zte_check['Scell_index'].map(CELLID_dict)
df_zte_relation['srcENBId'] = df_zte_check['Scell_index'].map(MEID_dict)
df_zte_relation['mcc'] = 460
df_zte_relation['mnc'] = 11

df_zte_relation['eNBId'] = df_zte_check['Ncell_index'].map(NeighboreNBId_dict)
df_zte_relation['NCellId'] = df_zte_check['Ncell_index'].map(NeighborCellId_dict)
df_zte_relation['userLabel'] = df_zte_check['Ncell_index'].map(NeighborCellName_dict)
df_zte_relation['isRemoveAllowed'] = 1
df_zte_relation['isX2HOAllowed'] = 1
df_zte_relation['isHOAllowed'] = 1
df_zte_relation['shareCover'] = 0
df_zte_relation['qofStCell'] = 15
df_zte_relation['isAnrCreated'] = 0
df_zte_relation['nCelPriority'] = 2
df_zte_relation['s1DataFwdFlag'] = 0
df_zte_relation['cellIndivOffset'] = 15
df_zte_relation['stateInd'] = 2
df_zte_relation['coperType'] = 0
df_zte_relation['radioMode'] = 'LTE FDD'
df_zte_relation['overlapCoverage'] = 50

with pd.ExcelWriter(data_path + '中兴邻区漏配检查结果.xlsx') as writer:
     df_zte_check.to_excel(writer,index =False)

with pd.ExcelWriter(data_path + '中兴邻区添加模板.xlsx') as writer:
     df_zte_add.to_excel(writer,'外部邻区',index =False)
     df_zte_relation.to_excel(writer,'邻接关系',index =False)


