# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 17:10:59 2020

@author: Administrator
"""

import numpy as np
from keras.layers.embeddings import Embedding
from keras.models import Sequential

'''
输入数据是32*1，32个样本，1个类别特征，且类别特征的可能值是0到9之间（10个）。
对1个特征做one-hot的话，应该为32*10，
embedding就是使1个特征原本应该one-hot的10维变为3维（可以手动设定，也可以是其它）
这样输出的结果就应该是32*3
'''

# 搭建模型
model = Sequential()
model.add(Embedding(10, 3, input_length=1))
model.compile('rmsprop', 'mse')

# 构造输入数据
input_array = np.random.randint(10, size=(32,))
output_array = model.predict(input_array)
output_array.shape
# 输出的shape是 (32, 1, 3)
output_array = output_array.reshape(32,3)
