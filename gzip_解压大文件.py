# -*- coding: utf-8 -*-
"""
Created on Mon May  6 15:46:33 2019

@author: Administrator
"""

import gzip

BufSize = 1024*8
def gZipFile(src, dst):
  fin = open(src, 'rb')
  fout = gzip.open(dst, 'wb')
  in2out(fin, fout)
def gunZipFile(gzFile, dst):
  fin = gzip.open(gzFile, 'rb')
  fout = open(dst, 'wb')
  in2out(fin, fout)
def in2out(fin, fout):
  while True:
    buf = fin.read(BufSize)
    if len(buf) < 1:
      break
    fout.write(buf)
  fin.close()
  fout.close()
if __name__ == '__main__':
  src = r'D:\tmp\src.txt'
  dst = r'D:\tmp\src.txt.gz'
  ori = r'D:\tmp\ori.txt'
  gZipFile(src, dst)
  print('gZipFile over!')
  gunZipFile(dst, ori)
  print('gunZipFile over!')


class GZipTool:
  def __init__(self, bufSize):
    self.bufSize = bufSize
    self.fin = None
    self.fout = None
  def compress(self, src, dst):
    self.fin = open(src, 'rb')
    self.fout = gzip.open(dst, 'wb')
    self.__in2out()
  def decompress(self, gzFile, dst):
    self.fin = gzip.open(gzFile, 'rb')
    self.fout = open(dst, 'wb')
    self.__in2out()
  def __in2out(self,):
    while True:
      buf = self.fin.read(self.bufSize)
      if len(buf) < 1:
        break
      self.fout.write(buf)
    self.fin.close()
    self.fout.close()