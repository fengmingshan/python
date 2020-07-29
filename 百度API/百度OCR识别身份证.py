# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 19:20:16 2020

@author: Administrator
"""

import cv2
from aip import AipOcr

""" 你的 APPID AK SK  """
APP_ID = '11152511'
API_KEY = 'ueBdIukdXt1l7HFwD8ULehip'
SECRET_KEY = 'ZcOnmjOLRGIiKwR4cizGO9doQA5O9zdW'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

fname = 'd:/sfz.jpg'

""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

image = get_file_content(fname)

""" 调用通用文字识别, 图片参数为本地图片 """
results = client.general(image)["words_result"]  # 还可以使用身份证驾驶证模板，直接得到字典对应所需字段

img = cv2.imread(fname)
for result in results:
    text = result["words"]
    location = result["location"]

    print(text)
    # 画矩形框
    cv2.rectangle(img, (location["left"],location["top"]), (location["left"]+location["width"],location["top"]+location["height"]), (0,255,0), 2)

cv2.imwrite(fname[:-4]+"_result.jpg", img)