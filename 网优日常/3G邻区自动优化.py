# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 14:54:34 2019

@author: Administrator
"""

import pandas as pd 
import numpy as np
import os
import xlwt
import shutil
# =============================================================================
# 设置环境变量
# =============================================================================
data_path = r'd:\3G邻区自动优化\BSC1原始数据' + '\\'
out_path = r'd:\3G邻区自动优化' + '\\'

# 定义一个文本转xls的函数，因为切换次数的xls文件格式有问题
def txt2xls(filename,xlsname):
    """
    :文本转换成xls的函数
    :param filename txt文本文件名称、
    :param xlsname 表示转换后的excel文件名
    """
    try:
        f = open(filename) 
        xls=xlwt.Workbook()
        #生成excel的方法，声明excel
        sheet = xls.add_sheet('sheet1',cell_overwrite_ok=True) 
        x = 0 
        while True:
            #按行循环，读取文本文件
            line = f.readline() 
            if not line: 
                break  #如果没有内容，则退出循环
            for i in range(len(line.split('\t'))):
                item=line.split('\t')[i]
                sheet.write(x,i,item) #x单元格经度，i 单元格纬度
            x += 1 #excel另起一行
        f.close()
        xls.save(xlsname) #保存xls文件
    except:
        raise

cell_config_files = [x for x in os.listdir(data_path) if '小区实体参数表' in x ]
handover_files = [x for x in os.listdir(data_path) if '小区切换邻区对象' in x ]
cell_neighbor_files = [x for x in os.listdir(data_path) if '邻接小区参数表' in x ]
carrie_neighborr_files = [x for x in os.listdir(data_path) if '载频邻区参数表' in x ]

## 转换xls文件格式为txt格式
#for file in handover_files:
#    os.rename(data_path + file,data_path + file.replace('.xls','.txt'))
#handover_files = [x for x in os.listdir(data_path) if '小区切换邻区对象' in x ]
# 
## 将TXT格式的文件转换成xls格式，并删除旧的txt文件  
#for file in handover_files:
#    txt2xls(data_path + file,data_path + file.replace('.txt','.xls'))
#    os.remove(data_path + file)

# 合并处理小区实体参数文件           
df_cell_config = pd.DataFrame()
for file in cell_config_files:
    df_tmp = pd.read_excel(data_path + file,skiprows = 1,dtype = str ,encoding='utf-8') 
    df_cell_config = df_cell_config.append(df_tmp)
df_cell_config = df_cell_config[['system','cellid','pilot_pn','alias_b']]
df_cell_config = df_cell_config.rename(columns = {'pilot_pn':'Scell_pn','alias_b':'Scell_name'})
df_cell_config['Scell_index'] =  df_cell_config['system'] + '_' + df_cell_config['cellid']
df_cell_config = df_cell_config[['Scell_index','Scell_name','Scell_pn']]

# 重新获取格式转换后的文件名
handover_files = [x for x in os.listdir(data_path) if '小区切换邻区对象' in x and '.txt' not in x ] 
# 合并处理切换次数文件    
df_handover = pd.DataFrame()
for file in handover_files:
    df_tmp = pd.read_excel(data_path + file,skiprows = 3,encoding='utf-8') 
    df_handover = df_handover.append(df_tmp)

df_handover.columns = df_handover.columns.map(lambda x:x.replace('\n',''))
df_handover['源BTS标识'] = df_handover['源BTS标识'].astype(str)
df_handover['源小区号'] = df_handover['源小区号'].astype(str) 
df_handover['目标BTS标识'] = df_handover['目标BTS标识'].astype(str) 
df_handover['目标小区号'] = df_handover['目标小区号'].astype(str)  
df_handover['Scell_index'] = df_handover['源BTS标识'] + '_' + df_handover['源小区号']
df_handover['neighbor_index'] = df_handover['源BTS标识'] + '_' + df_handover['源小区号'] + \
                                '-' + df_handover['目标BTS标识'] + '_' + df_handover['目标小区号']
df_handover['切换总次数'] = df_handover['切换成功次数'] + df_handover['无效导频失败次数'] + df_handover['拥塞失败次数'] + df_handover['其他失败次数']                              
df_handover = df_handover[['neighbor_index','Scell_index','切换总次数','切换成功次数']]
df_handover = pd.pivot_table(df_handover, index=['neighbor_index','Scell_index'], 
                              values =['切换总次数' ,'切换成功次数'], 
                              aggfunc = {'切换总次数':np.sum,'切换成功次数':np.sum}) 
df_handover = df_handover.reset_index() 
df_handover = pd.merge(df_handover,df_cell_config,how = 'left', on = 'Scell_index')
df_handover = df_handover[['neighbor_index','Scell_index','Scell_name','Scell_pn','切换总次数','切换成功次数']]
df_handover['切换成功率(%)'] =  df_handover['切换成功次数']/df_handover['切换总次数']

 
# 合并处理小区邻区文件            
df_cell_neighbor = pd.DataFrame()
for file in cell_neighbor_files:
    df_tmp = pd.read_excel(data_path + file,skiprows = 1,dtype = str ,encoding='utf-8') 
    df_cell_neighbor = df_cell_neighbor.append(df_tmp)
    
df_cell_neighbor['neighbor_index'] = df_cell_neighbor['system'] + '_' + df_cell_neighbor['cellid'] + \
                                    '-' + df_cell_neighbor['ncellsystemid'] + '_' + df_cell_neighbor['ncellid']
df_cell_neighbor['Scell_index'] =  df_cell_neighbor['system'] + '_' + df_cell_neighbor['cellid']
df_cell_neighbor = df_cell_neighbor[['system','cellid','Scell_index','alias_b','pilot_pn','ncellsystemid','ncellid','neighbor_index']]
df_cell_neighbor = df_cell_neighbor.rename(columns ={'pilot_pn':'neighbor_pn','alias_b':'neighbor_name'})
df_cell_neighbor = pd.merge(df_cell_neighbor,df_cell_config,how = 'left', on = 'Scell_index')
df_cell_neighbor = pd.merge(df_cell_neighbor,df_handover,how = 'left', on = 'neighbor_index')

# 合并处理载频邻区文件            
df_carrier_neighbor = pd.DataFrame()
for file in carrie_neighborr_files:
    df_tmp = pd.read_excel(data_path + file,skiprows = 1,dtype = str,encoding='utf-8') 
    df_carrier_neighbor = df_carrier_neighbor.append(df_tmp)

df_carrier_neighbor['neighbor_index'] = df_carrier_neighbor['system'] + '_' + df_carrier_neighbor['cellid'] + \
                                        '-' + df_carrier_neighbor['ncellsystemid'] + '_' + df_carrier_neighbor['ncellid']
df_carrier_neighbor['Scell_index'] =  df_carrier_neighbor['system'] + '_' + df_carrier_neighbor['cellid']
df_carrier_neighbor = df_carrier_neighbor[['system','cellid','Scell_index','carrierid','alias_b','pilot_pn','ncellsystemid','ncellid','neighbor_index']]
df_carrier_neighbor = df_carrier_neighbor.rename(columns ={'pilot_pn':'neighbor_pn','alias_b':'neighbor_name'})
df_carrier_neighbor = pd.merge(df_carrier_neighbor,df_cell_config,how = 'left', on = 'Scell_index')
df_carrier_neighbor = pd.merge(df_carrier_neighbor,df_handover,how ='left', on = 'neighbor_index')

# =============================================================================
# 检查小区邻区
# =============================================================================
df_cell = df_cell_neighbor[['system','cellid','ncellsystemid','ncellid','neighbor_pn','neighbor_name','neighbor_index']]
df_cell_check = pd.merge(df_handover,df_cell,how = 'left',on = 'neighbor_index')
df_cell_check = df_cell_check[['system','cellid','Scell_index','Scell_name','Scell_pn','ncellsystemid',\
                               'ncellid','neighbor_name','neighbor_pn','切换总次数',\
                               '切换成功次数','切换成功率(%)','neighbor_index']]

df_cell_check = df_cell_check.sort_values(by='切换总次数',ascending = False) 
#with pd.ExcelWriter(out_path + 'cell_check.xlsx') as writer: #不用保存和退出，系统自动会完成
#    df_cell_check.to_excel(writer,'cell_check',index = False) 
