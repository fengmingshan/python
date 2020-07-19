# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 15:47:01 2020

@author: Administrator
"""

# coding: UTF-8
import sys
import os
# 将自定义包的路径添加在系统路径中
sys.path.append(r'D:\_python\python\NLP\Chinese-Text-Classification-Pytorch')
import time
import torch
import numpy as np
from train_eval import train, init_network
from importlib import import_module
from utils import build_dataset, build_iterator, get_time_dif

path = r'D:\_python\python\NLP\Chinese-Text-Classification-Pytorch'
os.chdir(path)

dataset = 'THUCNews'  # 数据集

# 搜狗新闻:embedding_SougouNews.npz, 腾讯:embedding_Tencent.npz, 随机初始化:random
embedding = 'embedding_SougouNews.npz' # embedding_Tencent.npz, embedding_SougouNews.npz , random
model_name = 'TextCNN'


x = import_module('models.' + model_name)
config = x.Config(dataset, embedding)
config.vocab_path
config
config
np.random.seed(1)
torch.manual_seed(1)
torch.cuda.manual_seed_all(1)
torch.backends.cudnn.deterministic = True  # 保证每次结果一样

start_time = time.time()
print("Loading data...")
vocab, train_data, dev_data, test_data = build_dataset(config, 'True')
train_iter = build_iterator(train_data, config)
dev_iter = build_iterator(dev_data, config)
test_iter = build_iterator(test_data, config)
time_dif = get_time_dif(start_time)
print("Time usage:", time_dif)

# train
config.n_vocab = len(vocab)
model = x.Model(config).to(config.device)
if model_name != 'Transformer':
    init_network(model)
print(model.parameters)
train(config, model, train_iter, dev_iter, test_iter)
