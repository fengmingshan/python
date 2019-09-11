# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 09:47:40 2019

@author: Administrator
"""

#-*-coding:utf-8-*-
import torch
from torchvision import transforms
from PIL import Image
import cv2

img_path = "./cat.59.jpg"

transform1 = transforms.Compose([
	transforms.CenterCrop((224,224)), # 只能对PIL图片进行裁剪
	transforms.ToTensor(),
	]
)

## PIL图片与Tensor互转
img_PIL = Image.open(img_path).convert('RGB')
img_PIL.show() # 原始图片
img_PIL_Tensor = transform1(img_PIL)
print(type(img_PIL))
print(type(img_PIL_Tensor))

#Tensor转成PIL.Image重新显示
new_img_PIL = transforms.ToPILImage()(img_PIL_Tensor).convert('RGB')
new_img_PIL.show() # 处理后的PIL图片

## opencv读取的图片与Tensor互转
# transforms中，没有对np.ndarray格式图像的操作
img_cv = cv2.imread(img_path)
transform2 = transforms.Compose([
	transforms.ToTensor(),
	]
)

img_cv_Tensor = transform2(img_cv)
print(type(img_cv))
print(type(img_cv_Tensor))
