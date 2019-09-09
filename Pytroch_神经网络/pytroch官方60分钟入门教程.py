# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 21:26:10 2019

@author: Administrator
"""

from __future__ import print_function
import numpy as np
import torch

# =============================================================================
# Tensors：张量
# =============================================================================
# 构建一个5x3的矩阵，未初始化：
x = torch.empty(5, 3)
print(x)

# 构建一个随机的初始化过的矩阵：
x = torch.rand(5, 3)
print(x)

# 构建一个dtype为long且用0填充的矩阵
x = torch.zeros(5, 3, dtype=torch.long)
print(x)

# 构建一个直接从data里构建tensor：
x = torch.tensor([5.5, 3])
print(x)

# 从已有的tensor创建tensor。这些方法将重用输入tensor的内容，例如dtype，除非使用者提供新的值。
x = x.new_ones(5, 3, dtype=torch.double)  # new_*方法接受了大小（sizes）
print(x)

x = torch.randn_like(x, dtype=torch.float)  # 重写了dtype
print(x)                                     # 结构具有相同的size

# 打印得到它的size（大小）：
print(x.size())

# 加法：语法1
y = torch.rand(5, 3)
print(x + y)

# 加法：语法2
print(torch.add(x, y))

# 加法：提供一个输出向量作为参数
result = torch.empty(5, 3)
torch.add(x, y, out=result)
print(result)

# 加法：in-place
y.add_(x)

# 可以使用类似于标准的numpy索引的切片功能。
print(x[:, 1])

# 改变大小：如果你想resize/reshape张量，你可以使用torch.view:
x = torch.randn(4, 4)
y = x.view(16)
z = x.view(-1, 8)  # size=-1 表示该纬度的size从其他维度推断
print(x.size(), y.size(), z.size())

# 如果你有一个元素的张量，可以使用.item()获得python number的值。
x = torch.randn(1)
print(x)
print(x.item())

# 将np array变成Torch Tensor。
a = np.ones(5)
b = torch.from_numpy(a)
np.add(a, 1, out=a)
print(a)
print(b)

# =============================================================================
# AUTOGRAD:自动求导
# =============================================================================

# torch.Tensor是包的核心类。如果你设置了它的属性.requires_grad为True，它开始时会追踪所有作用在它之上的操作。当你完成你的计算时你可以通过调用.backward()并且自动地计算所有梯度。这个张量的梯度将会被累积到.grad这个属性里。
# 为了组织张量追踪历史，你可以调用.detach()来从计算历史中将它分离，并且防止了在未来计算中被追踪。
# 为了防止追踪历史（并且使用内存），你也可以将代码块包装到with torch.no_grad():。

# 创建一个张量并且设置requires_grad=True并追踪它的计算。
x = torch.ones(2, 2, requires_grad=True)
print(x)

# 进行一个张量计算：
y = x + 2
print(y)

# y作为一个操作的结果，它有一个grad_fn
print(y.grad_fn)

# 对y做更多的操作
z = y * y * 3
out = z.mean()

print(z, out)

# 改变已存在张量的requires_grad=True标示。如果没有给定输入默认的标示是False。
a = torch.randn(2, 2)
a = ((a * 3) / (a - 1))
print(a.requires_grad)
a.requires_grad_(True)
print(a.requires_grad)
b = (a * a).sum()
print(b.grad_fn)

# =============================================================================
# 梯度
# =============================================================================
# 现在开始反向传播。因为out包含一个单独的标量，out.backward()等价于out.backward(torch.tensor(1.))。

out.backward()

print(x.grad)


# =============================================================================
# 神经网络
# =============================================================================
#一个典型的神经网络训练过程包括以下几点：

#1.定义一个包含可训练参数的神经网络
#2.迭代整个输入
#3.通过神经网络处理输入
#4.计算损失(loss)
#5.反向传播梯度到神经网络的参数
#6.更新网络的参数，典型的用一个简单的更新方法：weight = weight - learning_rate *gradient

# 定义神经网络

import torch
import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        # 1 input image channel, 6 output channels, 5x5 square convolution
        # kernel
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.conv2 = nn.Conv2d(6, 16, 5)
        # an affine operation: y = Wx + b
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        # Max pooling over a (2, 2) window
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        # If the size is a square you can only specify a single number
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]  # all dimensions except the batch dimension
        num_features = 1
        for s in size:
            num_features *= s
        return num_features

net = Net()
print(net)

#你刚定义了一个前馈函数，然后反向传播函数被自动通过 autograd 定义了。你可以使用任何张量操作在前馈函数上。

#一个模型可训练的参数可以通过调用 net.parameters() 返回：
params = list(net.parameters())
print(len(params))
print(params[0].size())  # conv1's .weight

# 让我们尝试随机生成一个 32x32 的输入。注意：期望的输入维度是 32x32 。为了使用这个网络在 MNIST 数据及上，你需要把数据集中的图片维度修改为 32x32。
input = torch.randn(1, 1, 32, 32)
out = net(input)
print(out)

# 把所有参数梯度缓存器置零，用随机的梯度来反向传播
net.zero_grad()
out.backward(torch.randn(1, 10))

# 损失函数
# 一个损失函数需要一对输入：模型输出和目标，然后计算一个值来评估输出距离目标有多远。
# 有一些不同的损失函数在 nn 包中。一个简单的损失函数就是 nn.MSELoss ，这计算了均方误差
output = net(input)
target = torch.randn(10)  # a dummy target, for example
target = target.view(1, -1)  # make it the same shape as output
criterion = nn.MSELoss()

loss = criterion(output, target)
print(loss)

# 当我们调用 loss.backward()，整个图都会微分，而且所有的在图中的requires_grad=True 的张量将会让他们的 grad 张量累计梯度。
# 为了演示，我们将跟随以下步骤来反向传播。

print(loss.grad_fn)  # MSELoss
print(loss.grad_fn.next_functions[0][0])  # Linear
print(loss.grad_fn.next_functions[0][0].next_functions[0][0])  # ReLU

#反向传播
#为了实现反向传播损失，我们所有需要做的事情仅仅是使用 loss.backward()。你需要清空现存的梯度，要不然帝都将会和现存的梯度累计到一起。
#现在我们调用 loss.backward() ，然后看一下 con1 的偏置项在反向传播之前和之后的变化。

net.zero_grad()     # zeroes the gradient buffers of all parameters

print('conv1.bias.grad before backward')
print(net.conv1.bias.grad)

loss.backward()

print('conv1.bias.grad after backward')
print(net.conv1.bias.grad)

#更新神经网络参数：
#最简单的更新规则就是随机梯度下降。
#weight = weight - learning_rate * gradient
#我们可以使用 python 来实现这个规则：
learning_rate = 0.01
for f in net.parameters():
    f.data.sub_(f.grad.data * learning_rate)

# 尽管如此，如果你是用神经网络，你想使用不同的更新规则，类似于 SGD, Nesterov-SGD, Adam, RMSProp, 等。
# 我们建立了一个小包：torch.optim 实现了所有的方法。使用它非常的简单。
import torch.optim as optim

# create your optimizer
optimizer = optim.SGD(net.parameters(), lr=0.01)
# in your training loop:
optimizer.zero_grad()   # zero the gradient buffers
output = net(input)
loss = criterion(output, target)
loss.backward()
optimizer.step()    # Does the update

