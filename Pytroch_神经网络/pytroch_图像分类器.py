# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 11:53:28 2019

@author: Administrator
"""

# 本教程，使用CIFAR10数据集，它包含十个类别：‘airplane’, ‘automobile’, ‘bird’, ‘cat’, ‘deer’, ‘dog’, ‘frog’, ‘horse’, ‘ship’, ‘truck’。
# CIFAR-10 中的图像尺寸为33232，也就是RGB的3层颜色通道，每层通道内的尺寸为32*32。

# 我们将按次序的做如下几步：
# 1.使用torchvision加载并且归一化CIFAR10的训练和测试数据集
# 2.定义一个卷积神经网络
# 3.定义一个损失函数
# 4.在训练样本数据上训练网络
# 5.在测试样本数据上测试网络

# 使用 torchvision加载 CIFAR10
import torch
import torchvision
import torchvision.transforms as transforms

# torchvision 数据集的输出是范围在[0,1]之间的 PILImage，我们将他们转换成归一化范围为[-1,1]之间的张量 Tensors。
transform = transforms.Compose(
    [transforms.ToTensor(),transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

trainset = torchvision.datasets.CIFAR10(
    root='./data', train=True,download=True, transform=transform)

trainloader = torch.utils.data.DataLoader(
    trainset, batch_size=4,shuffle=True, num_workers=2)

testset = torchvision.datasets.CIFAR10(
    root='./data', train=False,download=True, transform=transform)

testloader = torch.utils.data.DataLoader(
    testset, batch_size=4,shuffle=False, num_workers=2)

classes = (
    'plane', 'car', 'bird', 'cat','deer', 'dog', 'frog', 'horse', 'ship', 'truck')
