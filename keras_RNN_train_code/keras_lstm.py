# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 07:42:06 2019

@author: Sharon Quartett
"""
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from keras.layers import LSTM
import keras
from keras import Input
from keras.layers import Bidirectional, TimeDistributed
#from AttentionLayerClass import AttentionLayer
import numpy as np
import matplotlib.pyplot as plt
import help_function as hf
import cut_to_num as ctn

'''
datafile:数据文件（xlsx格式）
dict_savefile：将词转换为数字编码的字典的存储路径（json格式）
modelf_savefile：模型保存路径（文件夹）
'''
datafile = r'data/fk.xlsx'
dict_savefile = r'data_dict/fk_words_dict.json'
modelf_savefile = r'model_data/rnn_checkpoint'
num_bat=7#7分数据
i=1#第一份数据作为测试集

data_dict = ctn.cut_to_num(datafile,dict_savefile=dict_savefile,save=True,paramater=6)
xy_dict = hf.data_fenpian(data_dict)
x_train = np.concatenate([xy_dict[j][0] for j in range(num_bat) if not(j==i)],axis=0)
y_train = np.concatenate([xy_dict[j][1] for j in range(num_bat) if not(j==i)],axis=0)
x_train = x_train.reshape((x_train.shape[0], 1, x_train.shape[1]))
y_train=keras.utils.to_categorical(y_train, num_classes=6)
x_test = xy_dict[i][0]
y_test = xy_dict[i][1]
x_test = x_test.reshape((x_test.shape[0], 1, x_test.shape[1]))
y_test=keras.utils.to_categorical(y_test, num_classes=6)
input_dim = x_test.shape

# 定义网络模型
model = Sequential()
#model.add(Embedding(input_dim, output_dim=100))
model.add(keras.layers.LSTM(60,return_sequences=True))
model.add(keras.layers.LSTM(40,return_sequences=True))
model.add(keras.layers.LSTM(25))
model.add(Dropout(0.3))
#model.add(Dense(50, activation='relu'))
model.add(Dense(12, activation='relu'))
#model.add(Dropout(0.2))
model.add(Dense(6, activation='softmax'))
model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

history=model.fit(x_train, y_train, batch_size=128, epochs=100,validation_data=(x_test, y_test),verbose=1)
#score = model.evaluate(x_test, y_test, batch_size=32)
# Plot training & validation accuracy values
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

# Plot training & validation loss values
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

#model.save('keras.h5') #保存
