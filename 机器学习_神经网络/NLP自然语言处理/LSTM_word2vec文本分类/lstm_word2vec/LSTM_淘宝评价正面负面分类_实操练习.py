# -*- coding: utf-8 -*-
"""
Created on  2018/5/18 13:30

@author: lhua
"""

from keras.models import model_from_yaml
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.recurrent import LSTM
from keras.layers.embeddings import Embedding
from keras.models import Sequential
import yaml
from sklearn.model_selection import train_test_split
import multiprocessing
from gensim.corpora.dictionary import Dictionary
from keras.preprocessing import sequence
from gensim.models import Word2Vec
import re
import jieba
import pandas as pd
import numpy as np
import imp
import sys
import os
imp.reload(sys)

data_path = 'D:/_python/python/机器学习_神经网络/文本分类/LSTM_word2vec文本分类/data'
os.chdir(data_path)


np.random.seed(1337)  # For Reproducibility
# the dimension of word vector
vocab_dim = 300
# sentence length
maxlen = 100
# iter num
n_iterations = 1
# the number of words appearing
n_exposures = 10
# what is the maximum distance between the current word and the prediction
# word in a sentence, what is the maximum distance between the current and
# the prediction word in a sentence
window_size = 7
# batch size
batch_size = 32
# epoch num
n_epoch = 20
# input length
input_length = 100
# multi processing cpu number
cpu_count = multiprocessing.cpu_count()

# 读取训练文件
def loadfile():
    neg = pd.read_excel('./data/neg.xls', header=None, index=None)
    pos = pd.read_excel('./data/pos.xls', header=None, index=None)
    # merge all data
    neg = np.array(neg[0])
    post = np.array(pos[0])
    return neg, post

# 读取停用词
def getstopword(stopwordPath):
    stoplist = set()
    for line in stopwordPath:
        stoplist.add(line.strip())
    return stoplist

# 分词和去停用词
def wordsege(text):
    # get disused words set
    stopwordPath = open('/data/stopwords.txt', 'r')
    stoplist = getstopword(stopwordPath)
    stopwordPath.close()

    # 分词和去停用词
    text_list = []
    for document in text:

        seg_list = jieba.cut(document.strip())
        fenci = []

        for item in seg_list:
            # 只保留不在停词表且不是数字的词r'-?\d+\.?\d*'匹配所有的正负整数小数
            if item not in stoplist and re.match(
                    r'-?\d+\.?\d*',
                    item) is None and len(
                    item.strip()) > 0:
                fenci.append(item)
        # if the word segmentation of the sentence is null,the label of the
        # sentence should be deleted accordingly
        if len(fenci) > 0:
            text_list.append(fenci)
    return text_list
