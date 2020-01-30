# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 11:35:55 2020

@author: Administrator
"""

import sys
print(sys.path)

# 将自定义包的路径添加在系统路径中
sys.path.append('D:\\_python\\custom-package')

# 删除自定义路径
# sys.path.remove('D:\\_python\\custom-package')

# 然后就就可以导入自定义包了
# import xxx
# 注意如果你通过文件夹来管理包的话
# 必须这样导入你的包 from xxx.yyy import zzz
# xxx 为文件夹名
# yyy 为.py文件名
# yyy 为.py文件里面的类名