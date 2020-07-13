# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 10:09:11 2020

@author: Administrator
"""

import os
import pandas as pd
from sklearn.model_selection import train_test_split
import re

path = r'D:\_python\python\NLP\NOC工单分类_textCNN'
os.chdir(path)
if not os.path.exists(r'.\data'):
    os.mkdir(r'.\data')

df = pd.read_excel('训练集_合_6000.xlsx')

symbol_map = {
    ord('\n'): None,
    ord('\t'): None,
    ord('\r'): None,
    ord('①'): None,
    ord('②'): None,
    ord('③'): None,
    ord('④'): None,
    ord('【'): None,
    ord('】'): None,
    ord('('): None,
    ord(')'): None,
    ord('（'): None,
    ord('）'): None,
    ord('：'): None,
    ord(':'): None,
    ord('-'): None,
    ord('；'): None,
    ord(';'): None,
    ord('，'): None,
    ord(','): None,
    ord('。'): None,
    ord('.'): None,
    ord('、'): None,
    ord('-'): None,
    ord('—'): None,
    ord('/'): None,
}


def replace_spcial(msg):
    msg = msg.replace('<br>','')
    msg = msg.replace('<b>','')
    msg = msg.replace('</b>','')
    msg = msg.replace('->','')
    msg = msg.replace('>', '')
    msg = msg.replace('/n', '')
    msg = msg.replace('/t', '')
    msg = msg.replace(' ', '')
    return msg


df['label'] = df['打标'].map(lambda x:0 if x =='规范' else 1 )

# 处理text中的特殊字符
df['text'] = df['提请销障内容'].map(lambda x:x.translate(symbol_map)) # 替换特殊符号
df['text'] = df['text'].map(lambda x:replace_spcial(x)) # 替html格式
df['text'] = df['text'].map(lambda x:re.sub(r'1\d{10}','telnum',x)) # 替换电话号码

# 拆分训练集和测试集
X_train, X_test_vaild, y_train, y_test_vaild = train_test_split(df.text, df.label, test_size=0.4, stratify=df.label, shuffle=True, random_state=41)

X_test,X_vaild,y_test,y_vaild = train_test_split(X_test_vaild, y_test_vaild, test_size=0.5, stratify=y_test_vaild, shuffle=True, random_state=41)

with open('./data/train.txt','w',encoding='utf-8') as f:
    for x,y in zip(X_train,y_train):
        f.writelines(x+'\t'+str(y)+'\n')

with open('./data/test.txt','w',encoding='utf-8') as f:
    for x,y in zip(X_test,y_test):
        f.writelines(x+'\t'+str(y)+'\n')


with open('./data/dev.txt','w',encoding='utf-8') as f:
    for x,y in zip(X_vaild,y_vaild):
        f.writelines(x+'\t'+str(y)+'\n')

with open('./data/class.txt','w',encoding='utf-8') as f:
    f.writelines('correct')
    f.writelines('\n')
    f.writelines('inaccuracy')

