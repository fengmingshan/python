# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 13:09:37 2018
获取鼠标当前坐标
@author: Administrator
"""

import pandas as pd
import os
import PySimpleGUI as sg


sg.change_look_and_feel('DarkAmber')   # Add a style
# 定义GUI窗体布局
layout = layout = [[sg.Text('打资金往来文件')],
                   [sg.Input('d:/'),
                    sg.FilesBrowse(file_types=(('任意格式', '*.*'),('Excel2007', '*.xlsx'), ('Excel2003', '*.xls'),), initial_folder='d:/')],
                   [sg.Text('打开项目名称与客户名称对应表')],
                   [sg.Input('d:/'),
                    sg.FilesBrowse(file_types=(('任意格式', '*.*'),('Excel2007', '*.xlsx'), ('Excel2003', '*.xls'),), initial_folder='d:/')],
                   [sg.Button('开始核对'),
                    sg.Button('退出')]]
# 新建窗体，引用之前定义好的布局
window = sg.Window('计算基站距离小程序', layout)

def getNumofCommonSubstr(str1, str2):

    lstr1 = len(str1)
    lstr2 = len(str2)
    record = [[0 for i in range(lstr2+1)] for j in range(lstr1+1)]
    #开辟列表空间 为什么要多一位呢?主要是不多一位的话,会存在边界问题
    # 多了一位以后就不存在超界问题
    maxNum = 0   # 最长匹配长度
    p = 0    # 匹配的起始位

    for i in range(lstr1):
        for j in range(lstr2):
            if str1[i] == str2[j]:
    # 相同则累加
                record[i+1][j+1] = record[i][j] + 1
                if record[i+1][j+1] > maxNum:
     # 获取最大匹配长度
                     maxNum = record[i+1][j+1]
     # 记录最大匹配长度的终止位置
                     p = i + 1
    return (str1[p-maxNum:p], maxNum)

while True:
    event, values = window.read()
    file_list = values[0].split(',')
    cust_file = values[1]
    out_path = '/'.join(file_list[0].split('/')[:-1])+'/核对结果/'
    if not os.path.exists(out_path):
        os.mkdir(out_path)
    if event in (None, '退出'):  # if user closes window or clicks cancel
        break
    elif event in ('开始核对'):
        sg.Print('你选择的资金往来共有{}。'.format(len(file_list)))
        for i,file in enumerate(file_list):
            sg.Print('文件{} : {}。'.format(i, file))

        df_pro2cus = pd.read_excel(cust_file)
        dict_pro2cus = {k:v for k,v in zip(df_pro2cus['项目名称'], df_pro2cus['客商名称'])}

        df_list = []
        for file in file_list:
            df_tmp = pd.read_excel(file)
            subject = df_tmp.iloc[5,1][1:-1]
            col = df_tmp.loc[6,:]
            df_tmp.drop(range(8),axis = 0 ,inplace =True)
            df_tmp.columns = col
            # 删除账套合计行
            df_tmp = df_tmp[pd.isnull(df_tmp['摘要'])]
            df_tmp = df_tmp.iloc[:,[1,2,20,22]]
            df_tmp['科目'] = subject
            df_list.append(df_tmp)
        df = pd.concat(df_list, axis = 0)
        df.fillna(0,inplace = True)
        set_project = set(df['项目辅助核算名称'])
        set_customer = set(df['客商辅助核算名称'])

        same_name = set_project & set_customer
        different_project = list(set_project - same_name)
        different_customer = list(set_customer - same_name)

        fit_dict = {}
        not_fit_dict = {}
        for name in different_project:
            max_fit_list = [getNumofCommonSubstr(name, x)[1] for x in different_customer]
            name_fit_dict = {k:v for k,v in zip(different_customer,max_fit_list)}
            if max(zip(name_fit_dict.values(), name_fit_dict.keys()))[0]>=5:
                fit_dict[name] = max(zip(name_fit_dict.values(), name_fit_dict.keys()))[1]
            else:
                not_fit_dict[name] = max(zip(name_fit_dict.values(), name_fit_dict.keys()))[1]

        fit_dict = {k:v for k,v in fit_dict.items() if k not in dict_pro2cus.keys()}
        dict_pro2cus = dict(dict_pro2cus, **fit_dict)

        df_customer = pd.DataFrame({'项目名称':list(dict_pro2cus.keys()),'客商名称':list(dict_pro2cus.values())})
        with pd.ExcelWriter(out_path + '项目名称与客商名称匹配结果.xlsx') as f:
            df_customer.to_excel(f,'项目名称与客商名称自动匹配结果',index =False)
        with open(out_path + '项目名称匹配不到客商名称.txt','w') as f:
            for x in not_fit_dict.keys():
                f.writelines(x+'\n')

        # 保留有用字段
        df.rename(columns = {'原币':'期末余额'}, inplace =True)
        df['期末余额'] = df['期末余额'].astype(float)
        df['对应客商名称_自动匹配'] = ''
        df['对应客商名称_自动匹配'][df['项目辅助核算名称'].isin(dict_pro2cus.keys())] = df['项目辅助核算名称'][df['项目辅助核算名称'].isin(dict_pro2cus.keys())].map(dict_pro2cus)
        df['direction'] = df['客商辅助核算名称'] + '-->' + df['项目辅助核算名称']

        df2 = df.copy(deep=True)
        df2['direction'] = df['项目辅助核算名称'] + '-->' + df['客商辅助核算名称']
        df2 = df2[['direction','方向','期末余额']]
        df2.set_index('direction',inplace = True)
        number_dict = df2['期末余额'].to_dict()
        direct_dict = df2['方向'].to_dict()

        df['期末余额2'] = df['direction'].map(number_dict)
        df['方向2'] = df['direction'].map(direct_dict)
        df['差额'] = df['期末余额'] - df['期末余额2']
        df['核对结果'] = ''
        df['核对结果'][df['差额'] == 0] = '正常'
        df['核对结果'][df['差额'] > 0] = '金额不平'
        df['核对结果'][pd.isnull(df['期末余额2'])] = '对方账目未找到'
        df_res = df[['项目辅助核算名称', '对应客商名称_自动匹配', '客商辅助核算名称', '科目', '方向', '期末余额', '核对结果', '差额']]
        with pd.ExcelWriter(out_path + '_资金往来自动核对结果.xlsx') as f:
            df_res.to_excel(f, '资金往来核对结果', index =False)
            df.to_excel(f, '原始数据', index =False)
        sg.Print('核对已完成,结果已输出到 {} ,文件名："_资金往来自动核对结果.xlsx"'.format(out_path))
        os.startfile(out_path)
