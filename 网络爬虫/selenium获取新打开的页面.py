windows = driver.current_window_handle #定位当前页面句柄

all_handles = driver.window_handles   #获取全部页面句柄

for handle in all_handles:          #遍历全部页面句柄
    if handle != windows:          #判断条件
        driver.switch_to.window(handle)      #切换到新页面