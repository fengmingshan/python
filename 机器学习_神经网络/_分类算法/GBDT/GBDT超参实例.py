import os
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import cross_validation, metrics
from sklearn.grid_search import GridSearchCV

import matplotlib.pylab as plt
%matplotlib inline

path = 'D:/_python/python/机器学习_神经网络/分类算法/GBDT'
os.chdir(path)

train = pd.read_csv('./data/train_modified.csv')
label ='Disbursed' # Disbursed的值就是二元分类的输出
IDcol = 'ID'
train['Disbursed'].value_counts()

x_columns = [x for x in train.columns if x not in [label, IDcol]]
X = train[x_columns]
y = train['Disbursed']

gbm0 = GradientBoostingClassifier(random_state=10)
gbm0.fit(X,y)
y_pred = gbm0.predict(X)
y_predprob = gbm0.predict_proba(X)[:,1]
print("Accuracy : %.4g" % metrics.accuracy_score(y.values, y_pred))
print("AUC Score (Train): %f" % metrics.roc_auc_score(y, y_predprob))

# Accuracy : 0.9852
# AUC Score (Train): 0.900531

# 首先我们从步长(learning rate)和迭代次数(n_estimators)入手。
# 一般来说,开始选择一个较小的步长来网格搜索最好的迭代次数。
# 这里，我们将步长初始值设置为0.1。对于迭代次数进行网格搜索如下：
param_test1 = {'n_estimators':list(range(20,81,10))}
gsearch1 = GridSearchCV(estimator = GradientBoostingClassifier(learning_rate=0.1, min_samples_split=300,
                                  min_samples_leaf=20,max_depth=8,max_features='sqrt', subsample=0.8,random_state=10),
                       param_grid = param_test1, scoring='roc_auc',iid=False,cv=5)
gsearch1.fit(X,y)
gsearch1.grid_scores_, gsearch1.best_params_, gsearch1.best_score_


# 找到了一个合适的迭代次数:n_estimators
# 现在我们开始对决策树进行调参。
# 首先我们对决策树最大深度max_depth和 min_samples_split 进行网格搜索
param_test2 = {'max_depth':range(3,14,2), 'min_samples_split':range(100,801,200)}
gsearch2 = GridSearchCV(estimator = GradientBoostingClassifier(learning_rate=0.1, n_estimators=60, min_samples_leaf=20,
      max_features='sqrt', subsample=0.8, random_state=10),
   param_grid = param_test2, scoring='roc_auc',iid=False, cv=5)
gsearch2.fit(X,y)
gsearch2.grid_scores_, gsearch2.best_params_, gsearch2.best_score_

# 由于决策树深度7是一个比较合理的值，我们把它定下来，
# 对于内部节点再划分所需最小样本数 min_samples_split
param_test3 = {'min_samples_split':range(800,1900,200), 'min_samples_leaf':range(60,101,10)}
gsearch3 = GridSearchCV(estimator = GradientBoostingClassifier(learning_rate=0.1, n_estimators=60,max_depth=7,
                                     max_features='sqrt', subsample=0.8, random_state=10),
                       param_grid = param_test3, scoring='roc_auc',iid=False, cv=5)
gsearch3.fit(X,y)
gsearch3.grid_scores_, gsearch3.best_params_, gsearch3.best_score_

# 我们调了这么多参数了，终于可以都放到GBDT类里面去看看效果了。
# 现在我们用新参数拟合数据：
gbm1 = GradientBoostingClassifier(learning_rate=0.1, n_estimators=60,max_depth=7, min_samples_leaf =60,
               min_samples_split =1200, max_features='sqrt', subsample=0.8, random_state=10)
gbm1.fit(X,y)
y_pred = gbm1.predict(X)
y_predprob = gbm1.predict_proba(X)[:,1]
print "Accuracy : %.4g" % metrics.accuracy_score(y.values, y_pred)
print "AUC Score (Train): %f" % metrics.roc_auc_score(y, y_predprob)
