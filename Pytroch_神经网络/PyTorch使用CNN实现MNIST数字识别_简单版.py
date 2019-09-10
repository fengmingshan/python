# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-09-10 20:04:43
# @Last Modified by:   Administrator
# @Last Modified time: 2019-09-10 21:08:20

import torch
import torch.nn as nn
import torchvision
import os
from torchvision import datasets,transforms
from torch.autograd import Variable
from matplotlib import pyplot as plt

data_path = 'd:/_python/神经网络数据集/mnist'
os.chdir(data_path)

class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Sequential(
                nn.Conv2d(1,48,kernel_size = 3,padding = 0), # 输出为48,26,26
                nn.BatchNorm2d(48),
                nn.ReLU(),
                # 输出为：48,13,13，输入的图片为 28*28，(28-3)/2+1 = 13，所以输出为 48*13*13。
                nn.MaxPool2d(kernel_size = 2,stride = 2)
        )
        self.layer2 = nn.Sequential(
                nn.Conv2d(48,96,kernel_size = 3,padding = 1), #96,26,26
                nn.BatchNorm2d(96),
                nn.ReLU(),
                nn.MaxPool2d(kernel_size = 2,stride = 2)  #96,6,6
        )
        self.fc = nn.Sequential(
                nn.Linear(96 * 6 * 6, 96),
                nn.BatchNorm1d(96),
                nn.ReLU(),
                nn.Linear(96, 128),
                nn.BatchNorm1d(128),
                nn.ReLU(),
                nn.Linear(128, 10)
        )
    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = x.reshape(x.shape[0],-1)
        x = self.fc(x)
        return x



model = CNN()
print(model)


model = model.train()

img_transform = transforms.Compose([transforms.ToTensor(),
                                    transforms.Normalize(mean = [0.5],std = [0.5])])
dataset_train = datasets.MNIST(root = './',transform = img_transform,train = True,download = True)
dataset_test = datasets.MNIST(root = './',transform = img_transform,train = False,download = True)

train_loader = torch.utils.data.DataLoader(dataset = dataset_train,batch_size=64,shuffle = True)
test_loader = torch.utils.data.DataLoader(dataset = dataset_test,batch_size=4,shuffle = False)

# 随机抽取图片显示
images,label = next(iter(train_loader))
print(images.shape)
print(label.shape)
images_example = torchvision.utils.make_grid(images)
# 转成numpy包的图片，并调整颜色轴
# H代表高，W代表宽，C代表颜色，因为：
# numpy包的图片是: H * W * C
# torch包的图片是: C * H * W，所以需要通过转置操作调整颜色轴
images_example = images_example.numpy().transpose(1,2,0)
mean = [0.5]
std = [0.5]
images_example = images_example*std + mean
plt.imshow(images_example)
plt.show()

def Get_ACC():
    correct = 0
    total_num = len(dataset_test)
    for item in test_loader:
        batch_imgs,batch_labels = item
        batch_imgs = Variable(batch_imgs)
        out = model(batch_imgs)
        _,pred = torch.max(out.data,1)
        correct += torch.sum(pred==batch_labels)
        # print(pred)
        # print(batch_labels)
    correct = correct.data.item()
    acc = correct/total_num
    print('correct={},Test ACC:{:.5}'.format(correct,acc))


# 定义优化器和损失函数
optimizer = torch.optim.Adam(model.parameters())
loss_f = nn.CrossEntropyLoss()

Get_ACC()
for epoch in range(1):
    print('epoch:{}'.format(epoch))
    cnt = 0
    for item in train_loader:
        batch_imgs ,batch_labels = item
        batch_imgs,batch_labels = Variable(batch_imgs),Variable(batch_labels)
        out = model(batch_imgs)
        # print(out.shape)
        loss = loss_f(out,batch_labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if(cnt%100==0):
            print_loss = loss.data.item()
            print('epoch:{},cnt:{},loss:{}'.format(epoch,cnt,print_loss))
        cnt+=1
    Get_ACC()

# 随机抽取图片进行测试
classes = (0,1,2,3,4,5,6,7,8,9)
test_data_iter = iter(test_loader)
for i in range(10):
    images,label = test_data_iter.next()

    out = model(images)
    _, predicted = torch.max(out, 1)
    images_example = torchvision.utils.make_grid(images)
    # 转成numpy包的图片，并调整颜色轴
    # H代表高，W代表宽，C代表颜色，因为：
    # numpy包的图片是: H * W * C
    # torch包的图片是: C * H * W，所以需要通过转置操作调整颜色轴
    images_example = images_example.numpy().transpose(1,2,0)
    # 因为读取数据的时候对img做了Normalize标准化，现在要反算回来
    mean = [0.5]
    std = [0.5]
    images_example = images_example*std + mean
    plt.imshow(images_example)
    plt.show()

    # print 预测结果
    print('Predicted: ', ' '.join('%s' % classes[predicted[j]]
        for j in range(6)))

    time.sleep(2)

