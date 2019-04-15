# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 21:08:22 2018

@author: Administrator
"""

import tensorflow as tf

a = tf.constant(2)
b = tf.constant(3)

# 启动计算图
with tf.Session() as sess:
    print("a: %i" % sess.run(a), "b: %i" % sess.run(b))
    print("Addition with constants: %i" % sess.run(a+b))
    print("Multiplication with constants: %i" % sess.run(a*b))
    
# 占位符，相当于先挖好两个坑用来存放神经网络的输入和输出
a = tf.placeholder(tf.int16)
b = tf.placeholder(tf.int16)

# 自定义一些运算
add = tf.add(a, b)
mul = tf.multiply(a, b)

# 启动计算图
with tf.Session() as sess:
    # 针对不同的运算输入不同的变量
    # feed_dict的作用：就是通过定义好的占位符传入变量或常量
    print("Addition with variables: %i" % sess.run(add, feed_dict={a: 2, b: 3}))
    print("Multiplication with variables: %i" % sess.run(mul, feed_dict={a: 2, b: 3}))


# 矩阵运算
matrix1 = tf.constant([[3., 3.]])
matrix2 = tf.constant([[2.],[2.]])

product = tf.matmul(matrix1, matrix2)  # 两个矩阵相乘

with tf.Session() as sess:
    result = sess.run(product)
    print(result)



