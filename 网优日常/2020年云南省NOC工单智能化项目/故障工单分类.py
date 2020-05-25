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
from func import symbol_map
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


data_path = 'E:/JupyterServer/Text_classify/static/'
os.chdir(data_path)

graph = tf.get_default_graph()
sess = tf.Session()
set_session(sess)

# 载入tokenizer模型用来统计词频
token = joblib.load('./token_file.pkl')
word_index = token.word_index

# 读取模型
model = load_model('./lstm_model_15_epochs_nosample.h5')

# 读取分类字典
with open('./label_dict.txt','r') as f:
    label_dict = eval(f.read())


def pred_class(msg):
    global token,model,symbol_map

    msg = msg.translate(symbol_map)
    msg = replace_spcial(msg)
    # 替换换行符
    msg = re.sub('\d','',msg)

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

@app.route('/',methods=['GET','POST'])
def text_classify():
    global graph,sess,label_dict
    form = Text_form()
    if request.method == 'POST':
        if form.validate_on_submit():
            res_dict = request.form.to_dict()
            msg = res_dict['content'].translate(symbol_map)
            msg = replace_spcial(msg)
            msg = re.sub('\d', '', msg)
            stopWords = loadStopWords()
            cutword = cutWords(msg, stopWords)  # 分词
            cutword = ' '.join(cutword)
            with graph.as_default():
                set_session(sess)
                y_pred = pred_class(msg)
                label_text = label_dict.get(y_pred)
            form.content.data = res_dict['content']
            form.cutword.data = cutword
            form.result.data = str(y_pred) + ': ' + label_text
            return render_template('index.html',form=form)
    return render_template('index.html',form=form)