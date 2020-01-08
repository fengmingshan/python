# -*- coding: utf-8 -*-
"""
Created on Tue May  8 13:38:13 2018

@author: alpha
"""

import pandas as pd
import jieba.posseg as pseg
import json  




num_classes = 6
vec_num = 100
num_words = 1030
max_len = 175



def fankui(text):
    '''
    去掉text中'姓名工号：'及之后的部分，第一个'反馈:'及之前的部分.
    '''
    result = text.split('姓名工号：')[0]   
    re = text.split('反馈:')[0]
    #result = result.strip(re+'反馈:')
    re = re+'反馈:'
    result = result.replace(re,' ')
    result.strip
    return result
    

#载入地名数据，用于区分国内外地名    
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
    对号码的粗略分类
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
    分词,并将词语做映射.
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

#读取词语字典。    
words_dict_file = r'data_dict/fk_words_dict.json'
f=open(words_dict_file,"r")  
for line in f:  
    words_dict = json.loads(line)
f.close()



def x_to_ins(words,words_dict=words_dict,max_len=max_len):
    '''
    利用词典将分词的输出词语映射为编号。
    '''
    result = [0]*max_len
    for i in range(min(max_len,len(words))):
        if words[i][0] in words_dict:
            result[i] = words_dict[words[i][0]]
        else:
            result[i] = words_dict['杂项']
    return result    
'''
def to_x(text,words_dict=words_dict,max_len=words_dict):
    x = []
    y = []

    for w in data:
        x.append(x_to_ins(w[2]))
        y.append(w[1]-1)
    return x,y
'''    
    
def fk_text_to_x(text,cut=True):
    '''
    整合上边的函数.
    '''
    if cut:
        text = fankui(text)
    result = jieba_pseg(text)
    result = x_to_ins(result)
    return result
    
    

if __name__=='__main__':
    text = '广东电信工位:2018-01-05 19:31:47:反馈:已电话通知集团上海NOC#02168563464.: 姓名工号：277: 联系电话020-87189115 '    
    print(fk_text_to_x(text)[:15])