# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 10:50:48 2018

@author: Administrator
"""

print('\n'.join([''.join([('ILOVEU!'[(x-y)%7]if((x*0.05)**2+(y*0.1)**2-1)**3-(x*0.05)**2*(y*0.1)**3<=0 else' ')for x in range(-30,30)])for y in range(15,-15,-1)]))

print(''.join(__import__('random').choice('\u2571\u2572') for i in range(50*24)))
