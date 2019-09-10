# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-09-10 19:19:39
# @Last Modified by:   Administrator
# @Last Modified time: 2019-09-10 20:08:50
from __future__ import print_function
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import os
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


def train(model, device, train_loader, optimizer, epoch):
    model.train() #启用 BatchNormalization 和 Dropout
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % log_interval == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item()))


def test(model, device, test_loader):
    model.eval() # 不启用 BatchNormalization 和 Dropout
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
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
    epochs = 3
    lr = 0.01
    momentum = 0.5
    seed = 1
    log_interval = 32

    use_cuda = torch.cuda.is_available()

    torch.manual_seed(seed)

    device = torch.device("cuda" if use_cuda else "cpu")

    kwargs = {'num_workers': 1, 'pin_memory': True} if use_cuda else {}
    train_loader = torch.utils.data.DataLoader(
        datasets.MNIST('./', train=True, download=True,
                       transform=transforms.Compose([
                           transforms.ToTensor(),
                           transforms.Normalize((0.1307,), (0.3081,))
                       ])),
        batch_size=batch_size, shuffle=True, **kwargs)
    test_loader = torch.utils.data.DataLoader(
        datasets.MNIST('./', train=False, transform=transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])),
        batch_size=test_batch_size, shuffle=True, **kwargs)

    model = CNN().to(device)
    optimizer = optim.SGD(model.parameters(), lr=lr,
                          momentum=momentum)

    for epoch in range(1, epochs + 1):
        train(model, device, train_loader, optimizer, epoch)
        test(model, device, test_loader)

    # =============================================================================
    # 随机选取test集中的图片测试模型
    # =============================================================================
    import torchvision
    import matplotlib.pyplot as plt
    import numpy as np
    import time

    # functions to show an image
    def imshow(img):
        img = img / 2 + 0.5     # unnormalize
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
        outputs = model(images)
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