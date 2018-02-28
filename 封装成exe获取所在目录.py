# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 14:44:06 2018

@author: Administrator
"""
import os
import sys

config_name = 'myapp.cfg'

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

config_path = os.path.join(application_path, config_name)