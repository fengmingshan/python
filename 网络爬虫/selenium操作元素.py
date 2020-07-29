#一、鼠标点击元素操作

driver=webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.baidu.com/")

#找到“登录”这个按钮，并且点击（click（））
WebDriverWait(driver,15).until(EC.visibility_of_element_located((By.XPATH,'//div[@id="u1"]//a[text()="登录"]'))).click()

#二、alter弹框

driver=webdriver.Chrome()
driver.maximize_window()
driver.get("E:\\python08\\web_selenium\\HTML_HomeWork.html")
driver.execute_script("window.alert('这是一个测试Alert弹窗');")
WebDriverWait(driver,30).until(EC.alert_is_present())        #等待直到alert弹框出现

#切换到该alert弹框
alert=driver.switch_to.alert

#获取alert弹框的文本
text=alert.text
print(text)

#接受该alert弹框的内容
alert.accept()

#不接受（取消）
alert.dismiss() 

#三、鼠标操作

#在进行页面操作时，需要用鼠标进行左键点击、右键点击、双击、鼠标悬浮（比如鼠标移到某个位置就会出现一些元素）、鼠标拖动等操作，这时需要导入ActionChains模块

perform() 执行所有ActionChains 中存储的行为
click_and_hold(element)左键点击
context_click(elem) 右击
double_click(elem) 双击
drag_and_drop(source,target) 拖动
move_to_element(elem) 鼠标悬停
例如：百度首页，鼠标移动到“设置”时会出现下拉选项



from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()
driver.maximize_window()

driver.get("http://www.baidu.com")

#找到“设置”这个元素

element = driver.find_element_by_xpath('//div[@id="u1"]//a[@name="tj_settingicon"]')
#实例化ActionChains类
#调用鼠标操作
#最后，调用perform()去执行所有的鼠标动作。
ac = ActionChains(driver)
# 鼠标悬浮
ac.move_to_element(element)
# 执行鼠标动作
ac.perform()

以上操作，可以合起来写成一条代码：ActionChains(driver).move_to_element(element).perform()

tips:鼠标悬浮的下拉列表元素定位：CTRL + Shift + C,松开，移动到要定位的元素处

#四、下拉选项框


from selenium.webdriver.support.ui import Select

sele_obj = driver.find_element_by_xpath('//select[@name="ft"]')      #找到该下拉选项框
#实例化
select = Select(sele_obj)
#根据下标选值
select.select_by_index(2)
#根据value属性选值
select.select_by_value("rtf")
#根据文本内容选值
select.select_by_visible_text("Adobe Acrobat PDF (.pdf)")

#五、窗口切换

#网页上的某些操作会打开新的窗口，如果要到新的窗口去做其他操作，就需要进行窗口切换

#打开一个浏览器 - 与浏览器之间的会话开始
driver = webdriver.Chrome()
#全屏操作
driver.maximize_window()

driver.get("http://www.baidu.com")

driver.find_element_by_id("kw").send_keys("火车票")   #百度首页输入“火车票”
driver.find_element_by_id("su").click()                        #点击查询

#等待元素出现
xpath_ele = '//h3/a[contains(text()," 12306")]'
ele_locator = (By.XPATH,xpath_ele)
WebDriverWait(driver,30,1).until(EC.visibility_of_element_located(ele_locator))

#获取未操作前的窗口总数 - 只有1个窗口
handles = driver.window_handles
print(handles)
#点击 - 带来窗口数量的变化 - 会有2个窗口(新窗口出现的时间把控不了)
driver.find_element_by_xpath(xpath_ele).click()

WebDriverWait(driver,10).until(EC.new_window_is_opened(handles))
#重新获取一下窗口列表 - 有2个窗口了
handles = driver.window_handles
print(handles)
#切换到新的窗口
driver.switch_to.window(handles[-1])

切换到第一个窗口
# driver.switch_to.window(windows[0])


#等待元素出现再操作
WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH,'//a[@href="XXXXXX"]')))
driver.find_element_by_xpath('//a[@href="XXXXXXX"]').click()

#关掉当前页面，回到第一个页面。
driver.close()