#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".

finance_features = ['salary', 'deferral_payments', 'total_payments', 'loan_advances', 'bonus', 'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses', 'exercised_stock_options', 'other', 'long_term_incentive', 'restricted_stock', 'director_fees']

email_features = ['to_messages', 'from_poi_to_this_person', 'from_messages', 'from_this_person_to_poi', 'shared_receipt_with_poi']

all_features = ['poi'] + finance_features + email_features

all_without_low_data = list(all_features)
all_without_low_data.remove('loan_advances')
all_without_low_data.remove('restricted_stock_deferred')
all_without_low_data.remove('deferred_income')
all_without_low_data.remove('director_fees')

my_four_features = ['poi', 'bonus', 'expenses', 'exercised_stock_options', 'other']
my_five_features = list(my_four_features)
my_five_features.append('poi_mail_rate')

features_list = my_four_features


### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)


### Task 2: Remove outliers
data_dict.pop('TOTAL', 0) # identified in the the outliers lesson

### Task 3: Create new feature(s)
# Bonus rate: bonus / salary
for person, data in data_dict.items():
    if data['salary'] == 'NaN' or data['bonus'] == 'NaN':
        data['bonus_rate'] = 'NaN'
    else:
        data['bonus_rate'] = float(data['bonus']) / float(data['salary'])

    if data['to_messages'] == 'NaN' or data['from_messages'] == 'NaN':
        data['poi_mail_rate'] = 'NaN'
    else:
        data['poi_mail_rate'] = float(data['from_poi_to_this_person']) / data['to_messages']
        data['poi_mail_rate'] += float(data['from_this_person_to_poi']) / data['from_messages']

### Store to my_dataset for easy export below.
my_dataset = data_dict

### Get a sense of the data
# print 'Entries: {}'.format(len(my_dataset.keys()))
# print 'POIs {}'.format(sum([x['poi'] for x in my_dataset.values()]))
print 'Features being Used: {}'.format(len(features_list)-1)
print 'Features: {}'.format(features_list)

# all_feature_names = data_dict.values()[0].keys()
# import matplotlib.pyplot as plt
# for feature in features_list:
#     try:
#         feature_data_poi = [x[feature] for x in data_dict.values() if x['poi'] == 1]
#         feature_data_poi = [x for x in feature_data_poi if x != 'NaN']
#         feature_data_reg = [x[feature] for x in data_dict.values() if x['poi'] == 0]
#         feature_data_reg = [x for x in feature_data_reg if x != 'NaN']
#         datapoints = len(feature_data_poi) + len(feature_data_reg)
#         poi_percent = float(len(feature_data_poi)) / datapoints
#         print '{}: \t{:.3f}    ({} of {})'.format(feature, poi_percent, len(feature_data_poi), datapoints)
#         plt.scatter(feature_data_reg, [1]*len(feature_data_reg), marker='+', alpha=.5)
#         plt.scatter(feature_data_poi, [1]*len(feature_data_poi), c='r', alpha=.5)
#         plt.title(feature)
#         plottxt = 'poi: {}, non-poi: {}'.format(len(feature_data_poi), len(feature_data_reg))
#         plt.text(0, 1.002, plottxt)
#         plt.show()
#     except ValueError:
#         print "Can't plot {}".format(feature)
#         plt.close()
#         continue

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a variety of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.
from sklearn.naive_bayes import GaussianNB
gNB = GaussianNB()

from sklearn import tree
split = 2
dtree = tree.DecisionTreeClassifier(min_samples_split=split)

from sklearn.ensemble import AdaBoostClassifier
estimators = 50
ada = AdaBoostClassifier(n_estimators=estimators)

algo = 'ada'

if algo == 'tree':
    clf = dtree
    print 'Decision Tree, min_split: {}'.format(split)
elif algo == 'gnb':
    clf = gNB
    print 'GaussianNB'
elif algo == 'ada':
    clf = ada
    print 'AdaBoost, n_estimators: {}'.format(estimators)


### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

from sklearn.cross_validation import train_test_split

total_predictions = 0
true_positives = 0
true_negatives = 0
false_positives = 0
false_negatives = 0

feature_importance = []

for i in range(200):
    features_train, features_test, labels_train, labels_test = \
        train_test_split(features, labels, test_size=0.3, random_state=i)

    clf.fit(features_train, labels_train)
    if algo == 'tree':
        feature_importance.append(tuple(dtree.feature_importances_))
    elif algo == 'ada':
        feature_importance.append(tuple(ada.feature_importances_))
    predictions = clf.predict(features_test)
    paired = zip(predictions, labels_test)

    total_predictions += len(predictions)

    true_positives += sum([1 for (p,t) in paired if (p,t)==(1,1)])
    true_negatives += sum([1 for (p,t) in paired if (p,t)==(0,0)])
    false_positives += sum([1 for (p,t) in paired if (p,t)==(1,0)])
    false_negatives += sum([1 for (p,t) in paired if (p,t)==(0,1)])

accuracy = float(true_positives + true_negatives) / total_predictions
precision = true_positives / float(true_positives + false_positives) if true_positives > 0 else 0
recall = true_positives / float(true_positives + false_negatives) if true_positives > 0 else 0

if algo == 'tree' or algo == 'ada':
    feature_importance = [sum(x)/len(x) for x in zip(*feature_importance)]
    feature_importance = zip(features_list[1:], feature_importance)
    for f in feature_importance:
        print '{}: {:.5f}'.format(f[0], f[1])

print 'Number of Predictions: {}'.format(total_predictions)
print 'Accuracy: {:.3f}    Precision: {:.3f}    Recall: {:.3f}'.format(accuracy, precision, recall)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)