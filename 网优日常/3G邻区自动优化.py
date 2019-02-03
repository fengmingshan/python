# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 14:54:34 2019

@author: Administrator
"""

import pandas as pd 
import numpy as np
import os
import xlwt
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
        txt2xls(data_path + file,data_path + file.replace('.txt','.xlsx'))
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
df_cell_neighbor['Ncell_index'] = df_carrier_neighbor['ncellsystemid'] + '_'  + df_carrier_neighbor['ncellid']    
df_cell_neighbor['操作类型'] = '正常'
df_cell_neighbor = df_cell_neighbor[['system','cellid','Scell_index','alias_b','pilot_pn','ncellsystemid','ncellid','neighbor_index']]
df_cell_neighbor = df_cell_neighbor.rename(columns ={'pilot_pn':'Ncell_pn','alias_b':'Ncell_name'})
df_cell_neighbor = pd.merge(df_cell_neighbor,df_cell_config,how = 'left', on = 'Scell_index')
df_切换次数 =  df_handover[['neighbor_index','切换总次数','切换成功次数','切换成功率(%)']]
df_cell_neighbor = pd.merge(df_cell_neighbor,df_切换次数,how = 'left', on = 'neighbor_index')
df_cell_neighbor.fillna(0,inplace = True)
df_cell_neighbor = df_carrier_neighbor[['system','cellid','carrierid','Scell_index','Scell_name','Scell_pn',
                                         'ncellsystemid','ncellid','Ncell_index','Ncell_name','Ncell_pn',
                                         '切换总次数','切换成功次数','切换成功率(%)','neighbor_index','操作类型']]    
# 合并处理载频邻区文件            
df_carrier_neighbor = pd.DataFrame()
for file in carrie_neighborr_files:
    df_tmp = pd.read_excel(data_path + file,skiprows = 1,dtype = str,encoding='utf-8') 
    df_carrier_neighbor = df_carrier_neighbor.append(df_tmp)

df_carrier_neighbor['neighbor_index'] = df_carrier_neighbor['system'] + '_' + df_carrier_neighbor['cellid'] + \
                                        '-' + df_carrier_neighbor['ncellsystemid'] + '_' + df_carrier_neighbor['ncellid']
df_carrier_neighbor['Scell_index'] =  df_carrier_neighbor['system'] + '_' + df_carrier_neighbor['cellid']
df_carrier_neighbor['Ncell_index'] = df_carrier_neighbor['ncellsystemid'] + '_'  + df_carrier_neighbor['ncellid']    
df_carrier_neighbor['操作类型'] = '正常'
df_carrier_neighbor = df_carrier_neighbor.rename(columns ={'pilot_pn':'Ncell_pn','alias_b':'Ncell_name'})
df_carrier_neighbor = pd.merge(df_carrier_neighbor,df_cell_config,how = 'left', on = 'Scell_index')
df_carrier_neighbor = pd.merge(df_carrier_neighbor,df_切换次数,how = 'left', on = 'neighbor_index')
df_carrier_neighbor.fillna(0,inplace = True)
df_carrier_neighbor = df_carrier_neighbor[['system','cellid','carrierid','Scell_index','Scell_name','Scell_pn',
                                             'ncellsystemid','ncellid','Ncell_index','Ncell_name','Ncell_pn',
                                             '切换总次数','切换成功次数','切换成功率(%)','neighbor_index','操作类型']]  
print('**********原始数据汇总完成!**********')
  
# =============================================================================
# 检查小区邻区
# =============================================================================
df_cell = df_cell_neighbor[['neighbor_index','Ncell_name','Ncell_pn',]]
df_cell_check = pd.merge(df_handover,df_cell,how = 'left',on = 'neighbor_index')
df_cell_check = df_cell_check[['system','cellid','Scell_index','Scell_name','Scell_pn','ncellsystemid',\
                               'ncellid','Ncell_index','Ncell_name','Ncell_pn','切换总次数',\
                               '切换成功次数','切换成功率(%)','neighbor_index']]
df_cell_check['切换总次数'] = df_cell_check['切换总次数'].astype(int)
df_cell_check['切换成功次数'] = df_cell_check['切换成功次数'].astype(int)
df_cell_check['切换成功率(%)'] = df_cell_check['切换成功率(%)'].astype(float)
df_cell_check['切换成功率(%)'] = df_cell_check['切换成功率(%)'].map(lambda x:round(x,3)*100)

df_cell_check = df_cell_check.sort_values(by='切换总次数',ascending = False) 
df_cell_check = df_cell_check[(df_cell_check['system'] != '65535')&(df_cell_check['ncellsystemid'] != '65535')]
df_cell_check['Ncell_pn'] =  df_cell_check['Ncell_pn'].fillna('-')
df_cell_check['操作类型'] = df_cell_check['Ncell_pn'].map(lambda x:'待定' if x == '-' else '正常') 
df_cell_check.drop('Ncell_name',axis = 1,inplace = True)
df_cell_check.drop('Ncell_pn',axis = 1,inplace = True)
df_cell_check = pd.merge(df_cell_check , df_neighbor_config , how = 'left' , on = 'Ncell_index')
df_cell_check = df_cell_check[['system','cellid','Scell_index','Scell_name','Scell_pn','ncellsystemid',
                               'ncellid','Ncell_index','Ncell_name','Ncell_pn','切换总次数','切换成功次数',
                               '切换成功率(%)','neighbor_index','操作类型']]

全量小区 = sorted(list(set(df_cell_check['Scell_index'])))
df_小区邻区替换 = pd.DataFrame() 
df_小区邻区删除 = pd.DataFrame() 
df_小区邻区添加 = pd.DataFrame() 

print('**********检查小区邻区!**********')
for cell in 全量小区:
    df_tmp = df_cell_check[df_cell_check['Scell_index'] == cell]
    df_tmp = df_tmp.reset_index()
    df_tmp.drop('index',axis = 1 , inplace = True)
    
    df_normal = df_cell_neighbor[df_cell_neighbor['Scell_index'] == 'cell']
    df_normal = df_normal.reset_index()
    df_normal.drop('index',axis = 1 , inplace = True)
    
    小区邻区数量 = len(df_normal)
    小区邻区PN列表 = list(df_normal['Ncell_pn'])
    if len(df_normal) > 0:
        最小切换次数 = df_normal.loc[len(df_normal)-1 , '切换总次数']
    else:
        最小切换次数 = 0

    for i in range(0,len(df_tmp),1):
        if df_tmp.loc[i,'操作类型'] == '待定':
            if 小区邻区数量 < 55 and df_tmp.loc[i,'切换总次数'] >= 10:
                df_tmp.loc[i,'操作类型'] = '添加'
                df_小区邻区添加 = df_小区邻区添加.append(df_tmp.loc[i,:])
                df_normal = df_normal.append(df_tmp.loc[i,:])
                df_normal.sort_values(by='切换总次数',ascending = False , inplace = True)
                df_normal = df_normal.reset_index()
                df_normal.drop('index',axis = 1 , inplace = True)
                小区邻区数量 += 1
            elif 小区邻区数量 >= 55 and df_tmp.loc[i,'切换总次数'] >= 10:
                if (df_tmp.loc[i,'切换总次数'] - 最小切换次数)/最小切换次数 >= 0.3:
                    if df_tmp.loc[i,'Ncell_pn'] not in 小区邻区PN列表:
                        df_tmp.loc[i,'操作类型'] = '替换'
                        df_normal.loc[len(df_normal)-1,'操作类型'] = '删除'
                        df_小区邻区添加 = df_小区邻区添加.append(df_tmp.loc[i,:])
                        df_小区邻区删除 = df_小区邻区删除.append(df_normal.loc[len(df_normal)-1,:])
                        df_小区邻区替换 = df_小区邻区替换.append(df_normal.loc[len(df_normal)-1,:])
                        df_小区邻区替换 = df_小区邻区替换.append(df_tmp.loc[i,:])
                        df_normal.drop(len(df_normal)-1 , inplace = True)
                        df_normal = df_normal.append(df_tmp.loc[i,:])
                        df_normal.sort_values(by='切换总次数',ascending = False , inplace = True)
                        df_normal = df_normal.reset_index()
                        df_normal.drop('index',axis = 1 , inplace = True)
                        最小切换次数 = df_normal.loc[len(df_normal)-1 , '切换总次数']
                        小区邻区PN列表 = list(df_normal['Ncell_pn'])

                    else :            
                        n = df_normal[df_normal['Ncell_pn'] == df_tmp.loc[i,'Ncell_pn']].index.values[0]
                        if df_tmp.loc[i,'切换总次数'] > df_normal.loc[n,'切换总次数']:
                            df_tmp.loc[i,'操作类型'] = '替换'  
                            df_小区邻区添加 = df_小区邻区添加.append(df_tmp.loc[i,:])
                            df_小区邻区删除 = df_小区邻区删除.append(df_normal.loc[n,:])
                            df_小区邻区替换 = df_小区邻区替换.append(df_normal.loc[n,:])
                            df_小区邻区替换 = df_小区邻区替换.append(df_tmp.loc[i,:])
                            df_normal.drop(n,inplace = True) 
                            df_normal.append(df_tmp.loc[i,:])
                            df_normal.sort_values(by='切换总次数',ascending = False , inplace = True)
                            df_normal = df_normal.reset_index()
                            df_normal.drop('index',axis = 1 , inplace = True)
                            最小切换次数 = df_normal.loc[len(df_normal)-1 , '切换总次数']
                            小区邻区PN列表 = list(df_normal['Ncell_pn'])

if len(df_小区邻区添加) > 0:
    df_小区邻区添加 = df_小区邻区添加[['system','cellid','Scell_index','Scell_name','Scell_pn',
                                     'ncellsystemid','ncellid','Ncell_index','Ncell_name','Ncell_pn',
                                     '切换总次数','切换成功次数','切换成功率(%)','neighbor_index','操作类型']]

if len(df_小区邻区删除) > 0:
    df_小区邻区删除 = df_小区邻区删除[['system','cellid','Scell_index','Scell_name','Scell_pn',
                                     'ncellsystemid','ncellid','Ncell_index','Ncell_name','Ncell_pn',
                                     '切换总次数','切换成功次数','切换成功率(%)','neighbor_index','操作类型']]
if len(df_小区邻区替换) > 0:
    df_小区邻区替换 = df_小区邻区替换[['system','cellid','Scell_index','Scell_name','Scell_pn',
                                     'ncellsystemid','ncellid','Ncell_index','Ncell_name','Ncell_pn',
                                     '切换总次数','切换成功次数','切换成功率(%)','neighbor_index','操作类型']]
with pd.ExcelWriter(out_path + data_path.split('\\')[2][0:4] + '_小区邻区检查结果.xlsx') as writer: #不用保存和退出，系统自动会完成
    df_小区邻区添加.to_excel(writer,'添加小区邻区',index = False) 
    df_小区邻区删除.to_excel(writer,'删除小区邻区',index = False) 
    df_小区邻区替换.to_excel(writer,'替换小区邻区',index = False) 

print('**********小区邻区检查完毕!**********')


# =============================================================================
# 汇总载频邻区
# =============================================================================
df_carrier = df_carrier_neighbor[['carrierid','neighbor_index','Ncell_name','Ncell_pn',]]
df_carrier_check = pd.merge(df_handover,df_carrier,how = 'left',on = 'neighbor_index')
df_carrier_check['切换总次数'] = df_carrier_check['切换总次数'].astype(int)
df_carrier_check['切换成功次数'] = df_carrier_check['切换成功次数'].astype(int)
df_carrier_check['切换成功率(%)'] = df_carrier_check['切换成功率(%)'].astype(float)
df_carrier_check['切换成功率(%)'] = df_carrier_check['切换成功率(%)'].map(lambda x:round(x,3)*100)

df_carrier_check = df_carrier_check.sort_values(by='切换总次数',ascending = False) 
df_carrier_check = df_carrier_check[(df_carrier_check['system'] != '65535')&(df_carrier_check['ncellsystemid'] != '65535')]
df_carrier_check['Ncell_pn'] =  df_carrier_check['Ncell_pn'].fillna('-')
df_carrier_check['操作类型'] = df_carrier_check['Ncell_pn'].map(lambda x:'待定' if x == '-' else '正常') 
df_carrier_check.drop('Ncell_name',axis = 1,inplace = True)
df_carrier_check.drop('Ncell_pn',axis = 1,inplace = True)
df_carrier_check = pd.merge(df_carrier_check , df_neighbor_config , how = 'left' , on = 'Ncell_index')
df_carrier_check = df_carrier_check[['system','cellid','carrierid','Scell_index','Scell_name','Scell_pn',
                                     'ncellsystemid','ncellid','Ncell_index','Ncell_name','Ncell_pn',
                                     '切换总次数','切换成功次数','切换成功率(%)','neighbor_index','操作类型']]
# =============================================================================
# 迭代检查载频邻区
# =============================================================================
全量小区 = sorted(list(set(df_carrier_check['Scell_index'])))
df_载频邻区替换 = pd.DataFrame() 
df_载频邻区添加 = pd.DataFrame() 
df_载频邻区删除 = pd.DataFrame() 

print('**********检查载频邻区!**********')
for cell in 全量小区:
    df_tmp = df_carrier_check[df_carrier_check['Scell_index'] == cell]
    df_tmp = df_tmp.reset_index()
    df_tmp.drop('index',axis = 1 , inplace = True)
    
    df_normal = df_carrier_neighbor[df_carrier_neighbor['Scell_index'] == cell]
    df_normal = df_normal.reset_index()
    df_normal.drop('index',axis = 1 , inplace = True)
    
    载频邻区数量 = len(df_normal)
    载频邻区PN列表 = list(df_normal['Ncell_pn'])
    if len(df_normal) > 0:
        最小切换次数 = df_normal.loc[len(df_normal)-1 , '切换总次数']
    else:
        最小切换次数 = 0

    for i in range(0,len(df_tmp),1):
        if df_tmp.loc[i,'操作类型'] == '待定':
            if 载频邻区数量 < 20 and df_tmp.loc[i,'切换总次数'] >= 10:
                df_tmp.loc[i,'操作类型'] = '添加'
                df_载频邻区添加 = df_载频邻区添加.append(df_tmp.loc[i,:])
                df_normal = df_normal.append(df_tmp.loc[i,:])
                df_normal.sort_values(by='切换总次数',ascending = False , inplace = True)
                df_normal = df_normal.reset_index()
                df_normal.drop('index',axis = 1 , inplace = True)
                载频邻区数量 += 1
                载频邻区PN列表 = list(df_normal['Ncell_pn'])
                最小切换次数 = df_normal.loc[len(df_normal)-1 , '切换总次数']
            elif 载频邻区数量 >= 20 and df_tmp.loc[i,'切换总次数'] >= 10:
                if (df_tmp.loc[i,'切换总次数'] - 最小切换次数)/最小切换次数 >= 0.3:
                    if df_tmp.loc[i,'Ncell_pn'] not in 载频邻区PN列表:
                        df_tmp.loc[i,'操作类型'] = '替换'
                        df_normal.loc[len(df_normal)-1,'操作类型'] = '删除'
                        df_载频邻区添加 = df_载频邻区添加.append(df_tmp.loc[i,:])
                        df_载频邻区删除 = df_载频邻区删除.append(df_normal.loc[len(df_normal)-1,:])
                        df_载频邻区替换 = df_载频邻区替换.append(df_normal.loc[len(df_normal)-1,:])
                        df_载频邻区替换 = df_载频邻区替换.append(df_tmp.loc[i,:])
                        df_normal.drop(len(df_normal)-1 , inplace = True)
                        df_normal = df_normal.append(df_tmp.loc[i,:])
                        df_normal.sort_values(by='切换总次数',ascending = False , inplace = True)
                        df_normal = df_normal.reset_index()
                        df_normal.drop('index',axis = 1 , inplace = True)
                        最小切换次数 = df_normal.loc[len(df_normal)-1 , '切换总次数']
                        载频邻区PN列表 = list(df_normal['Ncell_pn'])
                    else :
                        n = df_normal[df_normal['Ncell_pn'] == df_tmp.loc[i,'Ncell_pn']].index.values[0]
                        if df_tmp.loc[i,'切换总次数'] > df_normal.loc[n,'切换总次数']:
                            df_tmp.loc[i,'操作类型'] = '替换'
                            df_normal.loc[n,'操作类型'] = '删除'
                            df_载频邻区添加.append(df_tmp.loc[i,:])
                            df_载频邻区删除 = df_小区邻区删除.append(df_normal.loc[n,:])
                            df_载频邻区替换 = df_载频邻区替换.append(df_normal.loc[n,:])
                            df_载频邻区替换 = df_载频邻区替换.append(df_tmp.loc[i,:])
                            df_normal.drop(n,inplace = True) 
                            df_normal.append(df_tmp.loc[i,:])
                            载频邻区PN列表 = list(df_normal['Ncell_pn'])

if len(df_载频邻区添加) > 0:
    df_载频邻区添加 = df_载频邻区添加[['system','cellid','carrierid','Scell_index','Scell_name','Scell_pn',
                                     'ncellsystemid','ncellid','Ncell_index','Ncell_name','Ncell_pn',
                                     '切换总次数','切换成功次数','切换成功率(%)','neighbor_index','操作类型']]
if len(df_载频邻区删除) > 0:
    df_载频邻区删除 = df_载频邻区删除[['system','cellid','carrierid','Scell_index','Scell_name','Scell_pn',
                                     'ncellsystemid','ncellid','Ncell_index','Ncell_name','Ncell_pn',
                                     '切换总次数','切换成功次数','切换成功率(%)','neighbor_index','操作类型']]
if len(df_载频邻区替换) > 0 :
    df_载频邻区替换 = df_载频邻区替换[['system','cellid','carrierid','Scell_index','Scell_name','Scell_pn',
                                     'ncellsystemid','ncellid','Ncell_index','Ncell_name','Ncell_pn',
                                     '切换总次数','切换成功次数','切换成功率(%)','neighbor_index','操作类型']]

df_切换次数为零小区 = df_carrier_neighbor[df_carrier_neighbor['切换总次数'] == 0 ]


with pd.ExcelWriter(out_path + data_path.split('\\')[2][0:4] + '_小区邻区总表.xlsx') as writer: #不用保存和退出，系统自动会完成
    df_cell_neighbor.to_excel(writer,'小区邻区总表',index = False) 

with pd.ExcelWriter(out_path + data_path.split('\\')[2][0:4] + '_载频邻区总表.xlsx') as writer: #不用保存和退出，系统自动会完成
    df_carrier_neighbor.to_excel(writer,'载频邻区总表',index = False) 
    
with pd.ExcelWriter(out_path + data_path.split('\\')[2][0:4] + '_切换次数总表.xlsx') as writer: #不用保存和退出，系统自动会完成
    df_handover.to_excel(writer,'切换次数总表',index = False) 

with pd.ExcelWriter(out_path + data_path.split('\\')[2][0:4] +'_载频邻区检查结果.xlsx') as writer: #不用保存和退出，系统自动会完成
    df_载频邻区替换.to_excel(writer,'替换载频邻区',index = False) 
    df_载频邻区添加.to_excel(writer,'添加载频邻区',index = False) 
    df_载频邻区删除.to_excel(writer,'删除载频邻区',index = False) 
    df_切换次数为零小区.to_excel(writer,'切换次数为零',index = False) 
print('**********载频邻区检查完毕!**********')
