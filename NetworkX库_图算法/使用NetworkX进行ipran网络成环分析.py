# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 23:22:37 2020

@author: Administrator
"""

import networkx as nx
import pandas as pd
import os
from copy import deepcopy

path = r'D:\_python小程序\通过ipran端口数据判断相邻节点'
like_file = 'ipran_link.xls'
equipment_file = 'ipran_equipment.xls'
bts_file = 'ipran_bts.xls'
os.chdir(path)

G = nx.Graph()

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

# 找出在环上并且带有支链和没带支链的节点
loop_without_chain = [x for x in G.nodes() if G.degree(x)<=2 and x in on_loop_list]
loop_with_chain = [x for x in G.nodes() if G.degree(x)>2 and x in  on_loop_list]


# 删除所有在环上且没带支链的节点
G.remove_nodes_from(loop_without_chain)

# 找出所有B设备对应的节点
df_b_device = df_link[['A端设备名称', 'A端设备id','A端设备类型']][df_link['A端设备类型'] =='B']
b_device_node = list(set(df_b_device['A端设备id']))

# 删除所有的B设备对应的节点
G.remove_nodes_from(b_device_node)

# 只选A设备，使用广度搜索算法 bfs，生成环带链的节点关联的数
loop_with_chain = [x for x in loop_with_chain if x not in b_device_node]
loop_with_chain_tree_dict = {}
# 要生成环带链节点的树，要把在环上的其他节点全部删除，只考虑自己和不成环的节点
for node in loop_with_chain:
    li_tmp = deepcopy(on_loop_list)
    G_tmp = G.copy()
    li_tmp.remove(node)
    G_tmp.remove_nodes_from(li_tmp)
    loop_with_chain_tree_dict[node] = list(nx.bfs_tree(G_tmp,node))

# 翻译环带链下挂A设备的名字
loop_with_chain_name_dict ={
    k:list(map(lambda x:reverse_equip_dict[x],v))
    for k,v in loop_with_chain_tree_dict.items()
}

# 计算每个环带链节点下挂的基站总数
loop_with_chain_bts_num_dict ={
    k:sum(list(map(lambda x:bts_num_dict.setdefault(x,0),v)))
    for k,v in loop_with_chain_name_dict.items()
}

# 挑选出下挂基站数量大于 8个的node，就是关键传输节点
core_node_dict = {
    k:v
    for k,v in loop_with_chain_bts_num_dict.items()
    if v>=7
}

# 翻译关键节点的名字
core_node_name_dict = {
    reverse_equip_dict[k]:v
    for k,v in core_node_dict.items()
}

# 将最终结果输出成表格
df_core_node = pd.DataFrame({
    'A设备名称':list(core_node_name_dict.keys()),
    'A设备id':list(core_node_dict.keys()),
    '下挂基站数量':list(core_node_name_dict.values())
})

df_core_node['本站基站数量'] = df_core_node['A设备名称'].map(bts_num_dict)
df_core_node['下挂A设备清单'] = df_core_node['A设备id'].map(loop_with_chain_name_dict)

with pd.ExcelWriter('关键传输节点_输出.xlsx') as f:
    df_core_node.to_excel(f, index =False)