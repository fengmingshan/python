# -*- coding: utf-8 -*-
"""
Created on Mon May 21 09:40:15 2018

@author: alpha
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import jieba.posseg as pseg
import json
import os
#text = '上海电信工位:2018-01-04 16:25:10:反馈:我处15：44 用63591644话机拨打0080050405060听到“呼叫受限”语音提示，观察相应的呼叫主叫63591644 被叫0011950860155 已经上海ISC2-->美国VERIZON_MCI,请集团派境外协查。信令见附件。: 姓名工号：董基宇 '

datafile = r'data/fk.xlsx'
dict_savefile = r'data_dict/fk_words_dict.json'
#datafile = r'data/fk.xlsx'



def fankui(text):
    '''
    切分反馈信息
    '''
    result = text.split('姓名工号：')[0]   
    re = text.split('反馈:')[0]
    #result = result.strip(re+'反馈:')
    re = re+'反馈:'
    result = result.replace(re,' ')
    result.strip
    return result
    
    


#读取地名字典
dictfile3 = r'dict/adress_dict.xlsx'
adress_data = pd.read_excel(dictfile3, encoding = 'utf-8')
adress = list(adress_data[0])
ad_classes = list(adress_data[1])
n = len(adress)
adress_dict = {}
for i in range(n):
    adress_dict[adress[i]] = ad_classes[i]



def tel_num_check(num):
    '''
    判断号码
    '''
    str_num = str(num)
    head_num = str_num[:3]
    result = str_num
    if len(str_num)>6:
        result = '疑似电话号码'
    if (head_num=='400' or num=='800')and(len(str_num)>5) :
        result = '400800特殊号码'
    return result


def jieba_pseg(text,adress_dict=adress_dict):
    '''
    对text进行分词,并映射地名
    '''
    words = pseg.cut(text)
    words = [list(s) for s in words if s.flag is not 'x']    
    result = []
    for w in words:
        if w[0] in adress_dict:
            w[0] = adress_dict[w[0]]
        if w[1] == 'm':
            w[0] = tel_num_check(w[0])
        result.append(w)
    return result




def data_pretreat(data):
    '''
    对这个数据进行分词
    '''
    result = []
    for i in data:
        i[0] = fankui(i[0])
        i.append(jieba_pseg(i[0]))
        result.append(i)
    return result

      
def words_get(data):
    '''
    统计词典
    '''
    result = []
    for s in data:
        words = s[2]
        for w in words:
            if w[0] not in result:
                result.append(w[0])
    return result
    


def words_count(data,words):
    '''
    计算每个词语的出现次数
    '''
    n = len(data)
    result = {}
    for w in words:
        result[w] = 0
    for s in data:
        words = [w[0] for w in s[2]]
        words = list(set(words))
        for w in words:
            result[w] += 1
    return result,n
    


def words_data_get(words,words_count,paramater=6):
    '''
    对词语进行筛选
    '''
    result = []
    for w in words:
        if words_count[0][w]>=paramater:
            result.append(w)
    return result
    
    


def save_dict(words_dict_file,words_dict):
    '''
    保存字典
    '''
    if os.path.exists(words_dict_file):
        os.remove(words_dict_file)
    else:
        print ('no such file:%s'%words_dict_file)
    
    with open(words_dict_file,'a') as outfile:  
        json.dump(words_dict,outfile,ensure_ascii=False)  
        outfile.write('\n')  
    return



def get_max_len(data):
    '''
    获取最长句子词数
    '''
    
    max_len=0
    for w in data:
        if len(w[2])>max_len:
            max_len = len(w[2])
    max_len = int(0.9*max_len)
    return max_len


def to_xy(data,words_dict,max_len):
    '''
    转换为矢量格式的数据
    '''
    x = []
    y = []
    def x_to_ins(words):
        result = [0]*max_len
        for i in range(min(max_len,len(words))):
            if words[i][0] in words_dict:
                result[i] = words_dict[words[i][0]]
            else:
                result[i] = words_dict['杂项']
        return result
    for w in data:
        x.append(x_to_ins(w[2]))
        y.append(w[1]-1)
    return x,y





def cut_to_num(datafile,dict_savefile=dict_savefile,save=True,paramater=6):
    '''
    整合完整的流程
    '''
    data = pd.read_excel(datafile, encoding = 'utf-8')
    data = list(np.array(data))   
    data = [list(s) for s in data]#将学习集每行放入array[['国际公司综合处理:2018-01-01 10:11:27:反馈:国际公司->我处拨测正常,请重测: 姓名工号：国际公司->萧奋强 ', 1], ['上海电信工位:2018-01-01 10:01:06:反馈:附件: 姓名工号：戴晨晨: 联系电话13472638415 ', 2],。。。
    #print(data)
    data = data_pretreat(data)#[[' 国际公司->我处拨测正常,请重测: ', 1, [['国际', 'n'], ['公司', 'n'],

    words = words_get(data)#将学习集里出现的所有词语统计出来
    #print(words)
    count_total = words_count(data,words)#统计学习集中出现的所有词的词频({'国际': 2, '公司': 2, ...
    #print(count_total)
    words_data =words_data_get(words,count_total,paramater=paramater)#将词频出现超过paramater=6次的加入json文件中
    words_dict = {}
    n = len(words_data)
    for i in range(n):
        words_dict[words_data[i]] = i+1
    #print(n)
    words_dict['杂项'] = n+1
    n_words = len(words_dict) + 1
    #print(n_words)
    if save:
        words_dict_file = dict_savefile
        if os.path.exists(words_dict_file):
            os.remove(words_dict_file)
        else:
            print ('no such file:%s'%words_dict_file)
        
        with open(words_dict_file,'a') as outfile:  
            json.dump(words_dict,outfile,ensure_ascii=False)  
            outfile.write('\n')  
            
    save_dict(dict_savefile,words_dict)
    max_len = get_max_len(data)
    x,y = to_xy(data,words_dict,max_len)
    num_classes = max(y)+1

    return_dict = {
                    'x':x,             #文本分分词后的编码
                    'y':y,              #文本的分类
                    'data':data,        #文本整理后的原始数据
                    'max_len':max_len,  #最长的文本长度
                    'n_words':n_words,  #字典的词数
                    'num_classes':num_classes,#种类数
                
                   }
    return return_dict
    
    
    




if __name__ == '__main__':
    
    data_dict = cut_to_num(datafile,dict_savefile=dict_savefile,save=True,paramater=6)

