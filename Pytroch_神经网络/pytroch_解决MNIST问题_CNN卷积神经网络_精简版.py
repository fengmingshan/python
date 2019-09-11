# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-09-11 23:16:46
# @Last Modified by:   Administrator
# @Last Modified time: 2019-09-12 00:11:26

from __future__ import print_function
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import os
import torchvision
import matplotlib.pyplot as plt
import numpy as np
import time
from torchvision import datasets, transforms

data_path = 'd:/_python/神经网络数据集/mnist'
os.chdir(data_path)

# CNN （卷积神经网络）


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

# 读取训练集和测试集数据
batch_size = 64
test_batch_size = 4

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

train_loader = torch.utils.data.DataLoader(
    datasets.MNIST('./', train=True, download=True,transform=transform),
    batch_size=batch_size, shuffle=True)

test_loader = torch.utils.data.DataLoader(
    datasets.MNIST('./', train=False, transform=transform),
    batch_size=test_batch_size, shuffle=True)

# 查看训练集图片
# 自定义一个显示图片的函数
def imshow(img):
    # 对图片进行Normalize()的反运算
    img = img*0.3081 + 0.1307
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()

# 取图片数据，因为trainloader设置了batch_size=64，所以没运行一次.next()方法就会取出4幅图
train_iter = iter(train_loader)
images, labels = train_iter.next()
imshow(torchvision.utils.make_grid(images, padding=2))


# 训练模型
print("Training...")
start = time.time()

epochs = 3
lr = 0.01
momentum = 0.5
log_interval = 32

model = CNN()
optimizer = optim.SGD(model.parameters(), lr=lr,
                      momentum=momentum)
model.train()

def test(model, test_loader):
    model.eval() # 不启用 BatchNormalization 和 Dropout
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for images, lables in test_loader:
            output = model(images)
            # get the index of the max log-probability
            pred = output.max(1, keepdim=True)[1]
            # view_as等同于reshape，确保两个要比较的tensor形状和维度都一样
            correct += pred.eq(lables.view_as(pred)).sum().item()
    # 打印测试的样本数和正确率
    print('\nTest set:  Accuracy: {}/{} ({:.0f}%)\n'.format(
            correct,
            len(test_loader.dataset),
            100. * correct / len(test_loader.dataset))
        )
# 使用for循环训练模型
for i in range(epochs + 1):
    for batch_idx, (images, lables) in enumerate(train_loader):
        optimizer.zero_grad()
        output = model(images)
        # 定义损失函数
        loss = F.nll_loss(output, lables)
        loss.backward()
        optimizer.step()
        if batch_idx % log_interval == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                i, batch_idx * len(images), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item()))
    test(model,test_loader)

end = time.time()
t = end - start
print('Train：%d min %.2f sec' % (int(t/60), int(t-60*int(t/60))))


# =============================================================================
# 随机选取test集中的图片测试模型
# =============================================================================

# 定义一个随机选图片测试模型的函数:
# 该函数接收3个参数model,banchs,data_load
# model：要测试的模型，banchs：测试批次，data_load：数据集

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
        _, predicted = torch.max(outputs, 1)

        # print 预测标签
        print('Predicted: ', ' '.join('%s' % classes[predicted[j]]
                                      for j in range(4)))
        time.sleep(2)

# 随机抽取图片测试模型
test_model(model, 10, test_loader)