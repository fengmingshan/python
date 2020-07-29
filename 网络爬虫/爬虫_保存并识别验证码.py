# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 14:47:08 2020

@author: Administrator
"""

from selenium import webdriver
from PIL import Image
from aip import AipOcr

driver = webdriver.PhantomJS()
url = 'http://180.153.49.130:9000/baf/jsp/uiframe/login.jsp'  # 定义url地址
driver.get(url)  # 加载url网页
driver.save_screenshot('d:/printscreen.png')
verifyimg = driver.find_element_by_id('verifyimg')

left = verifyimg.location['x']
top = verifyimg.location['y']
right = verifyimg.location['x'] + verifyimg.size['width']
bottom = verifyimg.location['y'] + verifyimg.size['height']
im = Image.open('d:/printscreen.png')
im = im.crop((left, top, right, bottom))

def processing_image(img):
    img = img.convert("L")  # 转灰度
    pixdata = img.load()
    w, h = img.size
    threshold = 160  # 该阈值不适合所有验证码，具体阈值请根据验证码情况设置
    # 遍历所有像素，大于阈值的为黑色
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img


def delete_spot(images):
    data = images.getdata()
    w, h = images.size
    black_point = 0
    for x in range(1, w - 1):
        for y in range(1, h - 1):
            mid_pixel = data[w * y + x]  # 中央像素点像素值
            if mid_pixel < 50:  # 找出上下左右四个方向像素点像素值
                top_pixel = data[w * (y - 1) + x]
                left_pixel = data[w * y + (x - 1)]
                down_pixel = data[w * (y + 1) + x]
                right_pixel = data[w * y + (x + 1)]
                # 判断上下左右的黑色像素点总个数
                if top_pixel < 10:
                    black_point += 1
                if left_pixel < 10:
                    black_point += 1
                if down_pixel < 10:
                    black_point += 1
                if right_pixel < 10:
                    black_point += 1
                if black_point < 1:
                    images.putpixel((x, y), 255)
                black_point = 0
    return images


im = processing_image(im)
im = delete_spot(im)

im.save('d:/verifyimg.png')


# =============================================================================
# 通过百度OCR识别验证码
# =============================================================================
APP_ID = '11152511'
API_KEY = 'ueBdIukdXt1l7HFwD8ULehip'
SECRET_KEY = 'ZcOnmjOLRGIiKwR4cizGO9doQA5O9zdW'

# 初始化文字识别分类器
aipOcr=AipOcr(APP_ID, API_KEY, SECRET_KEY)
# 读取图片
filePath =r"d:/verifyimg.png"

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


# 定义参数变量
options = {
    'detect_direction': 'true',
    'language_type': 'CHN_ENG',
}

# 网络图片文字文字识别接口
result = aipOcr.webImage(get_file_content(filePath),options)
text = result['words_result'][0]
verify_code = text['words']
print(verify_code)

driver.find_element_by_id('loginName').send_keys('shiyanli-dx')
driver.find_element_by_id('password').send_keys('Dx124578！')
driver.find_element_by_id('verifycode').send_keys(verify_code)

driver.find_element_by_id("loginsubmit").click()

driver.save_screenshot('d:/123.png')


