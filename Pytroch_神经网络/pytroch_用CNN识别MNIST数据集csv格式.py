# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-09-10 22:28:02
# @Last Modified by:   Administrator
# @Last Modified time: 2019-09-11 00:18:52
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import os
import numpy as np
import pandas as pd

# 本例使用的是转成CSV格式的MNIST数据集，表格的第一列是lable，后面的img向量
# 注意：torch.nn只支持mini-batch的数据形式，而不支持单个的数据
# 例如，nn.conv2d接受四维的参数nSamples*nChannels*Height*Width.
# 如果你的input只有一个样本，用input.unsqueeze(0)加一个伪batch维度

data_path = 'd:/_python/神经网络数据集/mnist'
os.chdir(data_path)

# CNN （卷积神经网络）
# 定义CNN网络
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        # nn.Dropout2d()防止过拟合，随机选择一个信道，将其置为零
        self.conv2_drop = nn.Dropout2d()
        self.layer1 = nn.Sequential(
            nn.Linear(320, 100),
            nn.BatchNorm1d(100),
            nn.ReLU(True))
        self.layer2 = nn.Sequential(
            nn.Linear(100, 10))

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = self.layer1(x)
        # F.dropout()防止过拟合，随机选择一个元素将其置为零
        x = F.dropout(x, training=self.training)
        x = self.layer2(x)
        # log_softmax(x, dim=1)对第二个维度即每一列做softmax
        return F.log_softmax(x, dim=1)

trainData = pd.read_csv("mnist_train.csv").values
train_data = trainData[0:50000, 1:]
train_label = trainData[0:50000, 0]  # 50000 代表样本数

testData = pd.read_csv("mnist_test.csv").values
test_data = testData[0:10000, 1:]
test_label = testData[0:10000, 0]     # 10000 代表标签数


# 训练

lr = 0.01
momentum = 0.5
seed = 1
log_interval = 32

cnn = CNN()
cnn.train()
optimizer = optim.SGD(cnn.parameters(), lr=lr,
                          momentum=momentum)

print("Training...")
start = time.time()

transform = transforms.Normalize((0.1307,), (0.3081,))

for i in range(len(train_data)):
    img = torch.Tensor(train_data[i])
    img = img.view(-1,28,28)
    img = transform(img)
    img = img.unsqueeze(0)
    lable = torch.Tensor(train_label[i])
    optimizer.zero_grad()
    output = cnn(img)
    loss = F.nll_loss(output, lable)
    loss.backward()
    optimizer.step()
    if i % 1000 == 0:
        print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
            0, i, len(train_data),
            100. * i / len(train_data), loss.item()))

end = time.time()
t = end - start
print ('Train：%dmin%.3fsec' %  ((int)(t/60), t-60*(int)(t/60)))






