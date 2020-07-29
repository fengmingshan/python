# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 14:47:08 2020

@author: Administrator
"""

from selenium import webdriver
from PIL import Image
from aip import AipOcr
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

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
    threshold = 200  # 该阈值不适合所有验证码，具体阈值请根据验证码情况设置
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
sleep(3)

# =============================================================================
# 通过百度OCR识别验证码
# =============================================================================
APP_ID = '21634494'
API_KEY = 'DnPBRKmkGi7y8jSzGsxaB8c3'
SECRET_KEY = 'Zmb01t6WWWtwbVs91jibixUk7evrdIl7'

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
driver.find_element_by_id('password').send_keys('Dx124578!')
driver.find_element_by_id('verifycode').send_keys(verify_code)

driver.find_element_by_id("loginsubmit").click()

sleep(10)

# 点击导航栏
driver.find_element_by_xpath("//*[@id='app']/div[3]/div/ul[2]").click()
sleep(2)

# 点击综合查询
driver.find_element_by_xpath("//*[@id='popover-content-inner-id']/div[1]/dl[1]/dd/a[2]").click()


driver.find_element_by_xpath("//*[@id='app']/div[4]/ul/li[3]/a").click()
#driver.find_element_by_xpath("//*[@id='app']/div[4]/ul/li[1]/a").click()

iframes = driver.find_elements_by_tag_name("iframe")
iframe = iframes[len(iframes)-1]
driver.switch_to.frame(iframe)

driver.find_element_by_xpath("//*[@id='queryForm:isQueryHis:2']").click()

driver.find_element_by_xpath("//*[@id='queryForm:deviceidText']").send_keys('FS-53-001-20200601-581843')

js1 = 'document.getElementById("queryForm:starttimeInputDate").removeAttribute("readonly")'
js2 = 'document.getElementById("queryForm:endtimeInputDate").removeAttribute("readonly")'
js3 = 'document.getElementById("queryForm:revertstarttimeInputDate").removeAttribute("readonly")'
js4 = 'document.getElementById("queryForm:revertendtimeInputDate").removeAttribute("readonly")'

driver.execute_script(js1)
driver.execute_script(js2)
driver.execute_script(js3)
driver.execute_script(js4)
driver.find_element_by_xpath("//*[@id='queryForm:starttimeInputDate']").clear()
driver.find_element_by_xpath("//*[@id='queryForm:endtimeInputDate']").clear()
driver.find_element_by_xpath("//*[@id='queryForm:revertstarttimeInputDate']").clear()
driver.find_element_by_xpath("//*[@id='queryForm:revertendtimeInputDate']").clear()

driver.find_element_by_xpath("//*[@id='queryForm:btn']").click()

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='listForm:billListTable:0:list_Column1']/center/a[2]")))
driver.find_element_by_xpath("//*[@id='listForm:billListTable:0:list_Column1']/center/a[2]").click()

driver.find_element_by_xpath("//*[@id='elecConInfo']")
