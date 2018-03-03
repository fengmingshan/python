# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 17:10:05 2018
#####   python实战之实现excel读取、统计、写入    ######
背景
图像领域内的一个国内会议快要召开了，要发各种邀请邮件，之后要录入、统计邮件回复（参会还是不参会等）。
如此重要的任务，老师就托付给我了。ps: 统计回复邮件的时候，能知道谁参会或谁不参会。
而我主要的任务，除了录入邮件回复，就是统计理事和普通会员的参会情况了（参会的、不参会的、没回复的）。
录入邮件回复信息没办法只能人工操作，但如果统计也要人工的话，
那工作量就太大了（比如在上百人的列表中搜索另外上百人在不在此列表中！！）
于是就想到了用python来帮忙，花两天时间不断修改，写了6个版本。。。
@author: Administrator
"""
#   ###version_final
import os
import numpy as np
import pandas as pd
os.chdir('C:\\Users\\dell\\Desktop')
print('work_directory: ', os.getcwd())

loadfile_sheet = ['理事与会员名单.xlsx','理事与会员名单']
common_columns = ['回执参加','回执不参加']
concerned_columns = ['理事','会员']
disp_columns = ['参会','不参会','未回执']
savefile_sheet = ['理事和会员回执统计.xlsx','理事回执统计','会员回执统计']


def disp(ss, cap, num = True):
    #功能：显示名单
    #ss  : 名单集合
    #cap ：开头描述
    print(cap,'({})'.format(len(ss)))
    for i in range(np.ceil(len(ss)/5).astype(int)):
        pre = i * 5
        nex = (i+1) * 5
        #调整显示格式
        dd = ''
        for each in list(ss)[pre:nex]:
            if len(each) == 2:
                dd = dd + '    ' + each
            elif len(each) == 3:
                dd = dd + '  ' + each
            else:
                dd = dd + '' + each
        print('{:3.0f} -{:3.0f} {}'.format(i*5+1,(i+1)*5,dd))

def trans_pd(df,ll,cap,i=1):
    #功能：生成三列--空列、序号列、数据列
    #df  : DataFrame结构
    #ll  : 列表
    #cap : 显示的列名
    #i   : 控制空列的名字
    df['_'*i]=pd.DataFrame([''])
    if len(set(ll)) == 1:
        df['序号{}'.format(i)] = np.NaN
        df[cap] = np.NaN
    else:
        df['序号{}'.format(i)] = pd.DataFrame(np.arange(len(set(ll))-1)+1)
        df[cap] = pd.DataFrame(ll)    
    return df

def prep(ss, N):
    #功能：预处理，生成列表，并补齐到长度N
    #ss  : 集体
    #N   ：长度
    ll = list(ss)
    L = len(ll)
    ll.extend([np.NaN] * (N-L))
    return ll


def get_df(loadfile_sheet,common_columns,concerned_column,disp_columns, display = True):
    #1. 载入excel
    data = pd.read_excel(loadfile_sheet[0],loadfile_sheet[1])    
    common_set1 = set(data[common_columns[0]])
    common_set2 = set(data[common_columns[1]])    
    concerned_set = set(data[concerned_column])
    common_set1.discard(np.NaN)
    common_set2.discard(np.NaN)
    concerned_set.discard(np.NaN)

    #2. 统计
    concerned_in_set_1 = set([])
    concerned_in_set_2 = set([])
    concerned_in_no_set = set([])
    for each in concerned_set:
        if each in common_set1:
            concerned_in_set_1.add(each)
        elif each in common_set2:
            concerned_in_set_2.add(each)
        else:
            concerned_in_no_set.add(each)

    #3. 显示
    if display:
        disp(concerned_in_set_1,'\n'+disp_columns[0]+concerned_column)
        disp(concerned_in_set_2,'\n'+disp_columns[1]+concerned_column)
        disp(concerned_in_no_set,'\n'+disp_columns[2]+concerned_column)

    #4. 返回DataFrame
    N = np.max([len(concerned_in_set_1),len(concerned_in_set_2),len(concerned_in_no_set)])
    concerned_in_set_1_list = prep(concerned_in_set_1,N)
    concerned_in_set_2_list = prep(concerned_in_set_2,N)
    concerned_in_no_list = prep(concerned_in_no_set,N)

    df = pd.DataFrame(concerned_in_set_1_list,columns = [disp_columns[0]])
    df = trans_pd(df,concerned_in_set_2_list,disp_columns[1])
    df = trans_pd(df,concerned_in_no_list,disp_columns[2],2)
    df.index = df.index + 1

    return df

def save2excel(df, concerned_column, savefile_sheet):
    L = len(savefile_sheet) - 1
    idx = 0
    for i in np.arange(L)+1:
        if concerned_column in savefile_sheet[i]:
            idx = i
            break
    if idx != 0: #如果有对应sheet           
        names = locals()
        for i in np.arange(L)+1:
            if i != idx:
                names['df%s' % i] = pd.read_excel(savefile_sheet[0], sheet_name=savefile_sheet[i])
        writer = pd.ExcelWriter(savefile_sheet[0])
        for i in np.arange(L)+1:
            if i != idx:
                names['df%s' % i].to_excel(writer, sheet_name=savefile_sheet[i])
            else:
                df.to_excel(writer, sheet_name=savefile_sheet[i])
        writer.save()
    else: #如果没有对应sheet，创建一个新sheet         
        names = locals()
        for i in np.arange(L)+1:
                names['df%s' % i] = pd.read_excel(savefile_sheet[0], sheet_name=savefile_sheet[i])
        writer = pd.ExcelWriter(savefile_sheet[0])
        for i in np.arange(L)+1:
                names['df%s' % i].to_excel(writer, sheet_name=savefile_sheet[i])
        df.to_excel(writer, sheet_name=concerned_column)
        writer.save()
    print('writing success')


if __name__ == '__main__':
    for concerned_column in concerned_columns:
        df = get_df(loadfile_sheet,common_columns,
                    concerned_column,disp_columns, display = True)
        save2excel(df, concerned_column, savefile_sheet)