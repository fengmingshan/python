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

X_tr.shape
y_tr.shape

def add_layer(inputs, in_size, out_size, activation_function=None):
    Weights = tf.Variable(tf.random_normal([in_size, out_size])) #权重
    biases = tf.Variable(tf.constant(0.1),[out_size])  # 偏差
    Wx_plus_b = tf.matmul(inputs, Weights) + biases #输出 = 输入 * 权重 + 偏差
    if activation_function is None:
        outputs = Wx_plus_b
    else:
        outputs = activation_function(Wx_plus_b)
    return outputs


# 定义占位符输入变量
xs = tf.placeholder(tf.float32, [None, 5])
ys = tf.placeholder(tf.float32, [None, 1])

# 输入层5个，隐藏层50个，激励函数relu
l1 = add_layer(xs, 5, 50, activation_function=tf.nn.relu)


# 输入层10个，输出层1个，无激励函数
prediction = add_layer(l1, 50, 1, activation_function=None)


# 计算预测值prediction和真实值的误差，对二者差的平方求和再取平均。
loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys - prediction),
                     reduction_indices=[1]))

# 接下来，是很关键的一步，如何让机器学习提升它的准确率。
# tf.train.GradientDescentOptimizer()中的值通常都小于1，
# 这里取的是0.1，代表以0.1的效率来最小化误差loss。
train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

# 初始化
init = tf.global_variables_initializer()

# 初始化保存器，用于保存训练模型
saver = tf.train.Saver()

with tf.Session() as sess:
    sess.run(init)

    # 比如这里，我们让机器学习7200次。机器学习的内容是train_step,
    # 用 Session 来 run 每一次 training 的数据，逐步提升神经网络的预测准确性。
    # (注意：当运算要用到placeholder时，就需要feed_dict这个字典来指定输入。)
    for i in range(7200):
        # training
        sess.run(train_step, feed_dict={xs: X_tr, ys: y_tr})
        if i % 500 == 0:
            # 每50步我们输出一下机器学习的误差。
            print(sess.run(loss, feed_dict={xs: X_tr, ys: y_tr}))
    
#     # Test model
#    correct_prediction = tf.equal(tf.argmax(prediction, 1), tf.argmax(y_te, 1))
#    # Calculate accuracy
#    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
#    print("Accuracy:", accuracy.eval({xs: X_te, ys: y_te}))
#    print(sess.run(loss, feed_dict={xs: X_te, ys: y_te}))
#    print(sess.run(prediction, feed_dict={xs: X_te, ys: y_te}))    
#    # Save model weights to disk
    save_path = saver.save(sess, r'd:\_python\python\神经网络_tensorflow\MR_data' + '\\')
    print("Model saved in file: %s" % save_path)    
    result = sess.run(prediction,feed_dict={xs: X_tr})
    result.dtype = 'float16'
    df_result = pd.DataFrame(result)
    df_result.to_csv(r'd:\_python\python\神经网络_tensorflow\MR_data' + '\\' + 'result.csv')


# =============================================================================
# 调用原来的训练结果，开始第二次训练
# =============================================================================
print("Starting 2nd session...")
with tf.Session() as sess:
    # Initialize variables
    sess.run(init)

    # Restore model weights from previously saved model
    saver.restore(sess, r'd:\_python\python\神经网络_tensorflow\MR_data' + '\\')
    print("Model restored from file: %s" % save_path)

    # Resume training
    for i in range(1800):
        # training
        sess.run(train_step, feed_dict={xs: X_te, ys: y_te})
        if i % 500 == 0:
            # 每50步我们输出一下机器学习的误差。
            print(sess.run(loss, feed_dict={xs: X_te, ys: y_te}))
    
     # Test model
    correct_prediction = tf.equal(tf.argmax(prediction, 1), tf.argmax(y_te, 1))
    # Calculate accuracy
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    print("Accuracy:", accuracy.eval({xs: X_te, ys: y_te}))
    
    # Save model weights to disk
    print("Model saved in file: %s" % save_path)
    print(sess.run(loss, feed_dict={xs: X_te, ys: y_te}))
    print(sess.run(prediction, feed_dict={xs: X_te}))   
    print("Second Optimization Finished!")
    result = sess.run(prediction, feed_dict={xs: X_te})
    result.dtype = 'float16'
    df_result = pd.DataFrame(result)
    df_result.to_csv(r'd:\_python\python\神经网络_tensorflow\MR_data' + '\\' + 'result.csv')
                                                        

