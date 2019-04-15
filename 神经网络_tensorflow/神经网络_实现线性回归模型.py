# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 21:20:45 2018

@author: Administrator
"""

import tensorflow as tf
import numpy as np

def add_layer(inputs, in_size, out_size, activation_function=None):
    Weights = tf.Variable(tf.random_normal([in_size, out_size])) #权重
    biases = tf.Variable(tf.zeros([1, out_size]) + 0.1)  # 偏差
    Wx_plus_b = tf.matmul(inputs, Weights) + biases #输出 = 输入 * 权重 + 偏差
    if activation_function is None:
        outputs = Wx_plus_b
    else:
        outputs = activation_function(Wx_plus_b)
    return outputs

# x_data是由np.linspace()生成的一维数组，
#末尾乘上[:, np.newaxis]，相当与给x_data增加一个维度，变成二维
x_data = np.linspace(-1,1,300, dtype=np.float32)[:, np.newaxis]
noise = np.random.normal(0, 0.05, x_data.shape).astype(np.float32)
y_data = np.square(x_data) - 0.5 + noise
x_data.shape
y_data.shape
# 定义占位符输入变量
xs = tf.placeholder(tf.float32, [None, 1])
ys = tf.placeholder(tf.float32, [None, 1])

# 输入层1个，隐藏层10个，激励函数relu
l1 = add_layer(xs, 1, 10, activation_function=tf.nn.relu)

# 输入层10个，输出层1个，无激励函数
prediction = add_layer(l1, 10, 1, activation_function=None)

# 计算预测值prediction和真实值的误差，对二者差的平方求和再取平均。
loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys - prediction),
                     reduction_indices=[1]))

# 接下来，是很关键的一步，如何让机器学习提升它的准确率。
# tf.train.GradientDescentOptimizer()中的值通常都小于1，
# 这里取的是0.1，代表以0.1的效率来最小化误差loss。
train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

# 初始化
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

# 比如这里，我们让机器学习1000次。机器学习的内容是train_step,
# 用 Session 来 run 每一次 training 的数据，逐步提升神经网络的预测准确性。
# (注意：当运算要用到placeholder时，就需要feed_dict这个字典来指定输入。)
for i in range(1000):
    # training
    sess.run(train_step, feed_dict={xs: x_data, ys: y_data})
    if i % 50 == 0:
        # 每50步我们输出一下机器学习的误差。
        print(sess.run(loss, feed_dict={xs: x_data, ys: y_data}))
