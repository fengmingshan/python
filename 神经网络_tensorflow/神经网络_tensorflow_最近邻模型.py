# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 21:24:10 2018

@author: Administrator
"""

import numpy as np
import tensorflow as tf

# Import MINST data
from tensorflow.examples.tutorials.mnist import input_data

data_path = 'd:\_python\python\神经网络_tensorflow\mnist_data' + '\\'
mnist = input_data.read_data_sets(data_path, one_hot=True)

# 限制以下 mnist data的大小
Xtr, Ytr = mnist.train.next_batch(5000)  # 5000个用于训练
Xte, Yte = mnist.test.next_batch(200)  # 200个用于测试

# 定义 tf 计算图 输入占位符
xtr = tf.placeholder("float", [None, 784])
xte = tf.placeholder("float", [784])

# 最近邻算法使用 L1 Distance
# 计算 L1 Distance
# tf.negative()取反，tf.reduce_sum()压缩求和，用于对数据降维
# 距离算法可以这样理解：计算xtr-xte，再取绝对值，然后对得到的矩阵按行求和进行降维。reduction_indices=1，按行求和
distance = tf.reduce_sum(tf.abs(tf.add(xtr, tf.negative(xte))), reduction_indices=1)
# 预测: 计算最小距离的index (最近邻)。tf.argmin（）返回矩阵横列或者纵列的最小值的坐标
pred = tf.argmin(distance, 0)

accuracy = 0.

# 初始化变量
init = tf.global_variables_initializer()

# 开始训练
with tf.Session() as sess:
    sess.run(init)
    
    for i in range(len(Xte)):
        # 计算最近邻
        print(distance)
        nn_index = sess.run(pred, feed_dict={xtr: Xtr, xte: Xte[i, :]})
        # 获取最近的类标签，并将其与真正的标签进行比较
        # np.argmax（）返回矩阵横列或者纵列的最小值的坐标
        print("Test", i, "Prediction:", np.argmax(Ytr[nn_index]), \
            "True Class:", np.argmax(Yte[i]))
        # 计算精确度
        if np.argmax(Ytr[nn_index]) == np.argmax(Yte[i]):
            accuracy += 1./len(Xte)
        print("Done!")
        print("Accuracy: %i " % accuracy)
