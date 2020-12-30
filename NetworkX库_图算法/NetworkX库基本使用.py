# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 23:22:37 2020

@author: Administrator
"""

import networkx as nx
import pandas as pd
import os


path = r'D:\_python小程序\通过ipran端口数据判断相邻节点'
like_file = 'ipran_link.xls'
equipment_file = 'ipran_equipment.xls'
bts_file = 'ipran_bts.xls'
on_loop_file = '成环的设备.xlsx'
not_on_loop_file = '未成环的设备.xlsx'

G = nx.Graph()

df_on_loop = pd.read_excel(on_loop_file)
df_not_on_loop = pd.read_excel(not_on_loop_file)

#处理全网基站业务数据，统计全网A设备下挂基站数量
df_bts = pd.read_excel(bts_file)
df_bts.columns
df_bts = df_bts.groupby(by = '归属A名称',as_index=False)['基站类型'].count()
bts_num_dict = df_bts.set_index('归属A名称')['基站类型'].to_dict()

# 处理设备清单数据，将A设备进行编码：
df_equipment = pd.read_excel(equipment_file)

df_host2equip = df_equipment[['主机名','设备名称','设备类型']]
df_host2equip['设备名称'][df_host2equip['设备类型'] =='B'] = 'B设备'
host2equip_dict = df_host2equip[['主机名','设备名称']].set_index('主机名')['设备名称'].to_dict()

df_equip_name = df_equipment[['设备名称','设备类型']]
df_equip_name = df_equip_name['设备名称']
equip_list = list(df_equipment['设备名称'].unique())
equip_dict = {v:k for k,v in enumerate(equip_list)}
reverse_equip_dict = {k:v for k,v in enumerate(equip_list)}

df_a2b = df_equipment[['设备名称', 'B1设备名称', 'B2设备名称']]
df_a2b = df_a2b[~(df_a2b['B1设备名称'].isnull())&~(df_a2b['B1设备名称'].isnull())]
df_a2b['key'] = df_a2b['B1设备名称'] + '#' + df_a2b['B2设备名称']
df_a2b['key'] = df_a2b['key'].map(lambda x:sorted(x.split('#'))[0] + '#' + sorted(x.split('#'))[1])

a2b_dict = df_a2b.set_index('设备名称')['key'].to_dict()


df_link = pd.read_excel(like_file)
df_link.columns
df_link = df_link[(df_link['A端设备类型'].isin(['A','B']))&(df_link['B端设备类型'].isin(['A','B']))]
df_link = df_link[~df_link['A端端口'].isnull()]

# 对链路进行去重
df_link['key'] = df_link['A端设备名称'] + '#' +\
    df_link['A端端口'] + '#' +\
    df_link['B端设备名称'] + '#' +\
    df_link['B端端口']
df_link = df_link.drop_duplicates('key')

#df_link['key'] = df_link['key'].map(lambda x:sorted(x.split('#'))[0] + '#' +
#    sorted(x.split('#'))[1] + '#' +
#    sorted(x.split('#'))[2] + '#' +
#    sorted(x.split('#'))[3]
#)

#df_link['数量'] = df_link['key'].map(lambda x:list(df_link['key']).count(x))
#with pd.ExcelWriter('总表.xlsx') as f:
#    df_link.to_excel(f, index =False)

df_link = df_link[['A端设备名称', 'A端设备类型', 'B端设备名称', 'B端设备类型']]
df_link['A端设备id'] = df_link['A端设备名称'].map(equip_dict)
df_link['B端设备id'] = df_link['B端设备名称'].map(equip_dict)
df_link['A端下挂基站数'] = df_link['A端设备名称'].map(bts_num_dict)
df_link['A端下挂基站数'] = df_link['A端下挂基站数'].fillna(0)
df_link['B端下挂基站数'] = df_link['B端设备名称'].map(bts_num_dict)
df_link['B端下挂基站数'] = df_link['B端下挂基站数'].fillna(0)

df_b2b = df_link[(df_link['A端设备类型']== 'B')&(df_link['B端设备类型'] == 'B')]
df_b2b['key'] = df_b2b['A端设备名称'] + '#' + df_b2b['B端设备名称']
df_b2b['key'] = df_b2b['key'].map(lambda x:sorted(x.split('#'))[0] + '#' + sorted(x.split('#'))[1])

b2b_dict = df_b2b.set_index('A端设备名称')['key'].to_dict()

df_link['BB对'] = df_link['A端设备名称'].map(a2b_dict)
df_link['BB对'][df_link['BB对'].isnull()] = df_link['A端设备名称'][df_link['BB对'].isnull()].map(b2b_dict)
df_link = df_link[~df_link['A端设备id'].isnull()]
df_link = df_link[~df_link['B端设备id'].isnull()]

df_link = df_link[['A端设备名称',
                   'A端设备类型',
                   'A端设备id',
                   'A端下挂基站数',
                   'B端设备名称',
                   'B端设备类型',
                   'B端设备id',
                   'B端下挂基站数',
                   'BB对'
]]

G.add_nodes_from(df_link['A端设备id'])
G.add_edges_from(zip(df_link['A端设备id'], df_link['B端设备id']))

