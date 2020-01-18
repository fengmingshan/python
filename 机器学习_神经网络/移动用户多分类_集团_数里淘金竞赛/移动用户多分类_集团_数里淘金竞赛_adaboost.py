# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 23:25:18 2020

@author: Administrator
"""

import pandas as pd
import numpy as np
import os

from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.multiclass import OneVsOneClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

# =============================================================================
# 拆分 训练集 和 测试集
# =============================================================================
df_train = pd.read_csv('./数据集/训练集.csv', engine='python', encoding='utf-8')
df_test = pd.read_csv('./数据集/测试集.csv', engine='python', encoding='utf-8')

X = df_train.drop(['user', 'label'], axis=1)
y = df_train.label.values
X_train, X_valid, y_train, y_valid = train_test_split(
    X, y, test_size=0.3, stratify=y, shuffle=True, random_state=42)
X_train.shape
y_train.shape
X_valid.shape
y_valid.shape

# =============================================================================
# 建模训练
# =============================================================================
ovr_ = OneVsRestClassifier(GradientBoostingClassifier(n_estimators=100))
ovr.fit(X_train, y_train)  # 训练模型

y_pred = ovr.predict(X_valid)

Accuracy = accuracy_score(y_valid ,y_pred, normalize =True  )
Recall = recall_score(y_valid, y_pred, average='macro')
F1 = f1_score(y_valid, y_pred, average='weighted')
#F1_score = 2 * accuracy_score * recall_acc / (accuracy_score + recall_score)
F1_2 = F1**2
print('准确率 = {0} %'.format(round(Accuracy, 2)))
print('召回率 = {0} %'.format(round(Recall * 100, 2)))
print('F1 = {0}'.format(F1))
print('(F1)2 = {0}'.format(F1_2))


