# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 19:42:07 2019

@author: Administrator
"""

import torch
import torchvision
import torchvision.transforms as transforms


root_path = 'D:/_python/神经网络数据集/cifar-10'
os.chdir(root_path)

transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

trainset = torchvision.datasets.CIFAR10(root='./', train=True,
                                        download=False, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=4,
                                          shuffle=True, num_workers=2)

testset = torchvision.datasets.CIFAR10(root='./', train=False,
                                       download=False, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=4,
                                         shuffle=False, num_workers=2)

classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

import matplotlib.pyplot as plt
import numpy as np

# functions to show an image
def imshow(img):
    img = img / 2 + 0.5     # unnormalize
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()

# get some random training images
dataiter = iter(trainloader)
# 取图片数据，因为trainloader设置了batch_size=4，所以没运行一次.next()方法就会取出4幅图
images, labels = dataiter.next()
# 显示图片
# torchvision.utils.make_grid的作用是将多幅图拼接成一幅图,padding是每幅图中间的宽度
# 因为一次读入了4幅图片，所以images的shape是[4, 3, 32, 32]
imshow(torchvision.utils.make_grid(images,padding = 2))
# print 标签
# labels[j]返回的是一个类别的数值i，classes[i]就对应类别的名称。
print(' '.join('%s' % classes[labels[j]] for j in range(4)))



import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
# =============================================================================
# 输出的尺寸最终如何计算？在PyTorch中，可以用一个公式来计算，就是floor((W-F+2P)/ S + 1)。
# 其中，floor 表示下取整操作，W表示输入数据的大小，F表示卷积层中卷积核的尺寸，S表示步长，P表示边界填充0的数量
# =============================================================================
net = Net()

