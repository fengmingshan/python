# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 10:08:11 2019

@author: Administrator
"""

# =============================================================================
# PIL与Tensor
# PIL与Tensor的转换相对容易些，因为pytorch已经提供了相关的代码，我们只需要搭配使用即可：
# =============================================================================

import torch
from PIL import Image
import matplotlib.pyplot as plt

# loader使用torchvision中自带的transforms函数
loader = transforms.Compose([
    transforms.ToTensor()])

unloader = transforms.ToPILImage()

# PIL读取图片转化为Tensor
# 输入图片地址
# 返回tensor变量
def image_loader(image_name):
    image = Image.open(image_name).convert('RGB')
    image = loader(image).unsqueeze(0)
    return image.to(device, torch.float)

# 将PIL图片转化为Tensor
# 输入PIL格式图片
# 返回tensor变量
def PIL_to_tensor(image):
    image = loader(image).unsqueeze(0)
    return image.to(device, torch.float)

# Tensor转化为PIL图片
# 输入tensor变量
# 输出PIL格式图片
def tensor_to_PIL(tensor):
    image = tensor.cpu().clone()
    image = image.squeeze(0)
    image = unloader(image)
    return image

# 直接展示tensor格式图片
def imshow(tensor, title=None):
    image = tensor.cpu().clone()  # we clone the tensor to not do changes on it
    image = image.squeeze(0)  # remove the fake batch dimension
    image = unloader(image)
    plt.imshow(image)
    if title is not None:
        plt.title(title)
    plt.pause(0.001)  # pause a bit so that plots are updated

# 直接保存tensor格式图片
def save_image(tensor, **para):
    dir = 'results'
    image = tensor.cpu().clone()  # we clone the tensor to not do changes on it
    image = image.squeeze(0)  # remove the fake batch dimension
    image = unloader(image)
    if not osp.exists(dir):
        os.makedirs(dir)
    image.save('results_{}/s{}-c{}-l{}-e{}-sl{:4f}-cl{:4f}.jpg'
               .format(num, para['style_weight'], para['content_weight'], para['lr'], para['epoch'],
                       para['style_loss'], para['content_loss']))
# =============================================================================
# numpy与Tensor
# numpy格式是使用cv2，也就是python-opencv库读取出来的图片格式，
# 需要注意的是用python-opencv读取出来的图片和使用PIL读取出来的图片数据略微不同，
# 经测试用python-opencv读取出来的图片在训练时的效果比使用PIL读取出来的略差一些(详细过程之后发布)。
# =============================================================================
import cv2
import torch
import matplotlib.pyplot as plt
# numpy转化为tensor
def toTensor(img):
    assert type(img) == np.ndarray,'the img type is {}, but ndarry expected'.format(type(img))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = torch.from_numpy(img.transpose((2, 0, 1)))
    return img.float().div(255).unsqueeze(0)  # 255也可以改为256

# tensor转化为numpy
def tensor_to_np(tensor):
    img = tensor.mul(255).byte()
    img = img.cpu().numpy().squeeze(0).transpose((1, 2, 0))
    return img

# 展示numpy格式图片
def show_from_cv(img, title=None):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.figure()
    plt.imshow(img)
    if title is not None:
        plt.title(title)
    plt.pause(0.001)

# 展示tensor格式图片
def show_from_tensor(tensor, title=None):
    img = tensor.clone()
    img = tensor_to_np(img)
    plt.figure()
    plt.imshow(img)
    if title is not None:
        plt.title(title)
    plt.pause(0.001)

# 上面介绍的都是一张图片的转化，如果是n张图片一起的话，只需要修改一下相应代码即可。
# 举个例子，将之前说过的修改略微修改一下即可：

# 将 N x H x W X C 的numpy格式图片转化为相应的tensor格式
def toTensor(img):
    img = torch.from_numpy(img.transpose((0, 3, 1, 2)))
    return img.float().div(255).unsqueeze(0)