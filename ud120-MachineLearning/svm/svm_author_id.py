#!/usr/bin/python

""" 
    This is the code to accompany the Lesson 2 (SVM) mini-project.

    Use a SVM to identify emails from the Enron corpus by their authors:    
    Sara has label 0
    Chris has label 1
"""
    
import sys
from time import time
sys.path.append("../tools/")
from email_preprocess import preprocess


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()




#########################################################
### your code goes here ###

from sklearn.svm import SVC

# clf = SVC(kernel='linear')
# t0 = time()
# clf.fit(features_train, labels_train)
# print 'training time: ', round(time()-t0, 3), 's'
# print 'accuracy: ', clf.score(features_test, labels_test)

# # training time: 143.204s
# # accuracy: .984073


# clf = SVC(kernel='linear')
# features_train = features_train[:len(features_train)/100]
# labels_train = labels_train[:len(labels_train)/100]
# t0 = time()
# clf.fit(features_train, labels_train)
# print 'training time: ', round(time()-t0, 3), 's'
# print 'accuracy: ', clf.score(features_test, labels_test)

# # training time: 0.076s
# # accuracy: .884528


# clf = SVC(kernel='rbf')
# features_train = features_train[:len(features_train)/100]
# labels_train = labels_train[:len(labels_train)/100]
# t0 = time()
# clf.fit(features_train, labels_train)
# print 'training time: ', round(time()-t0, 3), 's'
# print 'accuracy: ', clf.score(features_test, labels_test)

# # training time: 0.084s
# # accuracy: .616041


# clf = SVC(kernel='rbf', C=10000)
# features_train = features_train[:len(features_train)/100]
# labels_train = labels_train[:len(labels_train)/100]
# t0 = time()
# clf.fit(features_train, labels_train)
# print 'training time: ', round(time()-t0, 3), 's'
# print 'accuracy: ', clf.score(features_test, labels_test)

# # C=10
# # training time: 0.082s
# # accuracy: .616041
# # C=100
# # training time: 0.069s
# # accuracy: .616041
# # C=1000
# # training time: 0.081s
# # accuracy: .821388
# # C=10000
# # training time: 0.078s
# # accuracy: .892491


# clf = SVC(kernel='rbf', C=10000)
# t0 = time()
# clf.fit(features_train, labels_train)
# print 'training time: ', round(time()-t0, 3), 's'
# print 'accuracy: ', clf.score(features_test, labels_test)

# # training time: 92.895s
# # accuracy: .990899


# clf = SVC(kernel='rbf', C=10000)
# features_train = features_train[:len(features_train)/100]
# labels_train = labels_train[:len(labels_train)/100]
# t0 = time()
# clf.fit(features_train, labels_train)
# print 'training time: ', round(time()-t0, 3), 's'
# pred = clf.predict(features_test)
# print 'item 10: {}'.format(pred[10]) # 1
# print 'item 26: {}'.format(pred[26]) # 0
# print 'item 50: {}'.format(pred[50]) # 1


clf = SVC(kernel='rbf', C=10000)
t0 = time()
clf.fit(features_train, labels_train)
print 'training time: ', round(time()-t0, 3), 's'
pred = clf.predict(features_test)
print 'Chris (1): {}'.format(sum(pred)) # 877



#########################################################


