# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 15:04:03 2018

@author: Administrator
"""

from PIL import Image
import glob, os

size = 128, 128

for infile in glob.glob("*.jpg"):
    file, ext = os.path.splitext(infile)
    im = Image.open(infile)
    im.thumbnail(size)
    im.save(file + ".thumbnail", "JPEG")