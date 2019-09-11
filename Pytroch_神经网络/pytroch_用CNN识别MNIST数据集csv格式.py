# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-09-10 22:28:02
# @Last Modified by:   Administrator
# @Last Modified time: 2019-09-11 09:10:36
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import os
import time
import numpy as np
import pandas as pd
from torch.autograd import Variable
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
import numpy as np

# 本例使用的是转成CSV格式的MNIST数据集，表格的第一列是lable，后面的img向量
# 注意：torch.nn只支持mini-batch的数据形式，而不支持单个的数据
# 例如，nn.conv2d接受四维的参数nSamples*nChannels*Height*Width.
# 如果你的input只有一个样本，用input.unsqueeze(0)加一个伪batch维度

data_path = 'd:/_python/神经网络数据集/mnist'
os.chdir(data_path)

# CNN （卷积神经网络）
# 定义CNN网络
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

transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.1307,), (0.3081,))])

# 自定义数据MNIST集
class my_mnist(Dataset):
    """我自己自定义的mnist数据集合"""

    def __init__(self, csv_file, root_dir, transform=None):
        """
        csv_file（string）：带注释的csv文件的路径。
        root_dir（string）：包含所有图像的目录。
        transform（callable， optional）：一个样本上的可用的可选变换
        """
        self.images = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img_name = os.path.join(self.root_dir,
                                self.landmarks_frame.iloc[idx, 0])
        image = io.imread(img_name)
        landmarks = self.landmarks_frame.iloc[idx, 1:]
        landmarks = np.array([landmarks])
        landmarks = landmarks.astype('float').reshape(-1, 2)
        sample = {'image': image, 'lable': landmarks}

        if self.transform:
            sample = self.transform(sample)

        return sample

# functions to show an image
def imshow(img):
    img = img / 2 + 0.5     # unnormalize
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()

# 训练

lr = 0.01
momentum = 0.5
seed = 1
log_interval = 32

cnn = CNN()
cnn.train()
optimizer = optim.SGD(cnn.parameters(), lr=lr,
                          momentum=momentum)

print("Training...")
start = time.time()

end = time.time()
t = end - start
print ('Train：%dmin%.3fsec' %  ((int)(t/60), t-60*(int)(t/60)))






