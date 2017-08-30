#!/usr/bin/python


"""
    Starter code for the evaluation mini-project.
    Start by copying your trained/tested POI identifier from
    that which you built in the validation mini-project.

    This is the second step toward building your POI identifier!

    Start by loading/formatting the data...
"""

import pickle
import sys
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit

data_dict = pickle.load(open("../final_project/final_project_dataset.pkl", "r") )

### add more features to features_list!
features_list = ["poi", "salary"]

data = featureFormat(data_dict, features_list)
labels, features = targetFeatureSplit(data)



### your code goes here 
from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import train_test_split

features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.3, random_state=42)

clf = DecisionTreeClassifier()
clf.fit(features_train, labels_train)
print clf.score(features_test, labels_test)

# How many POI in test set?
print sum(labels_test) # 4

# How many people in test set?
print len(labels_test) # 29

# What's accuracy for predicting all non-POI
# 25/29 = .86

# are there any true positives?
pred = clf.predict(features_test)
pairs = zip(pred, labels_test)
tp = 0
for x in pairs:
    if x == (1.0, 1.0):
        tp += 1
print tp #0

from sklearn.metrics import precision_score, recall_score
print 'precision: {}'.format(precision_score(labels_test, pred)) #0
print 'recall: {}'.format(recall_score(labels_test, pred)) #0

### Working with some fake data:
predictions = [0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1] 
truth = [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0]

paired = zip(predictions, truth)

true_positives = sum([1 for (p,t) in paired if (p,t)==(1,1)])
true_negatives = sum([1 for (p,t) in paired if (p,t)==(0,0)])
false_positives = sum([1 for (p,t) in paired if (p,t)==(1,0)])
false_negatives = sum([1 for (p,t) in paired if (p,t)==(0,1)])
print 'true positives: {}'.format(true_positives)
print 'true negatives: {}'.format(true_negatives)
print 'false positives: {}'.format(false_positives)
print 'false negatives: {}'.format(false_negatives)

precision = true_positives / float(true_positives + false_positives)
recall = true_positives / float(true_positives + false_negatives)
print 'precision: {}'.format(precision)
print 'recall: {}'.format(recall)


