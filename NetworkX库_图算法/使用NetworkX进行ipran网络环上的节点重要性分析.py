# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 23:22:37 2020

@author: Administrator
"""

import networkx as nx
import pandas as pd
import os
from copy import deepcopy
import difflib

path = r'D:\_python小程序\通过ipran端口数据判断相邻节点'
like_file = 'ipran_link.xls'
equipment_file = 'ipran_equipment.xls'
bts_file = 'ipran_bts.xls'
ipran_base_station = 'ipran_base_station.xlsx'

os.chdir(path)

G = nx.Graph()

# 处理IPRAN 基站业务数据制作每个A设备下挂基站的表格

df_ipran_base_station = pd.read_excel(ipran_base_station)
df_ipran_base_station = df_ipran_base_station[['区县', '归属A名称', '现网基站名称', 'enb', '铁塔站址编码']]

#处理全网基站业务数据，统计全网A设备下挂基站数量
df_bts = pd.read_excel(bts_file)
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

# 制作通过A设备查BB对的字典
df_a2b = df_equipment[['设备名称', 'B1设备名称', 'B2设备名称']]
df_a2b = df_a2b[~(df_a2b['B1设备名称'].isnull())&~(df_a2b['B1设备名称'].isnull())]
df_a2b['key'] = df_a2b['B1设备名称'] + '#' + df_a2b['B2设备名称']
df_a2b['key'] = df_a2b['key'].map(lambda x:sorted(x.split('#'))[0] + '#' + sorted(x.split('#'))[1])

a2b_dict = df_a2b.set_index('设备名称')['key'].to_dict()

# 制作通过B设备查BB对的字典
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
G.add_edges_from(zip(df_link['A端设备id'].map(int), df_link['B端设备id'].map(int)))

def find_loop(G):
    degree_one = [x for x in G.nodes() if G.degree(x) ==1]
    G.remove_nodes_from(degree_one)
    return G

on_loop_list = []
for BB in df_link['BB对'].unique():
    df_tmp = df_link[df_link['BB对']== BB]
    # 创建图
    G_tmp = nx.Graph()
    G_tmp.add_nodes_from(df_tmp['A端设备id'])
    G_tmp.add_edges_from(zip(df_tmp['A端设备id'].map(int), df_tmp['B端设备id'].map(int)))
    # 通过循环剪枝，剪去末梢node，直到图中剩余的node都在环上
    while 1 in [G_tmp.degree(x) for x in G_tmp.nodes()]:
        G_tmp = find_loop(G_tmp)
    on_loop_list = on_loop_list + list(G_tmp.nodes())
on_loop_list = list(set(on_loop_list))

#with pd.ExcelWriter('成环节点.xlsx') as f:
#    df_on_loop.to_excel(f, index =False)

# 找出所有B设备对应的节点
df_b_device = df_link[['A端设备名称', 'A端设备id','A端设备类型']][df_link['A端设备类型'] =='B']
b_device_node = list(set(df_b_device['A端设备id']))

# 删除所有的B设备对应的节点
G.remove_nodes_from(b_device_node)
on_loop_list = list(set(on_loop_list) - set(b_device_node))
# 只选A设备，使用广度搜索算法 bfs，生成环上的节点关联的A设备tree。
on_loop_node_tree_dict = {}
# 要生成环带链节点的树，要把在环上的其他节点全部删除，只考虑自己和不成环的节点
for node in on_loop_list:
    on_loop_node_tree_dict[node] = list(nx.bfs_tree(G,node))

key_node_dict = {k:v for k,v in on_loop_node_tree_dict.items() if len(v)>=5}

# 翻译关键节点的名字
key_node_name_dict = {
    reverse_equip_dict[k]:v
    for k,v in key_node_dict.items()
}

# 将最终结果输出成表格
df_key_node = pd.DataFrame({
    'A设备名称':list(key_node_name_dict.keys()),
    '关联A设备数量':[len(v) for v in key_node_name_dict.values()]
})
A_nums_dict = df_key_node.set_index('A设备名称')['关联A设备数量'].to_dict()

df_key_equipment = df_equipment[df_equipment['设备名称'].isin(df_key_node['A设备名称'])]
df_key_equipment['关联A设备数量'] = df_key_equipment['设备名称'].map(A_nums_dict)
df_key_equipment = df_key_equipment[['设备名称', '区县', '关联A设备数量']]
区县字典 = df_key_equipment[['设备名称', '区县']].set_index('设备名称')['区县'].to_dict()
网元数量字典 = df_key_equipment[['设备名称', '关联A设备数量']].set_index('设备名称')['关联A设备数量'].to_dict()

df_result = df_ipran_base_station[df_ipran_base_station['归属A名称'].isin(df_key_equipment['设备名称'])]
df_result['关联A设备数量'] = df_result['归属A名称'].map(网元数量字典)
df_result.columns

df_result = df_result[['区县', '归属A名称','关联A设备数量', '现网基站名称', 'enb','铁塔站址编码']]
df_result.sort_values(by = ['区县', '归属A名称'],inplace =True)

# 通过difflib库找出与A设备名称最接近的基站名，也就是A设备本站的站名
#for name in df_result['归属A名称'].unique():
#    df_tmp = df_result[df_result['归属A名称'] == name]
#    df_tmp['本站基站名称'] = df_tmp['归属A名称'].map(
#            lambda x:difflib.get_close_matches(x,list(df_tmp['基站名称']), n=1)[0])
#difflib.get_close_matches('七里牌村-A-1',['BS8700_QJ会泽迤车七里牌村山上_WDTD_ZFT_M'])

with pd.ExcelWriter('在环上的关键传输节点_输出.xlsx') as f:
    df_result.to_excel(f, index =False)


