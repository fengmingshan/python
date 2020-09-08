# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 16:43:47 2020

@author: Administrator
"""

import gzip

def in2out(fin, fout):
    BufSize = 1024*8
    while True:
        buf = fin.read(BufSize)
        if len(buf) < 1:
            break
        fout.write(buf)
    fin.close()
    fout.close()


def zip_gz_file(src, out_path):
    dst = src + '.gz'
    fin = open(src, 'rb')
    fout = gzip.open(out_path + dst, 'wb')

    in2out(fin, fout)


def unzip_gz_file(gzFile, out_path):
    dst = gzFile.replace('.gz','')
    fin = gzip.open(gzFile, 'rb')
    fout = open(out_path + dst, 'wb')

    in2out(fin, fout)


if __name__ == '__main__':
    src = r'D:\tmp\src.txt'
    dst = r'D:\tmp\src.txt.gz'
    ori = r'D:\tmp\ori.txt'

    gZipFile(src, dst)
    print('zip over!')
    gunZipFile(dst, ori)
    print('unzip over!')