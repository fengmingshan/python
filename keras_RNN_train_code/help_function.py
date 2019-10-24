# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 17:02:58 2018

@author: alpha
"""
import numpy as np
import tensorflow as tf
import cm_plot
next_batch = 100



def optimize(num_iterations,tf_class,input_dict_train,batch_size = next_batch):
    '''
    优化器
    输入：
    num_iterations，迭代次数；
    tf_dict，tf模型字典；
    input_dict_train，训练用的数据；
    batch_size，batch（每次读取next_batch条用于优化参数，以数据防止内存溢出）；
    '''
    x_tf = tf_class.x_tf
    y_tf = tf_class.y_tf
    sess = tf_class.sess
    optimizer = tf_class.optimizer
    cost = tf_class.cost
    x = input_dict_train[x_tf]
    y = input_dict_train[y_tf]
    n = len(x)
    m = n//batch_size+1
    for i in range(num_iterations):
        for j in range(m):
           
            feed_d = {x_tf:x[j*batch_size:min((j+1)*batch_size,n)],\
                      y_tf:y[j*batch_size:min((j+1)*batch_size,n)]}
            sess.run(optimizer, feed_dict=feed_d)
        print (('\ncost:%s')%(sess.run(cost,feed_dict=feed_d)))




def print_accuracy(tf_class,input_dict,batch_size=next_batch):
    '''
    获取预测值与正确率
    
    输入：
    tf_dict，tf模型字典；
    input_dict_train，训练用的数据；
    batch_size，batch（每次读取next_batch条用于优化参数，以数据防止内存溢出）；

    输出：
    np.array(result)，np格式的预测值；
    acc，正确率
    '''
    x_tf = tf_class.x_tf
    y_tf = tf_class.y_tf
    sess = tf_class.sess
    y_pred_cls = tf_class.y_pred_cls
    correct_prediction = tf_class.correct_prediction
    x = input_dict[x_tf]
    y = input_dict[y_tf]
    correct = []
    result = []
    n = len(x)
    m = n//batch_size+1
    for j in range(m):
           
        feed_d = {x_tf:x[j*batch_size:min((j+1)*batch_size,n)],\
                      y_tf:y[j*batch_size:min((j+1)*batch_size,n)]}
        result += list(sess.run(y_pred_cls, feed_dict=feed_d))  
        correct += list(sess.run(correct_prediction, feed_dict=feed_d))
 
    acc = sum(correct)/n
 
    return np.array(result),acc



def save_model(savepath,tf_class):
    '''
    保存模型

    输入：
    savepath，存储的文件夹路径；
    tf_dict，tf模型字典；    
    '''
    saver = tf.train.Saver()
    sess = tf_class.sess
    saver.save(sess=sess, save_path=savepath)
    
    
def data_fenpian(data_dict,num_bat=7):
    '''
    将数据分成num_bat份，用于k重交叉验证，其中一份作为测试集，其余6份为
    
    输入:
    data_dict,另一个模块预处理过的数据字典
    num_bat，切分的份数    
    '''
    x = data_dict['x']
    y = data_dict['y']
    data = data_dict['data']
    num_x = len(x)
    k_num = int(num_x/num_bat) + 1
    #print(k_num)
    xy_dict = {}
    for i in range(num_bat):
        xy_dict[i] = [np.array(x[i*k_num:min((i+1)*k_num,num_x)]),\
                      np.array(y[i*k_num:min((i+1)*k_num,num_x)]),\
                      data[i*k_num:min((i+1)*k_num,num_x)]]
    

    print('数据分片完成')    
    return xy_dict

def run(tf_class,xy_dict,i,num_iterations,initializer = False,num_bat=7):
    
    x_tf = tf_class.x_tf
    y_tf = tf_class.y_tf
    sess = tf_class.sess
    accuracy = tf_class.accuracy
    y_pred_cls = tf_class.y_pred_cls
    if initializer:
        sess.run(tf.global_variables_initializer())
        print('初始化所有参数')
    
    x_train_input = np.concatenate([xy_dict[j][0] for j in range(num_bat) if not(j==i)],axis=0)
    y_train_input = np.concatenate([xy_dict[j][1] for j in range(num_bat) if not(j==i)],axis=0)
    x_test_input = xy_dict[i][0]
    y_test_input = xy_dict[i][1]
    input_dict_train = {x_tf:x_train_input,\
                        y_tf:y_train_input}
    input_dict_test = {x_tf:x_test_input,\
                       y_tf:y_test_input}

    for j in range(num_iterations):
        optimize(num_iterations=1,tf_class=tf_class,input_dict_train=input_dict_train,batch_size = next_batch)

        if j//5==0:
            acc_test = sess.run(accuracy,feed_dict=input_dict_test)
            print(('train accruacy:%s')%(acc_test))
            print('\n')

    
    yp_train,acc_train=print_accuracy(tf_class=tf_class,input_dict = input_dict_train)
    cm_plot.cm_plot(yp_train,y_train_input).show()
    print(('train accruacy:%s')%(acc_train))

    
    yp_test = sess.run(y_pred_cls,feed_dict=input_dict_test)
    cm_plot.cm_plot(yp_test,y_test_input).show()
    acc_test = sess.run(accuracy,feed_dict=input_dict_test)
    print(('test accruacy:%s')%(acc_test))
