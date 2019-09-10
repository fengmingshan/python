# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-09-09 22:26:15
# @Last Modified by:   Administrator
# @Last Modified time: 2019-09-10 09:20:21

from __future__ import print_function, division
import os
import torch
import pandas as pd              #用于更容易地进行csv解析
from skimage import io, transform    #用于图像的IO和变换
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils

# 忽略警告
import warnings
warnings.filterwarnings("ignore")

plt.ion()   # 交互模式

# 下载人脸识别数据集存放到本地
data_path = 'D:/_python/神经网络数据集/faces'
os.chdir(data_path)
# 数据集是按如下规则打包成的csv文件:
# image_name,part_0_x,part_0_y,part_1_x,part_1_y,part_2_x, ... ,part_67_x,part_67_y

# 读取数据集

landmarks_frame = pd.read_csv('./face_landmarks.csv')

n = 65 #图片号码
img_name = landmarks_frame.iloc[n, 0]
landmarks = landmarks_frame.iloc[n, 1:].as_matrix()
# 每幅图片有68个标注点，分别对应 x,y 两个坐标，reshape成两行之后得到x，y坐标
landmarks = landmarks.astype('float').reshape(-1, 2)

print('Image name: {}'.format(img_name))
print('Landmarks shape: {}'.format(landmarks.shape))
print('First 4 Landmarks: {}'.format(landmarks[:4]))

# 写一个简单的函数来展示一张图片和它对应的标注点作为例子。
def show_landmarks(image, landmarks):
    """显示带有地标的图片"""
    plt.imshow(image)
    plt.scatter(landmarks[:, 0], landmarks[:, 1], s=10, marker='.', c='r')
    plt.pause(0.001)  # pause a bit so that plots are updated

plt.figure()
show_landmarks(io.imread(os.path.join('./', img_name)),
               landmarks)
plt.show('hold')


# 数据集类
# torch.utils.data.Dataset是表示数据集的抽象类，因此自定义数据集应继承Dataset并覆盖以下方法 
# * __len__ 实现 len(dataset) 返还数据集的尺寸。
# * __getitem__用来获取一些索引数据，例如 dataset[i] 中的(i)。

# 建立面部数据集类
class FaceLandmarksDataset(Dataset):
    """面部标记数据集."""

    def __init__(self, csv_file, root_dir, transform=None):
        """
        csv_file（string）：带注释的csv文件的路径。
        root_dir（string）：包含所有图像的目录。
        transform（callable， optional）：一个样本上的可用的可选变换
        """
        self.landmarks_frame = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.landmarks_frame)

    def __getitem__(self, idx):
        img_name = os.path.join(self.root_dir,
                                self.landmarks_frame.iloc[idx, 0])
        image = io.imread(img_name)
        landmarks = self.landmarks_frame.iloc[idx, 1:]
        landmarks = np.array([landmarks])
        landmarks = landmarks.astype('float').reshape(-1, 2)
        sample = {'image': image, 'landmarks': landmarks}

        if self.transform:
            sample = self.transform(sample)

        return sample


face_dataset = FaceLandmarksDataset(csv_file='./face_landmarks.csv',
    root_dir='./')

fig = plt.figure()

for i in range(len(face_dataset)):
    sample = face_dataset[i]

    print(i, sample['image'].shape, sample['landmarks'].shape)

    ax = plt.subplot(1, 4, i + 1)
    plt.tight_layout()
    ax.set_title('Sample #{num}'.format(num = i))
    ax.axis('off')
    show_landmarks(**sample)
    if i == 3:
        plt.show('hold')
        break

# 数据变换
# 通过上面的例子我们会发现图片并不是同样的尺寸。
# 绝大多数神经网络都假定图片的尺寸相同。因此我们需要做一些预处理。
# 让我们创建三个转换:
# * Rescale：缩放图片
# * RandomCrop：对图片进行随机裁剪。这是一种数据增强操作
# * ToTensor：把numpy格式图片转为torch格式图片 (我们需要交换坐标轴).

class Rescale(object):
    """将样本中的图像重新缩放到给定大小。.

    Args:
        output_size（tuple或int）：所需的输出大小。 如果是元组，则输出为
         与output_size匹配。 如果是int，则匹配较小的图像边缘到output_size保持纵横比相同。
    """

    def __init__(self, output_size):
        assert isinstance(output_size, (int, tuple))
        self.output_size = output_size

    def __call__(self, sample):
        image, landmarks = sample['image'], sample['landmarks']

        h, w = image.shape[:2]
        if isinstance(self.output_size, int):
            if h > w:
                new_h, new_w = self.output_size * h / w, self.output_size
            else:
                new_h, new_w = self.output_size, self.output_size * w / h
        else:
            new_h, new_w = self.output_size

        new_h, new_w = int(new_h), int(new_w)

        img = transform.resize(image, (new_h, new_w))

        # h and w are swapped for landmarks because for images,
        # x and y axes are axis 1 and 0 respectively
        landmarks = landmarks * [new_w / w, new_h / h]

        return {'image': img, 'landmarks': landmarks}


