import  pandas as pd
import  os

data_path = r'd:\_邻区自动规划' + '\\'
cell_info ='全网小区.csv'
neighbor_file = '邻区规划结果(合并).xlsx'
eric_nieghbor = 'PARA_ERBS_371.csv'
zte_nieghbor = '中兴LTE全量邻区导出.xlsx'
whole_network ='全网工程参数_含贵州(合).xlsx'

df_whole_network = pd.read_excel(data_path + whole_network)

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


df_eric = pd.read_csv(data_path + eric_nieghbor,engine = 'python')
df_eric['Scell_index'] = df_eric['ENBCELL'].map(lambda x:x.split('_')[4] + x.split('_')[5])
df_eric['Ncell_index'] = df_eric['EUTRANCELLRELATIONID'].map(lambda x:x.split('-')[1] + x.split('-')[2])
df_eric['relations'] = df_eric['Scell_index'].map(str) + '_' + df_eric['Ncell_index'].map(str)
df_eric['neighbor_check'] = 'YES'
df_eric = df_eric[['relations','neighbor_check']]

df_eric_neighbor = df_neighbor[df_neighbor['源小区厂家'] == 'ERIC']

df_eirc_check = pd.merge(df_eric_neighbor,df_eric, how ='left', on = 'relations')
df_eirc_check = df_eirc_check[df_eirc_check['neighbor_check'].isnull()]

df_eirc_add =
with open(data_path + '爱立信邻区漏配检查结果.csv','w') as writer:
     df_eirc_check.to_csv(writer,index =False)

df_zte = pd.read_excel(data_path + zte_nieghbor)
df_zte['relations'] = df_zte['Scell_index'].map(str) + '_' + df_zte['Ncell_index'].map(str)
df_zte['neighbor_check'] = 'YES'
df_zte = df_zte[['relations','neighbor_check']]

df_zte_neighbor = df_neighbor[df_neighbor['源小区厂家'] == 'ZTE']

df_zte_check = pd.merge(df_zte_neighbor,df_zte, how ='left', on = 'relations')
df_zte_check = df_zte_check[df_zte_check['neighbor_check'].isnull()]

with open(data_path + '中兴邻区漏配检查结果.csv','w') as writer:
     df_zte_check.to_csv(writer,index =False)


