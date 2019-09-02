# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 22:31:16 2019

@author: Administrator
"""
import torch

# =============================================================================
# 基本概念PyTorch 张量
# =============================================================================

torch.Tensor(5, 3)
type(torch.Tensor)

# 服从-1 - +1均匀分布的张量
torch.Tensor(5, 3).uniform_(-1, 1)

# 从list创建张量，FloatTensor 表示32bit的float
x = torch.FloatTensor([[1, 2, 3], [4, 5, 6]])

x[1][2]

print(x)
# Tensor支持直接数学运算
x = torch.Tensor(5, 3).uniform_(-1, 1)
y = x * torch.randn(5, 3)
print(y)

# Tensor支持直接数学运算
x = torch.Tensor([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15]])
print(x.size())

'''
PyTorch 会从最后开始往前逐个比较它们的维度大小。
在这个过程中，如果两者的对应维度相同，或者其一（或者全是）等于 1，则继续进行比较，直到最前面的维度。
若不满足这两个条件，程序就会报错。
'''

y = x + torch.randn(5, 1)
print(y)

z2 = x + torch.randn(1, 3)  # 一个维度相等,一个维度等于1，可以加
print(z1)

z1 = x + torch.randn(1, 1)  # 所有维度全1可以加，
print(z2)

z3 = x + torch.randn(4, 2)  # 两个维度都不同，报错

z4 = x + torch.randn(4, 1)  # 两个维度都不同，报错


# CPU张量 与 GPU张量
x = torch.FloatTensor(5, 3).uniform_(-1, 1)

y = torch.FloatTensor(3, 5).uniform_(-1, 1)

torch.matmul(x, y)

print(torch.cuda.is_available())  # 返回False，本机显卡不支持GPU张量

# 二维张量转置
matrix = torch.randn(3, 3)
matrix

matrix.t()


# =============================================================================
#  AutoGrad 模块 自动反向梯度，我们只用定义模型的前向传播，反向传播 PyTorch可以自动完成
# =============================================================================
'''
PyTorch 使用的技术为自动微分（automatic differentiation）。
在这种机制下，系统会有一个 Recorder 来记录我们执行的运算，然后再反向计算对应的梯度。
这种技术在构建神经网络的过程中十分强大，因为我们可以通过计算前向传播过程中参数的微分来节省时间。
'''
# 通过 backward() 和 torch.autograd.grad 计算梯度的方法
from torch.autograd import Variable

x = Variable(torch.Tensor(5, 3).uniform_(-1, 1), requires_grad=True)

y = Variable(torch.Tensor(5, 3).uniform_(-1, 1), requires_grad=True)

z = x ** 2 + 3 * y

# 通过backward（）计算梯度
z.backward(gradient=torch.ones(5, 3))

# torch.eq 判断两个值是否相等
torch.eq(x.grad, 2 * x)

# 通过 torch.autograd.grad 计算梯度
x = Variable(torch.Tensor(5, 3).uniform_(-1, 1), requires_grad=True)

y = Variable(torch.Tensor(5, 3).uniform_(-1, 1), requires_grad=True)

z = x ** 2 + 3 * y

dz_dx = torch.autograd.grad(z, x, grad_outputs=torch.ones(5, 3))

dz_dy = torch.autograd.grad(z, y, grad_outputs=torch.ones(5, 3))

# 最优化模块 torch.optim
# torch.optim 是实现神经网络中多种优化算法的模块，它目前已经支持大多数一般的方法，
# 所以我们不需要从头构建优化算法。只需要一行代码就可以使用

optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# 神经网络模块
'''
线性层- nn.Linear、nn.Bilinear
卷积层 - nn.Conv1d、nn.Conv2d、nn.Conv3d、nn.ConvTranspose2d
非线性激活函数- nn.Sigmoid、nn.Tanh、nn.ReLU、nn.LeakyReLU
池化层 - nn.MaxPool1d、nn.AveragePool2d
循环网络 - nn.LSTM、nn.GRU
归一化 - nn.BatchNorm2d
Dropout - nn.Dropout、nn.Dropout2d
嵌入 - nn.Embedding
损失函数 - nn.MSELoss、nn.CrossEntropyLoss、nn.NLLLoss

以上就是 PyTorch 的基本组件，我们可以使用它们快速构建神经网络。
'''
# define model 例子
model = torch.nn.Sequential(
    torch.nn.Linear(input_num_units, hidden_num_units),
    torch.nn.ReLU(),
    torch.nn.Linear(hidden_num_units, output_num_units),
)
loss_fn = torch.nn.CrossEntropyLoss()

# =============================================================================
#  构建神经网络（使用NumPy 和. 使用PyTorch对比）
# =============================================================================

# 使用numpy构建神经内网络
import numpy as np

# Input array
X = np.array([[1, 0, 1, 0], [1, 0, 1, 1], [0, 1, 0, 1]])

# Output
y = np.array([[1], [1], [0]])

# Sigmoid Function


def sigmoid(x):
    return 1/(1 + np.exp(-x))

# Derivative of Sigmoid Function


def derivatives_sigmoid(x):
    return x * (1 - x)


# Variable initialization
epoch = 5000  # Setting training iterations
lr = 0.1  # Setting learning rate
inputlayer_neurons = X.shape[1]  # number of features in data set
hiddenlayer_neurons = 3  # number of hidden layers neurons
output_neurons = 1  # number of neurons at output layer

# weight and bias initialization
wh = np.random.uniform(size=(inputlayer_neurons, hiddenlayer_neurons))
bh = np.random.uniform(size=(1, hiddenlayer_neurons))
wout = np.random.uniform(size=(hiddenlayer_neurons, output_neurons))
bout = np.random.uniform(size=(1, output_neurons))

for i in range(epoch):
    # Forward Propogation
    hidden_layer_input1 = np.dot(X, wh)
    hidden_layer_input = hidden_layer_input1 + bh
    hiddenlayer_activations = sigmoid(hidden_layer_input)
    output_layer_input1 = np.dot(hiddenlayer_activations, wout)
    output_layer_input = output_layer_input1 + bout
    output = sigmoid(output_layer_input)

    # Backpropagation
    E = y-output
    slope_output_layer = derivatives_sigmoid(output)
    slope_hidden_layer = derivatives_sigmoid(hiddenlayer_activations)
    d_output = E * slope_output_layer
    Error_at_hidden_layer = d_output.dot(wout.T)
    d_hiddenlayer = Error_at_hidden_layer * slope_hidden_layer
    wout += hiddenlayer_activations.T.dot(d_output) * lr
    bout += np.sum(d_output, axis=0, keepdims=True) * lr
    wh += X.T.dot(d_hiddenlayer) * lr
    bh += np.sum(d_hiddenlayer, axis=0, keepdims=True) * lr

print('actual :\n', y, '\n')
print('predicted :\n', output)


# =============================================================================
#  使用PyTorch构建神经内网络
# =============================================================================
import torch

# Input array
X = torch.Tensor([[1, 0, 1, 0], [1, 0, 1, 1], [0, 1, 0, 1]])
# Output
y = torch.Tensor([[1], [1], [0]])

# Sigmoid Function
def sigmoid(x):
    return 1/(1 + torch.exp(-x))

# Derivative of Sigmoid Function
def derivatives_sigmoid(x):
    return x * (1 - x)

# Variable initialization
epoch = 5000  # Setting training iterations
lr = 0.1  # Setting learning rate
inputlayer_neurons = X.shape[1]  # number of features in data set
hiddenlayer_neurons = 3  # number of hidden layers neurons
output_neurons = 1  # number of neurons at output layer

# weight and bias initialization
wh = torch.randn(inputlayer_neurons, hiddenlayer_neurons).type(torch.FloatTensor)
bh = torch.randn(1, hiddenlayer_neurons).type(torch.FloatTensor)
wout = torch.randn(hiddenlayer_neurons, output_neurons)
bout = torch.randn(1, output_neurons)

for i in range(epoch):
    # Forward Propogation
    hidden_layer_input1 = torch.mm(X, wh)
    hidden_layer_input = hidden_layer_input1 + bh
    hidden_layer_activations = sigmoid(hidden_layer_input)

    output_layer_input1 = torch.mm(hidden_layer_activations, wout)
    output_layer_input = output_layer_input1 + bout
    output = sigmoid(output_layer_input1)

    # Backpropagation
    E = y-output
    slope_output_layer = derivatives_sigmoid(output)
    slope_hidden_layer = derivatives_sigmoid(hidden_layer_activations)
    d_output = E * slope_output_layer
    Error_at_hidden_layer = torch.mm(d_output, wout.t())
    d_hiddenlayer = Error_at_hidden_layer * slope_hidden_layer
    wout += torch.mm(hidden_layer_activations.t(), d_output) * lr
    bout += d_output.sum() * lr
    wh += torch.mm(X.t(), d_hiddenlayer) * lr
    bh += d_output.sum() * lr

print('actual :\n', y, '\n')
print('predicted :\n', output)



# =============================================================================
# PyTorch 案例 线性回归
# =============================================================================

import torch
from torch.autograd import Variable

# 定义数据：
x_data = Variable(torch.Tensor([[1.0], [2.0], [3.0]]))
print(x_data)
y_data = Variable(torch.Tensor([[2.0], [4.0], [6.0]]))
print(y_data)

# 定义模型，在 PyTorch 中，我们可以使用高级 API 来定义相关的模型或层级。
# 如下定义了「torch.nn.Linear(1, 1)」，即一个输入变量和一个输出变量。
class Model(torch.nn.Module):
    def __init__(self):
        """
        In the constructor we instantiate two nn.Linear module
        """
        super(Model, self).__init__()
        self.linear = torch.nn.Linear(1, 1)  # One in and one out

    def forward(self, x):
        """
        In the forward function we accept a Variable of input data and we must return

        a Variable of output data. We can use Modules defined in the constructor as

        well as arbitrary operators on Variables.
        """
        y_pred = self.linear(x)
        return y_pred


# 构建损失函数和优化器，构建损失函数也可以直接使用「torch.nn.MSELoss(size_average=False)」调用均方根误差函数。
# 优化器可以使用「torch.optim.SGD()」提到用随机梯度下降，其中我们需要提供优化的目标和学习率等参数。
# nn.Linear modules which are members of the model.
model = Model()

criterion = torch.nn.MSELoss(size_average=False)
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# 训练模型，执行前向传播计算损失函数，并优化参数：

for epoch in range(500):
    # Forward pass: Compute predicted y by passing x to the model
    y_pred = model(x_data)

    # Compute and print loss
    loss = criterion(y_pred, y_data)
    print(epoch, loss.data.item())

    # Zero gradients, perform a backward pass, and update the weights.
    optimizer.zero_grad()
    # optimizer.zero_grad()与 model.zero_grad()作用是一样的，不管哪种写法可以
    # model.zero_grad()
    loss.backward()
    # 更新模型，只有执行了optimizer.step()模型才会更新
    optimizer.step()

# =============================================================================
#  用 PyTorch 解决图像识别问题
# =============================================================================
'''
为了进一步熟悉 PyTorch，我们将使用它解决 Analytics Vidhya 的深度学习实践问题：识别手写数字。
我们的问题是给定一张 28 x 28 的图像，利用模型识别其所代表的手写数字。
所以首先我们需要下载训练集与测试集，数据集包含了一个压缩文件以储存所有的图像。
其中 train.csv 和 test.csv 分别储存了训练和测试图像，且图像的格式为 png。
下面我们将一步步构建简单的神经网络以实现手写数字识别功能。
'''
# a）导入必要的函数库
# import modules
%pylab inline
import os
import numpy as np
import pandas as pd
from scipy.misc import imread
from sklearn.metrics import accuracy_score


# b）设置随机的 Seed，因此我们能控制模型产生的随机数基本不变（伪随机数）。
# To stop potential randomness
seed = 128
rng = np.random.RandomState(seed)


# c）设置工作目录的路径。
root_dir = 'D:/test/'
data_dir = os.path.join(root_dir, 'data')
# check for existence
if not os.path.exists(root_dir):
    os.mkdir(root_dir)
if not os.path.exists(data_dir):
    os.mkdir(data_dir)

# 第 1 步：加载与预处理数据
# a）现在读取 CSV 格式的数据集，并获取文件名与对应的标注。
# load dataset
train = pd.read_csv(os.path.join(data_dir, 'Train', 'train.csv'))
test = pd.read_csv(os.path.join(data_dir, 'Test.csv'))

sample_submission = pd.read_csv(
    os.path.join(data_dir, 'Sample_Submission.csv'))

train.head()

# b）接下来可以打印准备好的图片。
# print an image
img_name = rng.choice(train.filename)
filepath = os.path.join(data_dir, 'Train', 'Images', 'train', img_name)

img = imread(filepath, flatten=True)

pylab.imshow(img, cmap='gray')
pylab.axis('off')
pylab.show()


# c）对于更简单的数据操作，我们可以储存所有的图像作为 NumPy 数组。
# load images to create train and test set
temp = []
for img_name in train.filename:
    image_path = os.path.join(data_dir, 'Train', 'Images', 'train', img_name)
    img = imread(image_path, flatten=True)
    img = img.astype('float32')
    temp.append(img)

train_x = np.stack(temp)

train_x /= 255.0
train_x = train_x.reshape(-1, 784).astype('float32')

temp = []
for img_name in test.filename:
    image_path = os.path.join(data_dir, 'Train', 'Images', 'test', img_name)
    img = imread(image_path, flatten=True)
    img = img.astype('float32')
    temp.append(img)

test_x = np.stack(temp)

test_x /= 255.0
test_x = test_x.reshape(-1, 784).astype('float32')

train_y = train.label.values


# d）因为这个是一个典型的机器学习问题，所以我们可以创建验证集以监控模型的运行情况。
# 下面我们以 7:3 的比例分割训练集与验证集。
# create validation set
split_size = int(train_x.shape[0]*0.7)

train_x, val_x = train_x[:split_size], train_x[split_size:]
train_y, val_y = train_y[:split_size], train_y[split_size:]


# 第 2 步：构建模型
# a）下面是模型的主体，我们定义的神经网络共有三层，即输入层、隐藏层和输出层。
# 输入层和输出层的神经元数量是固定的，即 28 x 28 和 10 x 1，它们分别代表了输入图像的像素和类别。
# 我们在隐藏层采用了 50 个神经元，并采用 Adam 作为最优化算法。
import torch
from torch.autograd import Variable
# number of neurons in each layer
input_num_units = 28*28
hidden_num_units = 500
output_num_units = 10

# set remaining variables
epochs = 5
batch_size = 128
learning_rate = 0.001


# b）以下将开始训练模型。
# define model
model = torch.nn.Sequential(
    torch.nn.Linear(input_num_units, hidden_num_units),
    torch.nn.ReLU(),
    torch.nn.Linear(hidden_num_units, output_num_units),
)
loss_fn = torch.nn.CrossEntropyLoss()

# define optimization algorithm
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
# helper functions
# preprocess a batch of dataset


def preproc(unclean_batch_x):
    """Convert values to range 0-1"""
    temp_batch = unclean_batch_x / unclean_batch_x.max()

    return temp_batch

# create a batch


def batch_creator(batch_size):
    dataset_name = 'train'
    dataset_length = train_x.shape[0]

    batch_mask = rng.choice(dataset_length, batch_size)

    batch_x = eval(dataset_name + '_x')[batch_mask]
    batch_x = preproc(batch_x)

    if dataset_name == 'train':
        batch_y = eval(dataset_name).ix[batch_mask, 'label'].values

    return batch_x, batch_y


# train network
total_batch = int(train.shape[0]/batch_size)

for epoch in range(epochs):
    avg_cost = 0
    for i in range(total_batch):
        # create batch
        batch_x, batch_y = batch_creator(batch_size)

        # pass that batch for training
        x, y = Variable(torch.from_numpy(batch_x)), Variable(
            torch.from_numpy(batch_y), requires_grad=False)
        pred = model(x)

        # get loss
        loss = loss_fn(pred, y)

        # perform backpropagation
        loss.backward()
        optimizer.step()
        avg_cost += loss.data[0]/total_batch

    print(epoch, avg_cost)
# get training accuracy
x, y = Variable(torch.from_numpy(preproc(train_x))), Variable(
    torch.from_numpy(train_y), requires_grad=False)
pred = model(x)

final_pred = np.argmax(pred.data.numpy(), axis=1)

accuracy_score(train_y, final_pred)
# get validation accuracy
x, y = Variable(torch.from_numpy(preproc(val_x))), Variable(
    torch.from_numpy(val_y), requires_grad=False)
pred = model(x)
final_pred = np.argmax(pred.data.numpy(), axis=1)

accuracy_score(val_y, final_pred)
