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


import math
from collections import defaultdict

import numpy as np


class AdaBoost:
    def __init__(self, epsilon=0.0):
        self.epsilon = epsilon  # 分类误差率阈值
        self.w = None  # 样本的权值,每加入一个基本分类器都要重新计算
        self.N = None
        self.g_list = []  # 弱分类器, 本程序暂设弱分类器由x<nu或x>nu产生,故用(0,nu)或(1,nu)表示
        self.alpha = []  # 基本分类器前面的系数
        self.base_list = []  # 基本分类器

    def init_param(self, X_data):
        # 初始化参数,包括权值和所有可能的弱分类器
        self.N = X_data.shape[0]
        self.w = np.ones(self.N) / self.N  # 初始化权值
        for i in range(1, self.N):  # 构建可能的弱分类器集合
            nu = (X_data[i][0] + X_data[i - 1][0]) / 2
            self.g_list.append((0, nu))  # 对应x<nu, 取 1
            self.g_list.append((1, nu))
        return

    def cal_weak_val(self, nu, X):
        # 返回弱分类器的预测值
        val = 1
        if (nu[0] == 0 and X[0] > nu[1]) or (nu[0] == 1 and X[0] <= nu[1]):
            val = -1
        return val

    def get_base(self, X_data, y_data):
        # 挑选出最佳的弱分类器作为基本分类器, 即获取使分类误差率最小的数据集切分点(基于上一轮更新的权重)
        g_err = defaultdict(float)  # 每个弱分类器对应的分类误差率

        for g in self.g_list:
            for i in range(self.N):
                if self.cal_weak_val(g, X_data[i]) != y_data[i]:
                    g_err[g] += self.w[i]  # 误差等于错误分类样本的权值之和，即sum{1*w}

        best_g = min(g_err, key=g_err.get)
        return best_g, g_err[best_g]

    def cal_alpha(self, err):
        # 计算基本分类器前的系数
        return 1.0 / 2 * math.log((1 - err) / err)

    def cal_weight(self, X_data, y_data, base, alpha):
        # 基于新加入的基本分类器，迭代更新每个样本权重
        for i in range(self.N):
            self.w[i] *= math.exp(-alpha * y_data[i] * self.cal_weak_val(base, X_data[i]))
        self.w = self.w / np.sum(self.w)
        return

    def _fx(self, X):
        # 基于当前的组合分类器，计算预测值
        s = 0
        for alpha, base in zip(self.alpha, self.base_list):
            s += alpha * self.cal_weak_val(base, X)
        return np.sign(s)

    def fit(self, X_data, y_data):
        # 构建最终的强分类器, 暂设输入维度为1
        self.init_param(X_data)

        while True:  # 逐步添加基本分类器
            base, err = self.get_base(X_data, y_data)
            alpha = self.cal_alpha(err)
            self.cal_weight(X_data, y_data, base, alpha)  # 更新样本权值
            self.alpha.append(alpha)
            self.base_list.append(base)

            s = 0
            for X, y in zip(X_data, y_data):
                if self._fx(X) != y:
                    s += 1
            if s / self.N <= self.epsilon:  # 分类错误数目占比小于等于epsilon, 停止训练
                print('the err ratio is {0}'.format(s / self.N))
                break
        return

    def predict(self, X):
        # 预测
        return self._fx(X)


if __name__ == '__main__':
    X_data_raw = np.linspace(-50, 50, 100)
    np.random.shuffle(X_data_raw)
    y_data = np.sign(X_data_raw)
    X_data = np.transpose([X_data_raw])
    from machine_learning_algorithm.cross_validation import validate

    g = validate(X_data, y_data)
    for item in g:
        X_train, y_train, X_test, y_test = item
        AB = AdaBoost(epsilon=0.02)
        AB.fit(X_train, y_train)
        score = 0
        for X, y in zip(X_test, y_test):
            if AB.predict(X) == y:
                score += 1
        print(score / len(y_test))
