# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-09-16 08:16:28
# @Last Modified by:   Administrator
# @Last Modified time: 2019-09-16 09:10:48
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
import numpy as np
import os
import time

root_path = 'D:/_python/神经网络数据集/cifar-10'
os.chdir(root_path)

# 原来的tensor是三个维度的，值在0到1之间，那么经过transforms.Normalize之后就到了-1到1区间
# x = (x-mean)/std 也就是（（0,1）-0.5）/0.5=(-1,1)
transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

trainset = datasets.CIFAR10(root='./', train=True,
                                        download=False, transform=transform)
train_loader = torch.utils.data.DataLoader(trainset, batch_size=4,
                                          shuffle=True, num_workers=0)

testset = datasets.CIFAR10(root='./', train=False,
                                       download=False, transform=transform)
test_loader = torch.utils.data.DataLoader(testset, batch_size=4,
                                         shuffle=False, num_workers=0)
# 预测结果标签，一共10个类
classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

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

# functions to show an image
def imshow(img):
    # 因为读取数据的时候对img做了Normalize标准化，现在要反算回来
    # Normalize(x) = (x-mean)/std ,反算就是 x*std + mean
    # 因为0 < x < 1,所以std =1/2，mean = 1/2
    img = img / 2 + 0.5     # unnormalize
    # 将图片转成numpy包的图片
    npimg = img.numpy()
    # 交换颜色轴,H代表高，W代表宽，C代表颜色，因为
    # numpy包的图片是: H * W * C
    # torch包的图片是: C * H * W，所以需要通过转置调整颜色轴
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()

model = Net()
model.load_state_dict(torch.load('./cifar-10图片分类模型参数备份/net_4epochs.ckpt'))
# 在测试模型前，你必须调用model.eval来设置dropout和normalization层切换到评估模式，否则会导致不一致的测试结果.
model.eval()

# =============================================================================
# 用随机图片测试模型
# =============================================================================
def test_model(model, banchs, data_load):
    model.eval()
    # 分类结果:
    classes = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    # get some random test images
    test_iter = iter(data_load)

    classes = ('plane', 'car', 'bird', 'cat',
               'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

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

        # print 标签
        print('Predicted: ', ' '.join('%s' % classes[predicted[j]]
                                      for j in range(4)))
        time.sleep(2)


# 随机抽取图片测试模型
test_model(model, 5, test_loader)

