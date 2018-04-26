# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 11:16:19 2018

@author: Administrator
"""

from PIL import Image
from pytesseract import image_to_string


path = r'd:\_python' + '\\'
image = Image.open(path + '2809.jpg')
imgry = image.convert('L')#图像加强，二值化
table = []    
threshold = 140
for i in range(256):    
    if i < threshold:    
        table.append(0)    
    else:    
        table.append(1)    
        
imgpoint = imgry.point(table,'1') 
imgpoint.save(path + 'out.jpg')
text = image_to_string(imgpoint,config='-psm 7')

print(text) 