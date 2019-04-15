# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 11:09:00 2018

@author: Administrator
"""

import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


data_path = 'd:\_python\python\神经网络_tensorflow\MR_data' +'\\'

# =============================================================================
#  单层神经网络
# =============================================================================
MR_data = pd.read_csv(data_path + 'MR_1neighbor.csv', engine = 'python')
# 先对数据进行处理
bin1 = list(range(-20,30,1))
bin2 =[x+0.5 for x in bin1 ]
cut_bin = bin1 + bin2
cut_bin.sort()

def get_near(x):
    for i in range(0,len(cut_bin)-1,1):
        if  cut_bin[i] <= x <= cut_bin[i+1]:
            if abs(cut_bin[i+1] - x )> abs(cut_bin[i] - x ):
                return cut_bin[i]                
            else :
                return cut_bin[i+1]
            
MR_data['SINR'] = MR_data['SINR'].map(lambda x:get_near(x))               

y = MR_data['SINR']

X = MR_data.drop('SINR',axis = 1)
cols = X.columns
for col in cols:
     X[col] = X[col].astype(np.float32)

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2)

X_tr = np.array(X_tr)
X_te = np.array(X_te)
y_tr = np.array(y_tr)[:, np.newaxis]
y_te = np.array(y_te)[:, np.newaxis]

numClasses = 1
inputSize = 5 
numHiddenUnits = 50 
trainingIterations = 9000 
 
# 定义占位符输入变量

X = tf.placeholder(tf.float32, shape = [None, inputSize])
y = tf.placeholder(tf.float32, shape = [None, numClasses])


W1 = tf.Variable(tf.truncated_normal([inputSize, numHiddenUnits], stddev=0.1))
B1 = tf.Variable(tf.constant(0.1), [numHiddenUnits])
W2 = tf.Variable(tf.truncated_normal([numHiddenUnits, numClasses], stddev=0.1))
B2 = tf.Variable(tf.constant(0.1), [numClasses])

W1 = tf.cast(W1, tf.float32)  
B1 = tf.cast(B1, tf.float32)
W2 = tf.cast(W2, tf.float32)  
B2 = tf.cast(B2, tf.float32)

hiddenLayerOutput = tf.matmul(X_tr, W1) + B1
hiddenLayerOutput = tf.nn.relu(hiddenLayerOutput)
finalOutput = tf.matmul(hiddenLayerOutput, W2) + B2

loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels = y_tr, logits = finalOutput))
opt = tf.train.GradientDescentOptimizer(learning_rate = 0.1).minimize(loss)

correct_prediction = tf.equal(tf.argmax(finalOutput,1), tf.argmax(y_tr,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))


with tf.Session() as sess:
    init = tf.global_variables_initializer()
    sess.run(init)
    for i in range(7200):
        # training
        _, trainingLoss = sess.run([opt, loss], feed_dict={X: X_tr, y: y_tr})
        if i % 200 == 0:
            # 每50步我们输出一下机器学习的误差。
            print(sess.run(loss, feed_dict={X: X_tr, y: y_tr}))
    result = sess.run(finalOutput, feed_dict={X: X_tr})
    result.dtype = 'float16'
    df_result = pd.DataFrame(result)
    df_result.to_csv(r'd:\_python\python\神经网络_tensorflow\MR_data' + '\\' + 'result.csv')
