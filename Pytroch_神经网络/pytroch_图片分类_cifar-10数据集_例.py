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



# =============================================================================
# 定义一个卷积神经网络 ，并设置它为3通道的图片
# =============================================================================
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

net = Net()

# =============================================================================
# 定义一个损失函数和优化器 让我们使用分类交叉熵Cross-Entropy 作损失函数，动量SGD做优化器。
# =============================================================================
import torch.optim as optim

criterion = nn.CrossEntropyLoss()
# 知识点 冲量：momentum
# 当使用冲量时，则把每次x的更新量v考虑为本次的梯度下降量- dx * lr与上次x的更新量v乘上一个介于[0, 1]的因子momentum的和，
# 即：v = - dx * lr + v * momemtum。
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

for epoch in range(2):  # loop over the dataset multiple times
    running_loss = 0.0
    # enumerate(trainloader,0)，表示从头开始迭代，因为刚才运行过.next()方法，起始位置已经改变了
    for i, data in enumerate(trainloader,0):
        # get the inputs
        inputs, labels = data
        # zero the parameter gradients
        optimizer.zero_grad()
        # forward + backward + optimize
        outputs = net(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
        if i % 2000 == 1999:    # print every 2000 mini-batches
            print('[%d, %5d] loss: %.3f' %
                  (epoch + 1, i + 1, running_loss / 2000))
            running_loss = 0.0
print('Finished Training')

# =============================================================================
# 用随机图片测试模型
# =============================================================================
# get some random test images
test_dataiter = iter(testloader)
# 取图片数据，因为trainloader设置了batch_size=4，所以没运行一次.next()方法就会取出4幅图
images, labels = test_dataiter.next()
# 显示图片
imshow(torchvision.utils.make_grid(images,padding = 2))

# 预测
outputs = net(images)
# 第二个参数1是代表dim的意思，也就是取每一行的最大值，
# "_"取到的是最大值，predicted取到的是最大值对应的index，因为我们不关心最大值所以用匿名变量"_"来取
_, predicted = torch.max(outputs, 1)

# print 标签
print('Predicted: ', ' '.join('%s' % classes[predicted[j]]
    for j in range(4)))


# =============================================================================
# 用整个训练集测试模型
# =============================================================================
correct = 0
total = 0
# 因为是模型测试所以不用更新模型，所以用with torch.no_grad():关闭自动求导，减少了内存的使用，提高运算效率
with torch.no_grad():
    for data in testloader:
        images, labels = data
        outputs = net(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print('Accuracy of the network on the 10000 test images: %d %%' % (
    100 * correct / total))

# Save the model checkpoint
torch.save(net.state_dict(), 'model.ckpt')