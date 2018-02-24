# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 21:49:39 2018

@author: Administrator
"""

# 构造一个PHANTOMJS对象  
phan = dict(DesiredCapabilities.PHANTOMJS)  
  
# 在运行前修改对象参数  
  
#设置user-agent请求头  
UserAgent = "..."  
phan["phantomjs.page.settings.userAgent"] = (UserAgent)  
  
# 禁止加载图片  
phan["phantomjs.page.settings.loadImages"] = False   
  
# 设置请求cookie  
phan["phantomjs.page.customHeaders.Cookie"] = 'SINAGLOBAL=3955422793326.2764.1451802953297;   
'  
# 禁用缓存  
phan["phantomjs.page.settings.disk-cache"] = True   
  
#  设置代理  
service_args = ['--proxy=127.0.0.1:9999','--proxy-type=socks5']  
  
# 加载自定义配置  
driver = webdriver.PhantomJS(r"D:\phantomjs-2.1.1-windows\bin\phantomjs.exe",desired_capabilities=phan,service_args=service_args)  
  
# 设定get url最大等待时间，规定时间内没有响应就会报错  
#  类似于requests.get()的timeout选项，但driver.get()没有timeout选项  
driver.set_page_load_timeout(40)  
  
# 设置脚本超时时间
driver.set_script_timeout(10)  

#多进程并发
from multiprocessing import Pool
pool = Pool(8)
data_list = pool.map(get, url_list)
pool.close()
pool.join()

#获得session_id  page_source  get_cookies()
browser.session_id  
browser.page_source  
browser.get_cookies()  

#使用chrome时，可以隐藏chrome的界面运行
from pyvirtualdisplay import Display  
display = Display(visible=0, size=(800,800))  
display.start()  


