# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-09-10 22:28:02
# @Last Modified by:   Administrator
# @Last Modified time: 2019-09-11 11:06:31
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

# 自定义数据MNIST集
class My_Mnist_Dataset(Dataset):
    """我自己自定义的mnist数据集合"""

    def __init__(self, csv_file, root_dir, transform=None):
        """
        csv_file（string）：带注释的csv文件的路径。
        root_dir（string）：包含所有图像的目录。
        transform（callable， optional）：一个样本上的可用的可选变换
        """
        self.images = pd.read_csv(csv_file).values
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img = self.images[idx, 1:]
        # torch包的图片是: C * H * W，所以需要通过reshape调整颜色轴
        img = img.reshape(1,28,28)
        # np.array转torch.tensor
        img = torch.from_numpy(img)
        # 通过.float().div(255)操作将0-255之间的灰度转为0-1
        img = img.float().div(255)
        lable = self.images[idx,0]
        if self.transform:
            img = self.transform(img)
        sample = (img, lable)
        return sample

# 为什么这里是Normalize((0.1307,), (0.3081,))？
# 因为制作MNIST数据集的作者已经算好了mean和std，我们只要带入使用就行了
transform = transforms.Compose([
    transforms.Normalize((0.1307,), (0.3081,))]
)

train_dataset = My_Mnist_Dataset(csv_file = './mnist_train.csv',
    root_dir='./',transform = transform)

train_loader = DataLoader(train_dataset, batch_size=64,
                        shuffle=True)

test_dataset = My_Mnist_Dataset(csv_file = './mnist_test.csv',
    root_dir='./',transform = transform)

test_loader = DataLoader(train_dataset, batch_size=4,
                        shuffle=True)

train_iter = iter(train_loader)
# 取图片数据，因为trainloader设置了batch_size=4，所以没运行一次.next()方法就会取出4幅图
images, labels = train_iter.next()

# 显示图片
# 自定义一个显示图片的函数
def imshow(img):
    # 对图片进行Normalize()的反运算
    img = img*0.3081 + 0.1307
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()

# torchvision.utils.make_grid的作用是将多幅图拼接成一幅图,padding是每幅图中间的宽度
# 因为一次读入了4幅图片，所以images的shape是[4, 3, 32, 32]
imshow(torchvision.utils.make_grid(images,padding = 2))

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




# =============================================================================
# 训练模型
# =============================================================================
lr = 0.01
momentum = 0.5
log_interval = 16
epoch = 3

cnn = CNN()
cnn.train()

# 定义优化器
optimizer = optim.SGD(cnn.parameters(), lr=lr,
                          momentum=momentum)
# 使用for循环训练模型
print("Training...")
start = time.time()

for i in range(epoch):
    for batch_idx, (images, lables) in enumerate(train_loader):
        optimizer.zero_grad()
        output = cnn(images)
        # 定义损失函数
        loss = F.nll_loss(output, lables)
        loss.backward()
        optimizer.step()
        if batch_idx % log_interval == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                i, batch_idx * len(images), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item()))

end = time.time()
t = end - start
print ('Train：%dmin%.3fsec' %  ((int)(t/60), t-60*(int)(t/60)))

# =============================================================================
# 随机选取test集中的图片测试模型
# =============================================================================

# 定义一个随机选图片测试模型的函数:
# 该函数接收3个参数model,banchs,data_load
# model：要测试的模型，banchs：测试批次，data_load：数据集
def test_model(model,banchs,data_load):
    model.eval()
    # 分类结果:
    classes = (0,1,2,3,4,5,6,7,8,9)
    # get some random test images
    test_iter = iter(data_load)

    # 自定义一个显示图片的函数
    def imshow(img):
        # Normalize()的反运算
        img = img*0.3081 + 0.1307
        npimg = img.numpy()
        plt.imshow(np.transpose(npimg, (1, 2, 0)))
        plt.show()

    for i in range(banchs):
        # 取图片数据，因为trainloader设置了batch_size=4，所以没运行一次.next()方法就会取出4幅图
        images, labels = test_iter.next()
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
        time.sleep(2)

# 随机抽取图片测试模型
test_model(cnn,10,test_loader)

# =============================================================================
# 保存和重新加载模型
# =============================================================================

# 保存模型配置文件
torch.save(cnn.state_dict(), 'net_3_epoch.ckpt')

# 打印模型参数表
#print("net's state_dict:")
#for var_name in net.state_dict():
#    print(var_name, "\t", net.state_dict()[var_name])

# 重新加载网络模型
# 模型实例化
model = CNN()
# 加载模型参数
model.load_state_dict(torch.load('./cnn模型备份/net_3_epoch.ckpt'))
# 在测试模型前，你必须调用model.eval来关闭 BatchNormalization 和 Dropout
# 否则会导致不一致的测试结果.
model.eval()

# 下面可以输入图片开始测试了。

# 随机抽取图片测试模型
test_model(model,10,test_loader)


