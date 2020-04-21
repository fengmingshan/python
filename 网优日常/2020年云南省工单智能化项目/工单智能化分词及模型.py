# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 23:59:24 2020

@author: Administrator
"""

import os
import jieba
import re
from tqdm import tqdm
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM, GRU
from keras.models import Sequential
from keras.layers.embeddings import Embedding
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from keras.preprocessing import sequence, text
from keras.layers import GlobalMaxPooling1D, Conv1D, MaxPooling1D, Flatten, Bidirectional, SpatialDropout1D

work_path = r'd:\_python\python\网优日常\2020年云南省工单智能化项目'
os.chdir(work_path)

msg = '''
1.投诉原因：用户因携号转网用户无法正常使用 引发用户投诉
2.核实情况：查HLR数据正常，查询AN-AAA正常、AAA正常
3.处理结果：查看移动未反馈，我方已催促移动处理。
4.回复用户情况：（录音流水号1901050000179166）12132回复用户认可、无异议
5. 说明备注：； <br><br><br><b>回访信息</b><br><b>总体情况</b>：满意；  <b>处理态度</b>：满意；   <b>处理及时性</b>：满意； <b>处理结果</b>：满意；  <br><br><b>结果说明</b><br><b>问题产生原因</b>：；   <br><br><b>采取措施</b>：；  <br><br><b>原因分类</b>：移动业务->终端及卡->用户端原因->用户自备设备或终端问题；<br><br><b>处理结果</b>：<br><b>责任定性</b>：企业原因；<br><br><b>考核原因</b>：；<br><br><b>责任部门</b>：市场部【64】；<br><br><b>CRM流水号(操作)</b>：99999999999999；<br><br><b>备注</b>：
'''

#定义读取停词表的函数
def loadStopWords():
    stop = []
    for line in open('stopWord.txt').readlines():
        stop.append(line)
    return list(set(stop))


#定义切词函数
def cutWords(msg,stopWords):
    jieba.load_userdict("userdict.txt")
    arr_leftWords=[]
    seg_list = jieba.cut(msg,cut_all=False)
    li = [i for i in seg_list if i not in stopWords]
    return li


def replace_spcial(msg):
    msg = msg.replace('<br>','')
    msg = msg.replace('<b>','')
    msg = msg.replace('</b>','')
    msg = msg.replace('->','')
    return msg


symbol_map = {
 ord('\n') : None,
 ord('\t') : None,
 ord('\r') : None,
 ord('①') : None,
 ord('②') : None,
 ord('③') : None,
 ord('④') : None,
 ord('【') : None,
 ord('】') : None,
 ord('(') : None,
 ord(')') : None,
 ord('（') : None,
 ord('）') : None,
 ord('：') : None,
 ord(':') : None,
 ord('-') : None,
 ord('；') : None,
 ord(';') : None,
 ord('，') : None,
 ord(',') : None,
 ord('。') : None,
 ord('.') : None,
 ord('、') : None
 ord('-') : None
 ord('——') : None
 ord('—') : None
 ord('/') : None
}

msg = msg.translate(symbol_map)
msg = replace_spcial(msg)
msg = re.sub('\d','',msg)


stopWords = loadStopWords()
li = cutWords(msg,stopWords)
