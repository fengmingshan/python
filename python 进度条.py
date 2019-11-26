#!/usr/bin/env python
# coding: utf-8

# # 对可迭代对象添加进度条

# In[ ]:


# 对于可以迭代的对象都可以使用下面这种方式，来实现可视化进度，非常方便
from tqdm import tqdm
import time

for i in tqdm(range(50)):
    time.sleep(0.1)
    pass


# In[ ]:


# 在使用tqdm的时候，可以将tqdm(range(100))替换为trange(100)代码如下
from tqdm import tqdm,trange
import time

for i in trange(50):
  time.sleep(0.1)
  pass


# # 显示当前处理的数据

# In[ ]:


# 通过tqdm提供的set_description方法可以实时查看每次处理的数据内容
from tqdm import tqdm
import time

pbar = tqdm(["a","b","c","d"])
for c in pbar:
  time.sleep(1)
  pbar.set_description("正在处理第文件： %s 。"%c)


# # 手动设置进度条更新的粒度

# In[ ]:


# 通过update方法可以控制每次进度条更新的进度

#total参数设置进度条的总长度
with tqdm(total=100) as t:
    for i in range(100):
        time.sleep(0.05)
        #每次更新进度条的长度
        t.update(1)


# In[ ]:


# 除了使用with之外，还可以使用另外一种方法实现上面的效果
#total参数设置进度条的总长度
pbar = tqdm(total=100)
for i in range(100):
    time.sleep(0.05)
    #每次更新进度条的长度
    pbar.update(1)
#关闭占用的资源
pbar.close()


# # 自定义进度条显示信息

# In[ ]:


# 通过set_description和set_postfix方法设置进度条显示信息
from tqdm import trange
from random import random,randint
import time

with trange(100) as t:
    for i in t:
        #设置进度条左边显示的信息
        t.set_description("GEN %i"%i)
        #设置进度条右边显示的信息
        t.set_postfix(loss=random(),gen=randint(1,999),str="h",lst=[1,2])
        time.sleep(0.1)


# In[ ]:



from tqdm import tqdm
import time

with tqdm(total=10,bar_format="{postfix[0]}{postfix[1][value]:>9.3g}",
    postfix=["Batch",dict(value=0)]) as t:
    for i in range(10):
        time.sleep(0.5)
        t.postfix[1]["value"] = i / 2
        t.update()


# # 多层循环进度条

# In[ ]:


# 通过tqdm也可以很简单的实现嵌套循环进度条的展示
from tqdm import tqdm
import time

for i in tqdm(range(20), ascii=True,desc="1st loop"):
  for j in tqdm(range(10), ascii=True,desc="2nd loop"):
    time.sleep(0.2)

# # 递归使用进度条

# In[6]:


from tqdm import tqdm
import os.path

def find_files_recursively(path, show_progress=True):
  files = []
  # total=1 assumes `path` is a file
  t = tqdm(total=1, unit="file", disable=not show_progress)
  if not os.path.exists(path):
    raise IOError("Cannot find:" + path)

  def append_found_file(f):
    files.append(f)
    t.update()

  def list_found_dir(path):
    """returns os.listdir(path) assuming os.path.isdir(path)"""
    try:
      listing = os.listdir(path)
    except:
      return []
    # subtract 1 since a "file" we found was actually this directory
    t.total += len(listing) - 1
    # fancy way to give info without forcing a refresh
    t.set_postfix(dir=path[-10:], refresh=False)
    t.update(0) # may trigger a refresh
    return listing

  def recursively_search(path):
    if os.path.isdir(path):
      for f in list_found_dir(path):
        recursively_search(os.path.join(path, f))
    else:
      append_found_file(path)

  recursively_search(path)
  t.set_postfix(dir=path)
  t.close()
  return files

find_files_recursively("d:/")


# # 在pandas中使用tqdm
# In[5]:
import pandas as pd
import time
import numpy as np
from tqdm import tqdm

df = pd.DataFrame(np.random.randint(0, 100, (100000, 6)))

tqdm.pandas(desc="my bar!")
df.progress_apply(lambda x: x**2)

 # print和进度条一起使用

# In[5]:


# 在使用tqdm显示进度条的时候，如果代码中存在print可能会导致输出多行进度条，此时可以将print语句改为tqdm.write
import time
for i in tqdm(range(10),ascii=True):
    tqdm.write("come on")
    time.sleep(0.5)


# In[ ]:




