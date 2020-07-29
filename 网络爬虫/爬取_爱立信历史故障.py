# -*- coding: utf-8 -*-
"""
Created on Sun May 10 15:58:32 2020

@author: Administrator
"""

from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#chrome_options = Options()
#chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
#driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome()
month = 6
days = [1]

url = 'https://nbweb.lteenm.ynct.com/login'
driver.get(url)
sleep(2)

button1 = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, 'details-button')))
sleep(10)
button1.click()
link1 = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, 'proceed-link')))
sleep(1)
link1.click()
button2 = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, 'loginNoticeOk')))
sleep(1)
try:
    button2.click()
except:
    print('click fault!')
user_name = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, 'loginUsername')))
user_name.send_keys('qujing')
passwd = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, 'loginPassword')))
passwd.send_keys('Qjjk@2020')
submit = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, 'submit')))
submit.click()

alarm_search = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, 'a[href="/rest/apps/web/alarmsearch"]')))
alarm_search.click()

history1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, 'input.eaAlarmsearch-rLeft-historyAlarm')))
history1.click()

# history2 = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'input.eaAlarmsearch-rLeft-historyAlarm')))
# history2.click()

cur_window = driver.current_window_handle
for day in days:
    for hour in range(0, 23):
        start_time = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div.eaAlarmsearch-rLeft-StartDateTimeSelector input')))
        start_time.clear()
        start_time.send_keys(
            '{m}/{d}/2020 {h}:00:00'.format(m=str(month), d=str(day), h=str(hour)))
        sleep(1)
        end_time = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div.eaAlarmsearch-rLeft-EndDateTimeSelector input')))
        end_time.clear()
        end_time.send_keys(
            '{m}/{d}/2020 {h}:00:00'.format(m=str(month), d=str(day), h=str(hour+1)))
        sleep(1)
        submit1 = driver.find_element_by_class_name(
            'eaAlarmsearch-rLeft-SearchButton')
        try:
            submit1.click()
        except:
            print('click fault!')
        sleep(5)
        export = driver.find_element_by_class_name('elLayouts-ActionBarButton')
        try:
            export.click()
        except:
            print('click fault!')

        sleep(2)
        cur_handels = driver.window_handles
        new_handles = [handel for handel in cur_handels if handel !=cur_window]
        if len(new_handles)>0:
            driver.switch_to.window(new_handles[0])
        export_complete = WebDriverWait(driver, 120).until(EC.presence_of_element_located(
            (By.XPATH, "//p[text()='Export Completed']")))

#         driver.switch_to.window(cur_window)
        for handel in new_handles:
            if handel != cur_window:
                driver.switch_to.window(handel)
                driver.close()
        driver.switch_to.window(cur_window)
        print('{}日，{}点，爬取成功！'.format(str(day),str(hour)))

    start_time = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'div.eaAlarmsearch-rLeft-StartDateTimeSelector input')))
    start_time.clear()
    start_time.send_keys(
        '{m}/{d}/2020 23:00:00'.format(m=str(month), d=str(day)))
    sleep(1)
    end_time = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'div.eaAlarmsearch-rLeft-EndDateTimeSelector input')))
    end_time.clear()
    end_time.send_keys(
        '{m}/{d}/2020 00:00:00'.format(m=str(month), d=str(day+1)))
    sleep(1)
    submit1 = driver.find_element_by_class_name(
        'eaAlarmsearch-rLeft-SearchButton')
    try:
        submit1.click()
    except:
        print('click fault!')
    sleep(4)
    export = driver.find_element_by_class_name('elLayouts-ActionBarButton')
    sleep(1)
    try:
        export.click()
    except:
        print('click fault!')

    sleep(1)
    cur_handels = driver.window_handles
    new_handles = [handel for handel in cur_handels if handel !=cur_window]
    if len(new_handles)>0:
        driver.switch_to.window(new_handles[0])
    export_complete = WebDriverWait(driver, 120).until(EC.presence_of_element_located(
        (By.XPATH, "//p[text()='Export Completed']")))

#     driver.switch_to.window(cur_window)
    for handel in new_handles:
        if handel != cur_window:
            driver.switch_to.window(handel)
            driver.close()
    driver.switch_to.window(cur_window)
    print('{}日，23点，爬取成功！'.format(str(day)))

driver.quit()
str_day = [str(x) for x in days]
print('{}日的数据爬取成功！'.format(','.join(str_day)))
