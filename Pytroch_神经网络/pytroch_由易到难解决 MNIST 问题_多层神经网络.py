# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-09-10 19:03:43
# @Last Modified by:   Administrator
# @Last Modified time: 2019-09-11 11:19:02

# Multilayer Neural Network （多层神经网络）

from __future__ import print_function
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable
from torchvision import datasets, transforms


# Multilayer Neural Network （多层神经网络）
# 这里我们就创建三层神经网络，让前一层的输出作为后一层的输入。
# 添加批标准化 BatchNorm1d() 与激活函数 ReLU() ，来增加网络的收敛速度和非线性.
# 要注意的是，最后一个输出层不需要添加函数。
class net(nn.Module):
    def __init__(self):
        super(net, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Linear(28 * 28, 300),
            nn.BatchNorm1d(300),
            nn.ReLU(True))
        self.layer2 = nn.Sequential(
            nn.Linear(300, 100),
            nn.BatchNorm1d(100),
            nn.ReLU(True))
        self.layer3 = nn.Sequential(
            nn.Linear(100, 10))

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        return x

def train(model, device, train_loader, optimizer, epoch):
    model.train() #启用 BatchNormalization 和 Dropout
    criterion = nn.CrossEntropyLoss()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        data = Variable(data.view(-1, 28 * 28))
        target = Variable(target)
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % log_interval == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item()))

def test(model, device, test_loader):
    criterion = nn.CrossEntropyLoss()
    model.eval() #不启用 BatchNormalization 和 Dropout
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            data = Variable(data.view(-1, 28 * 28))
            target = Variable(target)
            output = model(data)
            # get the index of the max log-probability
            pred = output.max(1, keepdim=True)[1]
            correct += pred.eq(target.view_as(pred)).sum().item()

    print('\nTest set:  Accuracy: {}/{} ({:.0f}%)\n'.format(
        correct,
        len(test_loader.dataset),
        100. * correct / len(test_loader.dataset))
    )

if __name__ == '__main__':
    batch_size = 64
    test_batch_size = 4
    epochs = 2
    lr = 0.01
    momentum = 0.5
    seed = 1
    log_interval = 32

    use_cuda = torch.cuda.is_available()

    torch.manual_seed(seed)

    device = torch.device("cuda" if use_cuda else "cpu")

    kwargs = {'num_workers': 1, 'pin_memory': True} if use_cuda else {}
    train_loader = torch.utils.data.DataLoader(
        datasets.MNIST('./', train=True, download=False,
                       transform=transforms.Compose([
                           transforms.ToTensor(),
                           transforms.Normalize((0.1307,), (0.3081,))
                       ])),
        batch_size=batch_size, shuffle=True, **kwargs)

    test_loader = torch.utils.data.DataLoader(
        datasets.MNIST('.', train=False, transform=transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])),
        batch_size=test_batch_size, shuffle=True, **kwargs)

    model = net().to(device)
    optimizer = optim.SGD(model.parameters(), lr=lr,
                          momentum=momentum)

    for epoch in range(1, epochs + 1):
        train(model, device, train_loader, optimizer, epoch)
        #test(model, device, test_loader)


    # =============================================================================
    # 随机选取test集中的图片测试模型
    # =============================================================================
    import torchvision
    import matplotlib.pyplot as plt
    import numpy as np
    import time

    # functions to show an image
    def imshow(img):
        img = img*0.3081 + 0.1307
        npimg = img.numpy()
        plt.imshow(np.transpose(npimg, (1, 2, 0)))
        plt.show()

    # 分类结果:
    classes = (0,1,2,3,4,5,6,7,8,9)
    # get some random test images
    test_dataiter = iter(test_loader)
    for i in range(10):
        # 取图片数据，因为trainloader设置了batch_size=4，所以没运行一次.next()方法就会取出4幅图
        images, labels = test_dataiter.next()
        data = Variable(images.view(-1, 28 * 28))
        outputs = model(data)
        # 显示图片
        imshow(torchvision.utils.make_grid(images,padding = 2))

        # 预测
        # 第二个参数1是代表dim的意思，也就是取每一行的最大值，
        # "_"取到的是最大值，predicted取到的是最大值对应的index，因为我们不关心最大值所以用匿名变量"_"来取
        _, predicted = torch.max(outputs, 1)

        # print 标签
        print('Predicted: ', ' '.join('%s' % classes[predicted[j]]
            for j in range(4)))
        time.sleep(3)
