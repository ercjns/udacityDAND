#!/usr/bin/python

""" 
    Starter code for exploring the Enron dataset (emails + finances);
    loads up the dataset (pickled dict of dicts).

    The dataset has the form:
    enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

    {features_dict} is a dictionary of features associated with that person.
    You should explore features_dict as part of the mini-project,
    but here's an example to get you started:

    enron_data["SKILLING JEFFREY K"]["bonus"] = 5600000
    
"""

import pickle

enron_data = pickle.load(open("../final_project/final_project_dataset.pkl", "r"))

# # how many people?
# print 'Keys (people):{}'.format(len(enron_data.keys()))

# # how many features per person?
# print 'Features: {}'.format(len(enron_data[enron_data.keys()[0]]))
# # for x in enron_data[enron_data.keys()[0]].keys():
#     # print 'Feature key: {}'.format(x)

# # how many POI in the dataset?
# print 'POIs: {}'.format(len([x["poi"] for x in enron_data.values() if x['poi']==1]))

# # value of stock belonging to James Prentice?
# print 'Stock: {}'.format(enron_data['PRENTICE JAMES']['total_stock_value'])

# # emails from Wesley Colwell to poi
# print 'Emails to POI: {}'.format(enron_data['COLWELL WESLEY']['from_this_person_to_poi'])

# # value of stock options exercised by Jeffrey K Skilling?
# print 'Options: {}'.format(enron_data['SKILLING JEFFREY K']['exercised_stock_options'])

# # who got the money?
# top_dogs = ['SKILLING JEFFREY K','LAY KENNETH L','FASTOW ANDREW S']
# max_pay = 0
# who = ''
# for x in top_dogs:
#     pay = enron_data[x]['total_payments']
#     if pay > max_pay:
#         max_pay = pay
#         who = x
# print who, max_pay

# # how many in the dataset have a quantified salary?
# print 'Known Salary: {}'.format(len([1 for x in enron_data.values() if x['salary'] != 'NaN']))
# print 'Known Email: {}'.format(len([1 for x in enron_data.values() if x['email_address'] != 'NaN']))

# unknown total payments?
unknown_payments = [x for x in enron_data.values() if x['total_payments'] == 'NaN']
print len(unknown_payments)
print 'Unknown Payments: {:.3f}'.format(len(unknown_payments)/146.0)
from_poi = [x for x in unknown_payments if x['poi'] == 1]
print len(from_poi)
print 'Unknown Payments from POI: {:.3f}'.format(len(from_poi)/18.0)