# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 08:46:34 2018

@author: Administrator
"""
import tensorflow as tf
import numpy as np

# =============================================================================
# 第一个小例子：
# =============================================================================
## 创建测试数据
x_data = np.random.rand(100).astype(np.float32)
y_data = x_data * 0.1 + 0.3

###----------创建结构开始----------###
# 搭建模型
Weights = tf.Variable(tf.random_uniform([1],-1,1.0))
biases = tf.Variable(tf.zeros([1]))

y = x_data * Weights + biases

# 计算误差
loss = tf.reduce_mean(tf.square(y-y_data))

# 反向传递，优化权重和偏置
optimizer = tf.train.GradientDescentOptimizer(0.5)
train = optimizer.minimize(loss)

###----------创建结构结束----------###

# 初始化结构
init = tf.global_variables_initializer()
# 获取Session
sess = tf.Session()
# 用Session进行初始化
sess.run(init)

# 开始训练
for step in range(201):
    sess.run(train)
    # 每20步输出权重和偏置
    if step%20 == 0:
        print(step,sess.run(Weights),sess.run(biases))
        
        

# =============================================================================
# 第二个例子：
# =============================================================================
import tensorflow as tf

# 定义两个常量
matrix1 = tf.constant([[3,3]])
matrix2 = tf.constant([[2],[2]])

# 乘法操作
product = tf.matmul(matrix1,matrix2)

# 方式1
sess = tf.Session()
result = sess.run(product)
print(result)
sess.close()

# 方式2
# with tf.Session() as sess:
#     result = sess.run(product)
#     print(result)


# =============================================================================
# 第三个例子：
# =============================================================================

import tensorflow as tf

# 定义一个变量，初始化是0
state = tf.Variable(0,name='content')

# 定义一个常量
one = tf.constant(1)

# 定义加法步骤
new_value = tf.add(state,one)

# 将state 更新成 new_value
update = tf.assign(state,new_value)

#  初始化所定义的变量
init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    for step in range(3):
        sess.run(update)
        print(sess.run(state))


# =============================================================================
# 第四个例子：
# =============================================================================
        
import tensorflow as tf

#在 Tensorflow 中需要定义 placeholder 的 type ，一般为 float32 形式
input1 = tf.placeholder(tf.float32)
input2 = tf.placeholder(tf.float32)

# mul = multiply 是将input1和input2 做乘法运算，并输出为 output
ouput = tf.multiply(input1,input2)

with tf.Session() as sess:
    print(sess.run(ouput,feed_dict={input1:[7.],input2:[2.]}))
    

# =============================================================================
# 第五个例子
# =============================================================================

import tensorflow as tf

#在 Tensorflow 中需要定义 placeholder 的 type ，一般为 float32 形式
input1 = tf.placeholder(tf.float32)
input2 = tf.placeholder(tf.float32)

# mul = multiply 是将input1和input2 做乘法运算，并输出为 output
ouput = tf.multiply(input1,input2)

with tf.Session() as sess:
    print(sess.run(ouput,feed_dict={input1:[7.],input2:[2.]}))
