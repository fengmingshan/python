# -*- coding: utf-8 -*-
"""
Created on Mon May 25 14:41:55 2020

@author: Administrator
"""

from flask import Flask,render_template,request
import os
from sklearn.externals import joblib
from keras.models import load_model
import re
import tensorflow as tf
from tensorflow.python.keras.backend import set_session
from keras.preprocessing import sequence
import jieba
import re

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


#定义读取停词表的函数
def loadStopWords():
    stop = []
    for line in open('./stopWord.txt').readlines():
        stop.append(line)
    return list(set(stop))


def replace_spcial(msg):
    msg = msg.replace('<br>','')
    msg = msg.replace('<b>','')
    msg = msg.replace('</b>','')
    msg = msg.replace('->','')
    msg = msg.replace('>', '')
    return msg


#定义切词函数
def cutWords(msg,stopWords):
    jieba.load_userdict("./userdict.txt")
    arr_leftWords=[]
    seg_list = jieba.cut(msg,cut_all=False)
    leftWords=''
    for i in seg_list:#for i in y,y可以是列表、元组、字典、Series
        if (i not in stopWords):
            leftWords+=' '+i
    leftWords.strip()
    arr_leftWords.append(leftWords)
    return arr_leftWords


# 读取data_path = r'D:\2020年工作\2020年NOC工单智能化项目'
os.chdir(data_path)


# 载入tokenizer模型用来统计词频
token = joblib.load('./token_file.pkl')
word_index = token.word_index


model = load_model('./lstm_model_15_epochs_nosample.h5')

# 读取分类字典
with open('./label_dict.txt','r') as f:
    label_dict = eval(f.read())


def pred_class(msg):
    global token,model,symbol_map

    msg = msg.translate(symbol_map)
    msg = replace_spcial(msg)

    stopWords = loadStopWords()
    X_cut = cutWords(msg,stopWords) # 分词
    xtest_seq = token.texts_to_sequences(X_cut) #

    max_len = 216
    xtest_pad = sequence.pad_sequences(xtest_seq, maxlen=max_len)

    # 预测
    y_pred_prob = model.predict(xtest_pad, verbose=0)[0]
    y_pred_list = y_pred_prob.tolist()
    y_pred_class = y_pred_list.index(max(y_pred_list))
    return y_pred_class

msg ='''
I运维账号18908760577消障情况描述局站是WS广南八宝百乐销障情况描述202055 150942直派岗位广南县现场综合化维护班组专业类型数据专业IPRAN414643242发生停电|欠压故障维护人员 陈富祥 赶往现场进行处置请填写故障处理过程市电恢复供电支撑有效性满意定位信息动环故障停电|欠压市电停电
'''
msg_label=1

msg1 ='''
I运维账号13330403337消障情况描述断点位置断点在 蒙自天马路电信公司 与 HH蒙自文澜红河卫生职业学院微站 之间销障情况描述202023 182809直派岗位蒙自现场综合化维护综合专业类型无线专业4GDBS3900_HH蒙自文澜绿宝银河大酒店LampsiteB1_FBTD_HFD发生光缆故障维护人员 杨志 赶往现场进行处置经过确认光缆断点位置在距离本端设备所属局站蒙自天马路电信公司1 公里处请填写故障处理过程光缆故障现已恢复断点用户机房1？处支撑有效性满意定位信息线路故障光缆故障经维护人员测试光缆断点位置在距离用户机房1公路处
'''
msg1_label =1

msg2 ='''
定位信息线路故障光缆故障经维护人员测试光缆断点位置在距离0机房0公里处断点位置 断点在 西华小学长青酒店之间消障情况描述20200308 085806直派岗位干线专业维护包区专业类型传输本地网1879西华小学发生光缆故障维护人员0赶往现场进行处置经过确认光缆断点位置在距离本端设备所属局站西华小学0公里处请填写故障处理过程黑乔母机房14公里处光缆被人为剪断现已抢修恢复支撑有效性满意
'''
msg2_label = 0

stopWords = loadStopWords()
cutword = cutWords(msg, stopWords)  # 分词
cutword = ' '.join(cutword)
y_pred = pred_class(msg)
label_text = label_dict.get(y_pred)
