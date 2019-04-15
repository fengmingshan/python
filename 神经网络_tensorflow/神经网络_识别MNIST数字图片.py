# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 14:42:24 2018

@author: Administrator
"""

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
data_path = 'd:\_python\python\神经网络_tensorflow\mnist_data' + '\\'
mnist = input_data.read_data_sets(data_path, one_hot=True)

# =============================================================================
#  单层神经网络
# =============================================================================
numClasses = 10 
inputSize = 784 
numHiddenUnits = 50 
trainingIterations = 10000 
batchSize = 1000 


X = tf.placeholder(tf.float32, shape = [None, inputSize])
y = tf.placeholder(tf.float32, shape = [None, numClasses])

W1 = tf.Variable(tf.truncated_normal([inputSize, numHiddenUnits], stddev=0.1))
B1 = tf.Variable(tf.constant(0.1), [numHiddenUnits])
W2 = tf.Variable(tf.truncated_normal([numHiddenUnits, numClasses], stddev=0.1))
B2 = tf.Variable(tf.constant(0.1), [numClasses])

hiddenLayerOutput = tf.matmul(X, W1) + B1
hiddenLayerOutput = tf.nn.relu(hiddenLayerOutput)
finalOutput = tf.matmul(hiddenLayerOutput, W2) + B2

loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels = y, logits = finalOutput))
opt = tf.train.GradientDescentOptimizer(learning_rate = .1).minimize(loss)

correct_prediction = tf.equal(tf.argmax(finalOutput,1), tf.argmax(y,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

sess = tf.Session()
init = tf.global_variables_initializer()
sess.run(init)

for i in range(trainingIterations):
    batch = mnist.train.next_batch(batchSize)
    batchInput = batch[0]
    batchLabels = batch[1]
    _, trainingLoss = sess.run([opt, loss], feed_dict={X: batchInput, y: batchLabels})
    if i%1000 == 0:
        trainAccuracy = accuracy.eval(session=sess, feed_dict={X: batchInput, y: batchLabels})
        print ("step %d, training accuracy %g"%(i, trainAccuracy))
result = sess.run(finalOutput, feed_dict={X:batchInput})
df_result = pd.DataFrame(result)
df_result.to_csv(r'd:\_python\python\神经网络_tensorflow' + '\\' + 'result.csv')



# =============================================================================
# 两层神经网络
# =============================================================================
numHiddenUnitsLayer2 = 100
trainingIterations = 10000

X = tf.placeholder(tf.float32, shape = [None, inputSize])
y = tf.placeholder(tf.float32, shape = [None, numClasses])

W1 = tf.Variable(tf.random_normal([inputSize, numHiddenUnits], stddev=0.1))
B1 = tf.Variable(tf.constant(0.1), [numHiddenUnits])
W2 = tf.Variable(tf.random_normal([numHiddenUnits, numHiddenUnitsLayer2], stddev=0.1))
B2 = tf.Variable(tf.constant(0.1), [numHiddenUnitsLayer2])
W3 = tf.Variable(tf.random_normal([numHiddenUnitsLayer2, numClasses], stddev=0.1))
B3 = tf.Variable(tf.constant(0.1), [numClasses])

hiddenLayerOutput = tf.matmul(X, W1) + B1
hiddenLayerOutput = tf.nn.relu(hiddenLayerOutput)
hiddenLayer2Output = tf.matmul(hiddenLayerOutput, W2) + B2
hiddenLayer2Output = tf.nn.relu(hiddenLayer2Output)
finalOutput = tf.matmul(hiddenLayer2Output, W3) + B3

loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels = y, logits = finalOutput))
opt = tf.train.GradientDescentOptimizer(learning_rate = .1).minimize(loss)

correct_prediction = tf.equal(tf.argmax(finalOutput,1), tf.argmax(y,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

sess = tf.Session()
init = tf.global_variables_initializer()
sess.run(init)

for i in range(trainingIterations):
    batch = mnist.train.next_batch(batchSize)
    batchInput = batch[0]
    batchLabels = batch[1]
    _, trainingLoss = sess.run([opt, loss], feed_dict={X: batchInput, y: batchLabels})
    if i%1000 == 0:
        train_accuracy = accuracy.eval(session=sess, feed_dict={X: batchInput, y: batchLabels})
        print ("step %d, training accuracy %g"%(i, train_accuracy))

testInputs = mnist.test.images
testLabels = mnist.test.labels
acc = accuracy.eval(session=sess, feed_dict = {X: testInputs, y: testLabels})
print("testing accuracy: {}".format(acc))
