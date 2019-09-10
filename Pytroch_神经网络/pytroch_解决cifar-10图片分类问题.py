# @Author: Administrator
# @Date:   2019-09-09 13:40:28
# @Last Modified by:   Administrator
# @Last Modified time: 2019-09-10 22:20:48

# -*- coding: utf-8 -*-

# 先将cifar-10数据集转成train和test

import pickle as p
import numpy as np
import os
import torch
import torchvision
import torchvision.transforms as transforms

root_path = 'd:/_python/神经网络数据集/CIFAR-10'
os.chdir(root_path)

# 原来的tensor是三个维度的，值在0到1之间，那么经过transforms.Normalize之后就到了-1到1区间
# x = (x-mean)/std 也就是（（0,1）-0.5）/0.5=(-1,1)
transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])


# 在构建数据集的时候指定transform，就会应用我们定义好的transform
# root是存储数据的文件夹，download=True指定如果数据不存在先下载数据
cifar_train = torchvision.datasets.CIFAR10(root='./', train=True,
                                           download=False, transform=transform)
cifar_test = torchvision.datasets.CIFAR10(root='./', train=False,
                                          download=False,transform=transform)

# 读取 trian 和 test 数据
trainloader = torch.utils.data.DataLoader(cifar_train, batch_size=32, shuffle=True)
testloader = torch.utils.data.DataLoader(cifar_test, batch_size=32, shuffle=True)


import torch
import torch.nn as nn
import torch.nn.functional as F
# 定义神经网络
class LeNet(nn.Module):
    # 一般在__init__中定义网络需要的操作算子，比如卷积、全连接算子等等
    def __init__(self):
        # 这个语句是找到LeNet的父类即nn.Module，然后执行nn.Module的init方法
        # 相当于对实例LeNet执行nn.Module进行初始化方法
        super(LeNet, self).__init__()
        # Conv2d的第一个参数是输入的channel数量，第二个是输出的channel数量，第三个是kernel size
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.conv2 = nn.Conv2d(6, 16, 5)
        # 由于上一层有16个channel输出，每个feature map大小为5*5，所以全连接层的输入是16*5*5
        self.fc1 = nn.Linear(16*5*5, 120)
        self.fc2 = nn.Linear(120, 84)
        # 最终有10类，所以最后一个全连接层输出数量是10
        self.fc3 = nn.Linear(84, 10)
        self.pool = nn.MaxPool2d(2, 2)
    # forward这个函数定义了前向传播的运算，只需要像写普通的python算数运算那样就可以了
    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.pool(x)
        x = F.relu(self.conv2(x))
        x = self.pool(x)
        # 下面这步把二维特征图变为一维，这样全连接层才能处理
        x = x.view(-1, 16*5*5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# 实例化神经网络
net = LeNet()
# 定义损失函数和优化器
# optim中定义了各种各样的优化方法，包括SGD
import torch.optim as optim

# CrossEntropyLoss就是我们需要的损失函数，optimizer就是优化器
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

print("Start Training...")
for epoch in range(30):
    # 我们用一个变量来记录每100个batch的平均loss
    loss100 = 0.0
    # 我们的dataloader派上了用场
    for i, data in enumerate(trainloader):
        inputs, labels = data
        # 首先要把梯度清零，不然PyTorch每次计算梯度会累加，不清零的话第二次算的梯度等于第一次加第二次的
        optimizer.zero_grad()
        # 计算前向传播的输出
        outputs = net(inputs)
        # 根据输出计算loss
        loss = criterion(outputs, labels)
        # 算完loss之后进行反向梯度传播，这个过程之后梯度会记录在变量中
        loss.backward()
        # 用计算的梯度对模型去做优化
        optimizer.step()
        loss100 += loss.item()
        if i % 100 == 99:
            print('[Epoch %d, Batch %5d] loss: %.3f' %
                  (epoch + 1, i + 1, loss100 / 100))
            loss100 = 0.0

print("Done Training!")


# ok，训练完了之后我们来检测一下准确率，我们用训练好的模型来预测test数据集
# 构造测试的dataloader
dataiter = iter(testloader)
# 预测正确的数量和总数量
correct = 0
total = 0
# 使用torch.no_grad的话在前向传播中不记录梯度，节省内存
with torch.no_grad():
    for data in testloader:
        images, labels = data
        images, labels = images.to(device), labels.to(device)
        # 预测
        outputs = net(images)
        # 我们的网络输出的实际上是个概率分布，去最大概率的哪一项作为预测分类
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print('Accuracy of the network on the 10000 test images: %d %%' % (
    100 * correct / total))