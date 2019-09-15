# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 14:57:02 2019

@author: Administrator
"""

import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2*np.pi, 256)
y1 = np.sin(x)
plt.plot(x, y1)
plt.show('hold')

x = np.linspace(0.5*np.pi, 2.5*np.pi, 256)
y2 = np.sin(x)
plt.plot(x, y2)
plt.show('hold')

x = np.linspace(1*np.pi, 3*np.pi, 256)
y3 = np.sin(x)
plt.plot(x, y3)
plt.show('hold')

x = np.linspace(1.5*np.pi, 3.5*np.pi, 256)
y4 = np.sin(x)
plt.plot(x, y4)
plt.show('hold')
