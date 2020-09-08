# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 17:12:17 2020

@author: Administrator
"""

class GZipTool:
    bufSize = 1024*8
    def __init__(self, bufSize):
        self.bufSize = bufSize
        self.fin = None
        self.fout = None

    def compress(self, src, out_path):
        self.dst = src + '.gz'
        self.fin = open(src, 'rb')
        self.fout = gzip.open(out_path + self.dst, 'wb')
        self.__in2out()

    def decompress(self, gzFile, out_path):
        self.dst = gzFile.replace('.gz','')
        self.fin = gzip.open(gzFile, 'rb')
        self.fout = open(out_path + self.dst, 'wb')

        self.__in2out()

    def __in2out(self,):
        while True:
            buf = self.fin.read(self.bufSize)
            if len(buf) < 1:
                break
            self.fout.write(buf)

        self.fin.close()
        self.fout.close()