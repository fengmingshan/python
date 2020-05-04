# -*- coding: utf-8 -*-
"""
Created on Sat May  2 16:48:19 2020

@author: Administrator
"""

import os

path = 'D:/用户目录/'
os.chdir(path)
pathes = os.listdir(path)
#pathes.remove('System Volume Information')
#pathes.remove('$RECYCLE.BIN')

import os

def getFileFolderSize(fileOrFolderPath):
  """get size for file or folder"""
  totalSize = 0

  if not os.path.exists(fileOrFolderPath):
    return totalSize

  if os.path.isfile(fileOrFolderPath):
    totalSize = os.path.getsize(fileOrFolderPath) # 5041481
    return totalSize

  if os.path.isdir(fileOrFolderPath):
    with os.scandir(fileOrFolderPath) as dirEntryList:
      for curSubEntry in dirEntryList:
        curSubEntryFullPath = os.path.join(fileOrFolderPath, curSubEntry.name)
        if curSubEntry.is_dir():
          curSubFolderSize = getFileFolderSize(curSubEntryFullPath) # 5800007
          totalSize += curSubFolderSize
        elif curSubEntry.is_file():
          curSubFileSize = os.path.getsize(curSubEntryFullPath) # 1891
          totalSize += curSubFileSize

      return totalSize

dict_pathes = [(k,round(getFileFolderSize(k)/(1024*1024),2)) for k in pathes]

dict_pathes =sorted(dict_pathes,key = lambda x:x[1],reverse=True)

for i in dict_pathes:
    print(i)

