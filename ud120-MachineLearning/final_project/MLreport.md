# Detecting Persons of Interest in the Enron dataset
*Eric Jones, September 2017*

This report accompanies the Machine Learning project in the Udacity Data Analyst Nanodegree program by answering the questions posted [here](https://docs.google.com/document/d/1NDgi1PrNJP7WTbfSUuRUnz8yzs5nGVTSzpO7oeNTEWA/pub?embedded=true).

### 1. Summarize for us the goal of this project and how machine learning is useful in trying to accomplish it. As part of your answer, give some background on the dataset and how it can be used to answer the project question. Were there any outliers in the data when you got it, and how did you handle those?
The collapse of Enron is one of the largest business scandals of modern history - more detail [here](https://en.wikipedia.org/wiki/Enron_scandal). The goal of this project is to experiment with Machine Learning algorithms in an attempt to detect possible Persons of Interest (POIs) from a dataset containing financial information and emails from Enron employees and contractors. Machine learning can help here because there are a number of different inputs that individually do not point out a clear story, but ML can process different combinations of these data points and hopefully find some trends that may be able to point out individuals worthy of a closer investigation based on a combination of factors.

Before diving in, it's a good idea to get a more detailed idea of the data available. The provided dataset has information about 146 individuals with up to 22 features for each individual, though not all individuals have data for every feature. The dataset also already includes a `poi` feature which is a simple boolean classification for which of these individuals have already been identified as persons of interest: there are 18. Without this pre-classification, the dataset would probably be too small to work with. Additionally, when picking features to use in the ML classifier, I'll be sure to pick features which have data from both `poi:true` and `poi:false` individuals or else the feature is likely to throw off the classifier. 

There is one outlier I removed: the financial data was scraped from a spreadsheet and mistakenly scraped the `TOTAL` column and recorded that as another individual. At this point, I'm also going to remove two other datapoints: `LOCKHART EUGENE E` has no reported data other than `POI:False` which doesn't help us, and `THE TRAVEL AGENCY IN THE PARK` appears to not be a person, so I'm skeptical of including it as I'd expect an agency to have different characteristics than a person. That leaves me with 143 individuals in the dataset.

### 2. What features did you end up using in your POI identifier, and what selection process did you use to pick them? Did you have to do any scaling? Why or why not? As part of the assignment, you should attempt to engineer your own feature that does not come ready-made in the dataset -- explain what feature you tried to make, and the rationale behind it.
I used the `exercised_stock_options`, `bonus`, and `expenses`, and `other` in my POI identifier. Because there are few features (19) and a very small number of data points (145), I wanted to use only a few features, if possible, in order to combat possible overfitting due to trying to match too many feature characteristics. To narrow down the list, I first took advantage of the fact that the data is already labeled, and removed features which did not include a representative split of the data for that specific feature, or for which there were simply too few data points for me to feel confident including that feature in the classifier.

For example, the labeled data identifies 18 POIs within the 143 points, or about 12.5% POI. I discarded `deferred_income` because with 11 of 49 features, the 22% POI rate was too far from the actual data. Similarly, I discarded `director_fees` because in addition to only having this data for 17 of the people in the data set, *none* of them are identified as POIs. I also discarded `loan_advances` (1 POI of 4) and `restricted_stock_deferred` (0 POI of 18) at this step. 

With these 15 features, I figured I'd try a simple decision tree classifier to see where I stand. Looking at the feature importances for this decision tree, four features account for over 50% of the variation, and there's a drop off in individual feature importance after those four so I'll try again with just those features. Using just `bonus`, `expenses`, `exercised_stock_options`, and `other` in a decision tree actually does quite well: Accuracy: 0.827, Precision: 0.357, Recall: 0.351.

##### Decision Tree (15 Features)
`Accuracy: 0.804     Precision: 0.236     Recall: 0.263`

| Feature | Importance |
| ------- | ---------- |
| salary | 0.03971 |
| deferral_payments | 0.00766 |
| total_payments | 0.06904 |
| **bonus** | 0.15360 |
| total_stock_value | 0.07143 |
| **expenses** | 0.11450 |
| **exercised_stock_options** | 0.12682 |
| **other** | 0.11401 |
| long_term_incentive | 0.04422 |
| restricted_stock | 0.05155 |
| to_messages | 0.02743 |
| from_poi_to_this_person | 0.03884 |
| from_messages | 0.03756 |
| from_this_person_to_poi | 0.05552 |
| shared_receipt_with_poi | 0.04811 |

##### Decision Tree (4 Features)
`Accuracy: 0.827    Precision: 0.357    Recall: 0.351`

| Feature | Importance |
| ------- | ---------- |
| bonus | 0.26898 |
| expenses | 0.23925 |
| exercised_stock_options | 0.24448 |
| other | 0.24730 |

Because I'm using a decision tree classifier to predict categories and am not doing regression, I did not do any scaling, as it's not necessary in this type of classifier.

One thing I noticed here is that I now have no features from the email data in my classifier, which concerns me a little. I tried combining these features into one that I'll call `POI_mail_rate` that attempts to capture if an individual emails with POI more than might be expected. I'll define this feature as: `(from POI to this person / to_messages) PLUS (from this person to POI / from_messages)` so it's not really a rate and can be over 1, but the actual values matter less than if it separates the field well. Adding this feature in appeared to drop the performance slightly, but not significantly, and it did better than adding any other single email feature, though this may be a scenario where PCA on email features is the correct approach.

##### Decision Tree (5 Features)
`Accuracy: 0.821    Precision: 0.322    Recall: 0.343`

| Feature | Importance |
| ------- | ---------- |
| bonus | 0.19102 |
| expenses | 0.18387 |
| exercised_stock_options | 0.20096 |
| other | 0.19682 |
| poi_mail_rate | 0.22733 |


### 3. What algorithm did you end up using? What other one(s) did you try? How did model performance differ between algorithms?
After selecting the four or five features I wanted to use, I tried three different algorithms, and ultimately found the best performance with AdaBoost. A simple decision tree was extremely fast compared to the others, but AdaBoost provided slightly better results than the decision tree. This makes sense, as AdaBoost computes a decision tree many times, with each iteration giving more weight to miss-classified points in order to find a better overall classification. The GaussianNB classifier had high accuracy and precision, but much lower recall. Worth noting is that the AdaBoost Classifier took noticeably longer to run (seconds vs instantly) than either of the other algorithms I tried.

```python
Features: (4) ['bonus', 'expenses', 'exercised_stock_options', 'other']

GaussianNB
Accuracy: 0.857    Precision: 0.452    Recall: 0.285

Decision Tree, min_split: 2
Accuracy: 0.825    Precision: 0.353    Recall: 0.349

AdaBoost, n_estimators: 50
Accuracy: 0.851    Precision: 0.436    Recall: 0.338
```

```python
Features: (5) ['bonus', 'expenses', 'exercised_stock_options', 'other', 'poi_mail_rate']

GaussianNB
Accuracy: 0.864    Precision: 0.460    Recall: 0.288

DecisionTree, min_split: 2
Accuracy: 0.821    Precision: 0.326    Recall: 0.352

AdaBoost n_estimators=50
Accuracy: 0.856    Precision: 0.434    Recall: 0.355
```


### 4. What does it mean to tune the parameters of an algorithm, and what can happen if you don’t do this well?  How did you tune the parameters of your particular algorithm? What parameters did you tune?
Parameter tuning is an important part of machine learning as it can affect the performance of a given algorithm. The goal of parameter tuning is to best overcome the weaknesses of an algorithm, given the dataset. For example, if you're working on a classification problem such as this project, the algorithm may have parameters that dictate a threshold for when to split a set of similar points into different classes (or not). For some datasets, it may be best for the algorithm to drill deeply into specific data points, while for other problems it may be better to keep larger groups together, even with some potentially mixed data. Parameter tuning also can affect the speed at which an algorithm can finish, such as when dictating a number of iterations for the algorithm to complete. Especially on large datasets, time to complete may be an important factor to consider when choosing and tuning an algorithm. 

Simple tuning can be achieved by hand, by methodically testing different values and observing if and how the speed and performance change. Tuning can also be done in code with functions like GridSearch or RandomizedSearch, which can help to optimize many parameters at once or search over a wider range more quickly than by hand. Poor tuning can lead to a number of issues. The most obvious is that the default tuning is rarely the best for a given ML problem, so the performance will likely suffer if no tuning occurs. On the flip side, optimizing parameters to a training set can lead to over-fitting when the training and testing sets are not picked in a way that makes sense for the problem and available data.

My final algorithm uses an AdaBoost classifier, which is based on a decision tree. AdaBoost runs many iterations of a decision tree, with it's own strategy for weighting different points in order to improve the classifier. AdaBoost's tuning is primarily for a speed / accuracy tradeoff: the `n_estimators` parameter tells AdaBoost how many iterations to run before stopping. Higher values can provide better accuracy (to a point), but slow down execution. I tried running AdaBoost with `n_estimators` set at 10, 25, 50, 100, and 250, and found that performance didn't improve much past `n_estimators = 50`.

```python
AdaBoost, n_estimators: 5
Accuracy: 0.849    Precision: 0.406    Recall: 0.253

AdaBoost, n_estimators: 10
Accuracy: 0.848    Precision: 0.413    Recall: 0.300

AdaBoost, n_estimators: 25
Accuracy: 0.849    Precision: 0.424    Recall: 0.334

AdaBoost, n_estimators: 50
Accuracy: 0.851    Precision: 0.435    Recall: 0.339

AdaBoost, n_estimators: 100
Accuracy: 0.850    Precision: 0.432    Recall: 0.340

AdaBoost, n_estimators: 250
Accuracy: 0.851    Precision: 0.434    Recall: 0.340
```

While evaluating algorithms, I also tried tuning the simple decision tree. There are parameters that can change the number of splits, size required for a split to be made, and other characteristics of the algorithm. Poor tuning of a decision tree can lead to overfitting, such as when a tree creates a region that contains just a single data point, which may in fact be an outlier rather than representative of the data. I tried different values for `min_samples_split`, but with only 145 data points and 18 known POIs, found that `min_samples_split = 2`, the default, was best. Accuracy and Precision remained similar for all tested values, but Recall dropped:

```python
Decision Tree, min_samples_split: 2
Accuracy: 0.821    Precision: 0.323    Recall: 0.348

Decision Tree, min_samples_split: 3
Accuracy: 0.824    Precision: 0.326    Recall: 0.332

Decision Tree, min_samples_split: 5
Accuracy: 0.826    Precision: 0.324    Recall: 0.312

Decision Tree, min_samples_split: 10
Accuracy: 0.827    Precision: 0.312    Recall: 0.279
```


### 5. What is validation, and what’s a classic mistake you can make if you do it wrong? How did you validate your analysis?
In machine learning, validation is the process of testing a model against data that was not used during training, and evaluating the results. The critical step is that the test/validation data must be different than the data that is used to train the model. Without holding data separate for testing, it's near impossible to determine if the model is overfit, and therefore not applicable to new data.

Because of the small amount of data available for this analysis, I validated my model by creating a training and testing split, collecting the results, repeating with a different split of the same data, and then aggregating the validation results.


### 6. Give at least 2 evaluation metrics and your average performance for each of them.  Explain an interpretation of your metrics that says something human-understandable about your algorithm’s performance.

To evaluate the algorithms, I measured Accuracy, Precision, and Recall. Accuracy is the easiest to understand - it is simply the ratio of correct predictions that the algorithm makes on testing data once it has been trained. My algorithm has an accuracy of about 85%, meaning that for a given set of factors (one data point) that is known to represent a POI or known to not represent a POI, the algorithm correctly classifies it 85% of the time.

Precision and Recall are measurements that begin to explain what the algorithm might be doing in the cases where the classification is incorrect. 

I'll use a fictitious disease named *koupht* in a population of *Beelians* as an analogy. Let's say 10% of *Beelians* have *koupht*, and I've discovered a test that can detect the disease. I claim that my test is 95% accurate. That means that 19 out of 20 times, my test will correctly identify if a *Beelian* does or does not have *koupht*. But what about those other 5% of the tests? There are two cases: (a) some of these people have *koupht* but my test reported they are healthy so they are not given treatment even though they need it (statisticians call this set `false negatives`), and (b) some of these people are healthy, but were reported to have *koupht* and were subjected to unnecessary treatment (statisticians call this set `false positives`).

Precision explains how often moving on to treatment is the correct choice; precision drops when treatment is assigned to *Beelians* who are healthy and don't require it. (when there are many `false positives`)

Recall explains how often the test failed to identify the disease; recall drops when *Beelians* who should have received treatment instead have their *koupht* go undetected. (when there are many `false negatives`)

Depending on the real world situation, precision, recall, or both may be important. In the example, factors such as how harmful the disease is, how fast the disease spreads, and how expensive or invasive the treatment is all affect where I might want to focus on improving the test.

Bringing this back to the Enron dataset and identifying new POIs, I'm going to assume that I don't need to further investigate the POIs which have already been identified. Given that, while I want good accuracy, I don't care too much about recall because poor recall represents people my algorithm missed as POIs but who have already been investigated. On the other hand, I'd like precision to be high, but not too high. The datapoints which bring down the precision score are the exact points I'm looking for: they represent people my algorithm thinks are POIs, but were not previously identified as POIs. This gives me a great place to start further investigation to possibly identify more POIs, which was the original goal.
