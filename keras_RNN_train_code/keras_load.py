# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 10:02:18 2019

@author: 54934
"""

from keras.models import load_model
import text_to_x as ttx
import numpy as np
model = load_model('keras.h5') #载入 
text='请回单，谢谢'
text=np.array(ttx.fk_text_to_x(text)[:157])
text=text.reshape(1,1,157)
y_pred = model.predict(text)  # 预测
print(y_pred)
print(np.argmax(y_pred))
