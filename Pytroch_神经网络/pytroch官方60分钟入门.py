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

