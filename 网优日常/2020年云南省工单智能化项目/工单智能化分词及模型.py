# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 23:59:24 2020

@author: Administrator
"""

import os
import jieba
import re
import numpy as np
from tqdm import tqdm
from sklearn.externals import joblib
import gensim
from keras.models import load_model

work_path = 'D:/2020年工作/2020年工单智能化项目/'
os.chdir(work_path)

token = joblib.load('./token_file.pkl') # 载入tokenizer模型

# 加载自己以前训练的词向量
w2vModel = gensim.models.Word2Vec.load('./w2vModel.model')
embeddings_dict = dict(zip(w2vModel.wv.index2word, w2vModel.wv.vectors))

word_index = token.word_index
# 基于已有的数据集中的词汇创建一个词嵌入矩阵（Embedding Matrix），需要参与神经网络模型训练
embedding_matrix = np.zeros((len(word_index) + 1, 100))
for word, i in tqdm(word_index.items()):
    embedding_vector = embeddings_dict.get(word)
    if embedding_vector is not None:
        embedding_matrix[i] = embedding_vector
# 读取模型
model = load_model('./lstm_model_10_epochs_maxlen127.h5')

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
    leftWords=''
    for i in seg_list:#for i in y,y可以是列表、元组、字典、Series
        if (i not in stopWords):
            leftWords+=' '+i
    leftWords.strip()
    arr_leftWords.append(leftWords)
    return arr_leftWords

def replace_spcial(msg):
    msg = msg.replace('<br>','')
    msg = msg.replace('<b>','')
    msg = msg.replace('</b>','')
    msg = msg.replace('->','')
    return msg

def pred_class(msg):
    msg = msg.translate(symbol_map)
    msg = replace_spcial(msg)
    msg = re.sub('\d','',msg)

    stopWords = loadStopWords()
    X_cut = cutWords(msg,stopWords) # 分词
    xtest_seq = token.texts_to_sequences(X_cut) #

    max_len = 127
    xtest_pad = sequence.pad_sequences(xtest_seq, maxlen=max_len)

    # 预测
    y_pred_prob = model.predict(xtest_pad, verbose=0)[0]
    y_pred_list = y_pred_prob.tolist()
    y_pred_class = y_pred_list.index(max(y_pred_list))
    return y_pred_class


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
 ord('、') : None,
 ord('-') : None,
 ord('—') : None,
 ord('/') : None,
}


msg1 = '''
1.投诉原因：用户因携号转网用户无法正常使用 引发用户投诉
2.核实情况：查HLR数据正常，查询AN-AAA正常、AAA正常
3.处理结果：查看移动未反馈，我方已催促移动处理。
4.回复用户情况：（录音流水号1901050000179166）12132回复用户认可、无异议
5. 说明备注：； <br><br><br><b>回访信息</b><br><b>总体情况</b>：满意；  <b>处理态度</b>：满意；   <b>处理及时性</b>：满意； <b>处理结果</b>：满意；  <br><br><b>结果说明</b><br><b>问题产生原因</b>：；   <br><br><b>采取措施</b>：；  <br><br><b>原因分类</b>：移动业务->终端及卡->用户端原因->用户自备设备或终端问题；<br><br><b>处理结果</b>：<br><b>责任定性</b>：企业原因；<br><br><b>考核原因</b>：；<br><br><b>责任部门</b>：市场部【64】；<br><br><b>CRM流水号(操作)</b>：99999999999999；<br><br><b>备注</b>：
'''
msg1_class = 72

msg2 = '''
①投诉原因：因有信号无法正常使用引发用户的投诉
②核实情况：根据用户诉求查询AN-AAA正常、AAA正常，HLR状态正常
③处理结果：投诉原因：市电停电，富宁里达共移动基站目前已经恢复正常，联系用户，用户不在投诉区域，建议用户返还投诉区域后使用观察，用户表示认可
④回复用户情况：（录音流水号 1901050000212832 ）12947回复用户认可、无异议
⑤说明备注：无； <br><br><br><b>回访信息</b><br><b>总体情况</b>：满意；  <b>处理态度</b>：满意；   <b>处理及时性</b>：满意； <b>处理结果</b>：满意；  <br><br><b>结果说明</b><br><b>问题产生原因</b>：；   <br><br><b>采取措施</b>：；  <br><br><b>原因分类</b>：移动业务->移动语音网络->无线网络原因->基站故障->基站设备故障；<br><br><b>处理结果</b>：<br><b>责任定性</b>：企业原因；<br><br><b>考核原因</b>：；<br><br><b>责任部门</b>：文山分公司【876】；<br><br><b>CRM流水号(操作)</b>：99999999999999；<br><br><b>备注</b>：
'''
msg2_class = 23


msg3 = '''
1.投诉原因：用户因网速慢 引发用户投诉
2.核实情况：查HLR数据正常，查询AN-AAA正常、AAA正常
3.处理结果：经核实，分公司投诉处理员16613联系用户核实使用情况，男机主本人接听 ，用户反映在腾冲天诚商业街使用，有4G网络，但网速慢，离开该区域未好转，经网络部核实该区域基站信号正常。投诉处理员16613联系用户解释，请用至营业厅检查终端或更换UIM卡，用户对处理结果认可。
4.回复用户情况：（录音流水号1901040000416164 ）分公司已经联系用户解释
5. 说明备注：； <br><br><br><b>回访信息</b><br><b>总体情况</b>：满意；  <b>处理态度</b>：满意；   <b>处理及时性</b>：满意； <b>处理结果</b>：满意；  <br><br><b>结果说明</b><br><b>问题产生原因</b>：；   <br><br><b>采取措施</b>：；  <br><br><b>原因分类</b>：移动业务->终端及卡->用户端原因->用户自备设备或终端问题；<br><br><b>处理结果</b>：<br><b>责任定性</b>：用户原因；<br><br><b>考核原因</b>：；<br><br><b>责任部门</b>：；<br><br><b>CRM流水号(操作)</b>：99999999999999；<br><br><b>备注</b>：经核实，分公司投诉处理员16613联系用户核实使用情况，男机主本人接听 ，用户反映在腾冲天诚商业街使用，有4G网络，但网速慢，离开该区域未好转，经网络部核实该区域基站信号正常。投诉处理员16613联系用户解释，请用至营业厅检查终端或更换UIM卡，用户对处理结果认可
'''
msg3_class = 54


y_pred1 = pred_class(msg1)
y_pred2 = pred_class(msg2)
y_pred3 = pred_class(msg3)

for cla,y in  zip([msg1_class,msg2_class,msg3_class],[y_pred1,y_pred2,y_pred3]):
    print(
        'msg1 class is : {cla}, msg1 prediction is : {pred}'.format(
            cla=cla,
            pred=y))



