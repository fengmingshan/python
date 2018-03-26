# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 23:46:18 2018
重启挂掉的脚本
@author: Administrator
"""

import time

count = 0
def compute_number():
    for i in xrange(10):
        print('count number: %s' % str(i+1))
        time.sleep(1)
    raise Exception('a')

def main():  
    print ("AutoRes is starting")
    print ("Respawning")

    global count
    if count < 3:
        try:
            count += 1
            compute_number()
        except Exception:
            print(Exception)
            main()
        finally:
            print('success')

if __name__ == "__main__":  
    main()