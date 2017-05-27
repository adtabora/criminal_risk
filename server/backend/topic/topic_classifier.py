import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold

from text_classifiers import NBClassifier
from sklearn.metrics import precision_recall_fscore_support


# Combines the predictions of many classifiers in preparation for stacking 
def combine_preds(df, classifiers):
    rows_num = df.shape[0]

    pred_log_probas =[ clf.predict_log_proba(df) for clf in classifiers] 

    #brute force create X combined of all the predictions
    X_combined = []
    for index in range(rows_num):
        row = []
        for preds in pred_log_probas:
            row.append(preds[index][0])
            row.append(preds[index][1])
        X_combined.append(row)

    return X_combined




# This is the main function
def execute():
    #1. Read data
    print "- reading documents csv"
    documents_df = pd.read_csv("../../files/documents.csv")

    #2. Preprocess data (eliminate nulls, eliminate ambiguous)
    print "- preprocess data"
    documents_df = documents_df[(documents_df.content.notnull() ) 
                            & (documents_df["category"]!="Criminal-Other")]

    #3. Split into Train and Test Sets
    print "- splitting into Train and Test Sets"
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=943)
    for train_index, test_index in skf.split(documents_df, documents_df.category.values): 
        train_df = documents_df.iloc[train_index]
        test_df = documents_df.iloc[test_index]
        break #since we only want to split them 

    # 4. Train a series of classifiers with different parameters.
    classifiers = [
        #Only Title Classifier
        # NBClassifier(
        #     alpha=  [0.1] #[1.0, 0.5, 0.1, 0.01, 0.001], 
        #     title = { 
        #         "vectorizer":"count", "ngram":[5,5], 
        #         "min":1, "max":1, "binary":True
        #     }
        # ),
        #Only Content Classifier
        NBClassifier(
            alpha=[0.5], #[1.0, 0.5, 0.1, 0.01, 0.001], 
            content = { 
                "vectorizer":"count", "ngram":[5,5], 
                "min":1, "max":0.3, "binary":True
            }
        ),
        #Title and Content Classifier
        NBClassifier(
            alpha=[0.1], #[1.0, 0.5, 0.1, 0.01, 0.001],
            title = { 
                "vectorizer":"count", "ngram":[5,5], 
                "min":1, "max":0.9, "binary":True
            }, 
            content = { 
                "vectorizer":"count", "ngram":[5,5], 
                "min":1, "max":0.9, "binary":True
            }
        ),
    ]
    #train and test each classifier. Each classifier will store the scores
    print "- Training Classifiers"
    for index, clf in enumerate(classifiers):
        print "--- classifier %i ---" %index
        clf.train_test(train_df, test_df)
        clf.print_scores()

    # 5. Do a stacking or voting

    # filter classifiers with low scores
    print "- Filtering Classifiers"
    filtered_classifiers = []
    for index, clf in enumerate(classifiers):
        
        if clf.fscore["test"] >= 0.4:
            filtered_classifiers.append(clf)
        else:
            print "- Dropped classifier %i" %index
    
    # Prepare Stacked Data
    print "- Preparing Stacked Data"
    train_stacked = combine_preds(train_df, filtered_classifiers)
    test_stacked = combine_preds(test_df, filtered_classifiers)
    train_labels = train_df.category.apply(lambda cat: int(cat=="Criminal")).values.tolist()
    test_labels = test_df.category.apply(lambda cat: int(cat=="Criminal")).values.tolist()

    # Stacking with Random Forest
    print "- Training Stacked Classifier"
    from sklearn.model_selection import GridSearchCV
    from sklearn.ensemble import RandomForestClassifier
    parameters = {'max_depth':[3,4,6,10,15,20,30], "n_estimators": [100,200]}
    rf_clf = RandomForestClassifier()
    clf = GridSearchCV(rf_clf, parameters)
    
    clf.fit(train_stacked, train_labels)

    

    print 
    print "--- FINAL SCORES ---"
    print
    print "-- TRAIN SCORES --"
    stacked_preds = clf.predict(train_stacked)
    train_precision, train_recall, train_fscore, train_support =  precision_recall_fscore_support(train_labels,stacked_preds)
    print "precision %0.4f" %train_precision[1]
    print "recall %0.4f" %train_recall[1]
    print "fscore %0.4f" %train_fscore[1]
    print "support %0.4f" %train_support[1]
    print
    print "-- TEST SCORES --"
    stacked_preds = clf.predict(test_stacked)
    precision, recall, fscore, support =  precision_recall_fscore_support(test_labels,stacked_preds)
    print "precision %0.4f" %precision[1]
    print "recall %0.4f" %recall[1]
    print "fscore %0.4f" %fscore[1]
    print "support %0.4f" %support[1]

    scores = {
        "lvl2" : {
            "train": [{
                "precision": train_precision[1],
                "recall": train_recall[1],
                "fscore": train_fscore[1],
                "support": train_support[1],
            }],
            "test": [{
                "precision": precision[1],
                "recall": recall[1],
                "fscore": fscore[1],
                "support": support[1],
            }]
        }
    }

    # Save results
    print "- Saving Results"
    import json
    with open('../../files/topic_scores.json', 'w') as file:
        json.dump(scores, file)

    


