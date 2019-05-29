# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 17:51:09 2019

@author: Administrator
"""

import pandas as pd
import numpy as np
import os
import xlwt
# =============================================================================
# 设置环境变量
# =============================================================================
data_path = r'd:\3G邻区自动优化\BSC2原始数据' + '\\'
out_path = r'd:\3G邻区自动优化' + '\\'
cmd_path = r'd:\3G邻区自动优化\邻区修改脚本输出' + '\\'

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

print('**********汇总原始数据!**********')

cell_config_files = [x for x in os.listdir(data_path) if '小区实体参数表' in x ]
handover_files = [x for x in os.listdir(data_path) if '小区切换邻区对象' in x ]
cell_neighbor_files = [x for x in os.listdir(data_path) if '邻接小区参数表' in x ]
carrie_neighborr_files = [x for x in os.listdir(data_path) if '载频邻区参数表' in x ]

if handover_files[0].split('.')[1] == 'xls' and handover_files[len(handover_files)-1].split('.')[1] == 'xls' :
    # 转换xls文件格式为txt格式
    for file in handover_files:
        os.rename(data_path + file,data_path + file.replace('.xls','.txt'))
    handover_files = [x for x in os.listdir(data_path) if '小区切换邻区对象' in x ]

    # 将TXT格式的文件转换成xls格式，并删除旧的txt文件
    for file in handover_files:
        txt2xls(data_path + file,data_path + file.replace('.txt','.xls'))
        os.remove(data_path + file)
    handover_files = [x for x in os.listdir(data_path) if '小区切换邻区对象' in x ]
    for file in handover_files:
        df_tmp = pd.read_excel(data_path + file,encoding='utf-8')
        with pd.ExcelWriter(data_path + file.replace('xls','xlsx')) as writer: #不用保存和退出，系统自动会完成
            df_tmp.to_excel(writer,'sheet1',index = False)
        os.remove(data_path + file)


# 合并处理小区实体参数文件
df_cell_config = pd.DataFrame()
for file in cell_config_files:
    df_tmp = pd.read_excel(data_path + file,skiprows = 1,dtype = str ,encoding='utf-8')
    df_cell_config = df_cell_config.append(df_tmp)
df_cell_config = df_cell_config[['system','cellid','pilot_pn','alias_b']]
df_cell_config = df_cell_config.rename(columns = {'pilot_pn':'Scell_pn','alias_b':'Scell_name'})
df_cell_config['Scell_index'] =  df_cell_config['system'] + '_' + df_cell_config['cellid']
df_cell_config = df_cell_config[['Scell_index','Scell_name','Scell_pn']]

df_neighbor_config = df_cell_config.rename(columns={'Scell_index': 'Ncell_index',
                                                    'Scell_name': 'Ncell_name',
                                                    'Scell_pn': 'Ncell_pn'})

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
df_handover['切换总次数'] = df_handover['切换成功次数'] + df_handover['无效导频失败次数'] + \
                            df_handover['拥塞失败次数'] + df_handover['其他失败次数']

df_handover = df_handover.rename(columns = {'源BTS标识':'system',
                                            '源小区号':'cellid',
                                            '目标BTS标识':'ncellsystemid',
                                            '目标小区号':'ncellid'})

df_handover['Ncell_index'] = df_handover['ncellsystemid'] + '_'  + df_handover['ncellid']

df_handover = pd.pivot_table(df_handover, index=['system','cellid','Scell_index','ncellsystemid','Ncell_index','ncellid','neighbor_index'],
                             values =['切换总次数' ,'切换成功次数'],
                             aggfunc = {'切换总次数':np.sum,'切换成功次数':np.sum})

df_handover = df_handover.reset_index()
df_handover = pd.merge(df_handover,df_cell_config,how = 'left', on = 'Scell_index')
df_handover = df_handover[['system','cellid','Scell_index','Scell_name','Scell_pn','ncellsystemid','ncellid','Ncell_index','neighbor_index','切换总次数','切换成功次数']]
df_handover['切换成功率(%)'] =  df_handover['切换成功次数']/df_handover['切换总次数']


# 合并处理小区邻区文件
df_cell_neighbor = pd.DataFrame()
for file in cell_neighbor_files:
    df_tmp = pd.read_excel(data_path + file,skiprows = 1,dtype = str ,encoding='utf-8')
    df_cell_neighbor = df_cell_neighbor.append(df_tmp)

df_cell_neighbor['neighbor_index'] = df_cell_neighbor['system'] + '_' + df_cell_neighbor['cellid'] + \
                                    '-' + df_cell_neighbor['ncellsystemid'] + '_' + df_cell_neighbor['ncellid']
df_cell_neighbor['Scell_index'] =  df_cell_neighbor['system'] + '_' + df_cell_neighbor['cellid']
df_cell_neighbor['Ncell_index'] = df_cell_neighbor['ncellsystemid'] + '_'  + df_cell_neighbor['ncellid']
df_cell_neighbor['操作类型'] = '正常'
df_cell_neighbor = df_cell_neighbor.rename(columns ={'pilot_pn':'Ncell_pn','alias_b':'Ncell_name'})
df_cell_neighbor = pd.merge(df_cell_neighbor,df_cell_config,how = 'left', on = 'Scell_index')
df_切换次数 =  df_handover[['neighbor_index','切换总次数','切换成功次数','切换成功率(%)']]
df_cell_neighbor = pd.merge(df_cell_neighbor,df_切换次数,how = 'left', on = 'neighbor_index')
df_cell_neighbor.fillna(0,inplace = True)
df_cell_neighbor = df_cell_neighbor.reset_index()
df_cell_neighbor.drop('index',axis = 1 , inplace = True)
df_cell_neighbor = df_cell_neighbor[['system','cellid','Scell_index','Scell_name','Scell_pn',
                                     'ncellsystemid','ncellid','Ncell_index','Ncell_name','Ncell_pn',
                                     '切换总次数','切换成功次数','切换成功率(%)','neighbor_index','操作类型']]
df_小区邻区瘦身 = df_cell_neighbor[(df_cell_neighbor['切换总次数'] != 0)
                                    & (df_cell_neighbor['切换成功次数'] != 0)
                                    &(df_cell_neighbor['切换总次数'] < 4 )]
df_小区邻区瘦身['切换总次数'] = df_小区邻区瘦身['切换总次数'].astype(int)
df_小区邻区瘦身 = df_小区邻区瘦身.sort_values(by='切换总次数',ascending = False)


with pd.ExcelWriter(out_path + data_path.split('\\')[2][0:4] + '_小区邻区瘦身.xlsx') as writer:
    df_小区邻区瘦身.to_excel(writer,'小区邻区瘦身',index = False)


cell_neighbor_file = [x for x in os.listdir(out_path) if '小区邻区瘦身' in x ]

for file in cell_neighbor_file :
    df_小区邻区瘦身 = pd.read_excel(out_path + file, sheet_name='小区邻区瘦身')
    with open(cmd_path + file[0:4]+'小区邻区瘦身.txt','a') as f:
        for i in range(0,len(df_小区邻区瘦身),1):
            line = r'DEL 1X_LINKCELL:POS="{0}"-"{1}"-"{2}";'\
            .format(df_小区邻区瘦身.loc[i,'system'],
                    df_小区邻区瘦身.loc[i,'cellid'],
                    df_小区邻区瘦身.loc[i,'Ncell_pn'],
)
            f.write(line+'\n')

