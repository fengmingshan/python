import pandas as pd
import numpy as np
import os
import jieba
from tqdm import tqdm
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM, GRU
from keras.models import Sequential
from keras.layers.embeddings import Embedding
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from keras.preprocessing import sequence, text
from keras.layers import GlobalMaxPooling1D, Conv1D, MaxPooling1D, Flatten, Bidirectional, SpatialDropout1D

#定义读取停词表的函数
def loadStopWords():
    stop = []
    for line in open('stopWord.txt').readlines():
        stop.append(line)
    return list(set(stop))


#定义切词函数
def cutWords(msgs,stopWords):
    arr_leftWords=[]
    seg_list = jieba.cut(msg,cut_all=False)
    leftWords=''
    for i in seg_list:
        if (i not in stopWords):
            leftWords+=' '+i
    leftWords.strip()
    arr_leftWords.append(leftWords)
    return arr_leftWords