class RandomCrop(object):
    """随机裁剪样本中的图像.

    Args:
       output_size（tuple或int）：所需的输出大小。 如果是int，就进行正方形方形裁剪。
    """

    def __init__(self, output_size):
        assert isinstance(output_size, (int, tuple))
        if isinstance(output_size, int):
            self.output_size = (output_size, output_size)
        else:
            assert len(output_size) == 2
            self.output_size = output_size

    def __call__(self, sample):
        image, landmarks = sample['image'], sample['landmarks']

        h, w = image.shape[:2]
        new_h, new_w = self.output_size

        top = np.random.randint(0, h - new_h)
        left = np.random.randint(0, w - new_w)

        image = image[top: top + new_h,
                      left: left + new_w]

        landmarks = landmarks - [left, top]

        return {'image': image, 'landmarks': landmarks}


class ToTensor(object):
    """将样本中的ndarrays转换为Tensors."""

    def __call__(self, sample):
        image, landmarks = sample['image'], sample['landmarks']
        # 交换颜色轴,H代表高，W代表宽，C代表颜色，因为
        # numpy包的图片是: H * W * C
        # torch包的图片是: C * H * W
        image = image.transpose((2, 0, 1))
        return {'image': torch.from_numpy(image),
                'landmarks': torch.from_numpy(landmarks)}

# 接下来我们把这些转换应用到一个例子上
# 我们想要把图像的短边调整为256，然后随机裁剪(randomcrop)为224大小的正方形。
# 也就是说，我们打算组合一个Rescale和 RandomCrop的变换。
# 我们可以调用一个简单的类 torchvision.transforms.Compose可以把多个步骤整合到一起。具体实现如下图：
scale = Rescale(256)
crop = RandomCrop(128)
composed = transforms.Compose([Rescale(256),
                               RandomCrop(224)])

# 在样本上应用上述的每个变换。
fig = plt.figure()
sample = face_dataset[65]
for i, tsfrm in enumerate([scale, crop, composed]):
    transformed_sample = tsfrm(sample)
    ax = plt.subplot(1, 3, i + 1)
    plt.tight_layout()
    ax.set_title(type(tsfrm).__name__)
    show_landmarks(**transformed_sample)
plt.show('hold')


# 使用for i in range循环来对整个数据集执行同样的操作。
transformed_dataset = FaceLandmarksDataset(csv_file='./face_landmarks.csv',
                                           root_dir='./',
                                           transform=transforms.Compose([
                                               Rescale(256),
                                               RandomCrop(224),
                                               ToTensor()
                                           ]))

for i in range(len(transformed_dataset)):
    sample = transformed_dataset[i]
    # 在使用plt.imshow前必须先将图片格式转成numpy数组，并且对维度进行转置
    # 因为numpy包的图片是: H * W * C ，torch包的图片是: C * H * W。
    # 所以transpose((1, 2, 0))可以将torch图片，转成numpy图片。
    plt.imshow(sample['image']grid.numpy().transpose((1, 2, 0)))
    plt.show('hold')

    print(i, sample['image'].size(), sample['landmarks'].size())

    if i == 3:
        break

# 但是对所有全量数据集简单的使用for循环牺牲了很多性能
# torch.utils.data.DataLoader是一个提供上述所有这些功能的迭代器。参数DataLoader=（num_workers=n）表示进程数量
# 但是这个库目前有bug，使用多进程会报错，所以不要

dataloader = DataLoader(transformed_dataset, batch_size=4,
                        shuffle=True)

# 辅助功能：显示批次
def show_landmarks_batch(sample_batched):
    """Show image with landmarks for a batch of samples."""
    images_batch, landmarks_batch = \
            sample_batched['image'], sample_batched['landmarks']
    batch_size = len(images_batch)
    im_size = images_batch.size(2)
    grid_border_size = 2

    # utils.make_grid的作用是将多幅图拼接成一幅图
    grid = utils.make_grid(images_batch)
    # 在使用plt.imshow前必须先将图片格式转成numpy数组，并且对维度进行转置
    # 因为numpy包的图片是: H * W * C ，torch包的图片是: C * H * W。
    # 所以transpose((1, 2, 0))可以将torch图片，转成numpy图片。
    plt.imshow(grid.numpy().transpose((1, 2, 0)))

    for i in range(batch_size):
        plt.scatter(landmarks_batch[i, :, 0].numpy() + i * im_size + (i + 1) * grid_border_size,
                    landmarks_batch[i, :, 1].numpy() + grid_border_size,
                    s=10, marker='.', c='r')

        plt.title('Batch from dataloader')

for i_batch, sample_batched in enumerate(dataloader):
    print(i_batch, sample_batched['image'].size(),
          sample_batched['landmarks'].size())

    # 观察第4批次并停止。
    if i_batch == 3:
        plt.figure()
        show_landmarks_batch(sample_batched)
        plt.axis('off')
        plt.ioff()
        plt.show()
        break

# torchvision:torchvision中还有一个更常用的数据集类ImageFolder。 它假定了数据集是以如下方式构造的:
# root/ants/xxx.png
# root/ants/xxy.jpeg
# root/ants/xxz.png
# .
# root/bees/123.jpg
# root/bees/nsdf3.png
# root/bees/asd932_.png
# 其中'ants’,bees’等是分类标签。
# 你可以按如下的方式创建一个数据加载器(dataloader)

import torch
from torchvision import transforms, datasets

data_transform = transforms.Compose([
        transforms.RandomSizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])
hymenoptera_dataset = datasets.ImageFolder(root='D:/_python/神经网络数据集/hymenoptera_data/train',
                                           transform=data_transform)
dataset_loader = torch.utils.data.DataLoader(hymenoptera_dataset,
                                             batch_size=4, shuffle=True,
                                             num_workers=4)