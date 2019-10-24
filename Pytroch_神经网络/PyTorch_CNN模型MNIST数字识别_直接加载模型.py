# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-09-16 08:49:26
# @Last Modified by:   Administrator
# @Last Modified time: 2019-10-23 13:07:21
from __future__ import print_function
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
import numpy as np
import time
import os

data_path = 'd:/_python/神经网络数据集/mnist'
os.chdir(data_path)

# 这里涉及一个知识点，卷积层输出的计算：
# 经过nn.Conv2d()
# 输出信号的形式为(N,Cin,H,W)，N 表示batch size，C表示channel个数，H,W分别表示特征图的高和宽。
# Hout = (Hin + 2*padding -(kernel_size-1)-1)/stride + 1
# Wout = (Win + 2*padding -(kernel_size-1)-1)/stride + 1

# 经过nn.MaxPool2D()
# 输出信号的形式为(N,Cin,H,W)，N 表示batch size，C表示channel个数，H,W分别表示特征图的高和宽。
# Hout = (Hin + 2*padding -(kernel_size-1)-1)/stride + 1
# Wout = (Win + 2*padding -(kernel_size-1)-1)/stride + 1

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


img_transform = transforms.Compose([transforms.ToTensor(),
                                    transforms.Normalize(mean = [0.1307],std = [0.3081])])
dataset_train = datasets.MNIST(root = './',transform = img_transform,train = True,download = True)
dataset_test = datasets.MNIST(root = './',transform = img_transform,train = False,download = True)

train_loader = torch.utils.data.DataLoader(dataset = dataset_train,batch_size=64,shuffle = True)
test_loader = torch.utils.data.DataLoader(dataset = dataset_test,batch_size=6,shuffle = False)

# 自定义一个显示图片的函数
def imshow(img):
    # 对图片进行Normalize()的反运算
    img = img*0.3081 + 0.1307
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()

def test_model(model, banchs, data_load):
    model.eval()
    # 分类结果:
    classes = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    # get some random test images
    test_iter = iter(data_load)

    for i in range(banchs):
        # 取图片数据，因为trainloader设置了batch_size=4，所以没运行一次.next()方法就会取出4幅图
        images, labels = test_iter.next()
        outputs = model(images)
        # 显示图片
        imshow(torchvision.utils.make_grid(images, padding=2))
        # 预测
        # 第二个参数1是代表dim的意思，也就是取每一行的最大值，
        # "_"取到的是最大值，predicted取到的是最大值对应的index，因为我们不关心最大值所以用匿名变量"_"来取
        time.sleep(2)
        _, predicted = torch.max(outputs, 1)

        # print 标签
        print('Predicted: ', ' '.join('%s' % classes[predicted[j]]
                                      for j in range(6)))
        time.sleep(6)


# 重新加载网络模型
# 模型实例化
model = CNN()
# 加载模型参数
#model.load_state_dict(torch.load('./cnn模型备份/net_128_batches.ckpt'))
model.load_state_dict(torch.load('./cnn模型备份/net_3_epoch.ckpt'))
# 在测试模型前，你必须调用model.eval来关闭 BatchNormalization 和 Dropout
# 否则会导致不一致的测试结果.

# 随机抽取图片测试模型
test_model(model, 5, test_loader)

