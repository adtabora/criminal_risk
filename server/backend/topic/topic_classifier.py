import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold

from text_classifiers import NBClassifier
from sklearn.metrics import precision_recall_fscore_support

import pickle



# Combines the predictions of many classifiers in preparation for stacking 
def combine_preds(df, classifiers):
    rows_num = df.shape[0]

    lvl1_preds =[ clf.predict(df, mode="proba") for clf in classifiers] 

    #create X combined of all the predictions
    X_combined = []
    for index in range(rows_num):
        row = []
        for preds in lvl1_preds:
            row.append(preds[index][0])
            row.append(preds[index][1])
        X_combined.append(row)

    return X_combined

def print_scores(clf, X, y):
    preds = clf.predict(X)
    precision, recall, fscore, support = \
        precision_recall_fscore_support(y, preds)

    print "precision %0.4f" %precision[1]
    print "recall %0.4f" %recall[1]
    print "fscore %0.4f" %fscore[1]
    print "support %0.4f" %support[1]

    return precision, recall, fscore, support, preds


# This is the main function
def execute():
    #1. Read data
    print "- reading documents csv"
    documents_df = pd.read_csv("../../files/documents.csv")

    #only use the train documents:
    documents_df = documents_df.ix[:1999]

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
        # Only Content Classifier
        NBClassifier(
            alpha=[0.5], #[1.0, 0.5, 0.1, 0.01, 0.001], 
            # content = { 
            #     "vectorizer":"count", "ngram":[5,5], "analyzer":'char_wb',
            #     "min":1, "max":0.3, "binary":True
            # }
            title = { 
                "vectorizer":"count", "ngram":[1,1], "analyzer":'word',
                "min":1, "max":.05, "binary":False
            }, 
        ),
         NBClassifier(
            alpha=[1.0, 0.5, 0.1, 0.01, 0.001], 
            # content = { 
            #     "vectorizer":"count", "ngram":[5,5], "analyzer":'char_wb',
            #     "min":1, "max":0.3, "binary":True
            # }
            title = { 
                "vectorizer":"count", "ngram":[4,5], "analyzer":'char_wb',
                "min":1, "max":0.3, "binary":False
            }, 
        ),
        # Title and Content Classifier
        NBClassifier(
            alpha=[0.1], #[1.0, 0.5, 0.1, 0.01, 0.001],
            title = { 
                "vectorizer":"count", "ngram":[5,5], "analyzer":'char_wb',
                "min":1, "max":0.9, "binary":True
            }, 
            content = { 
                "vectorizer":"count", "ngram":[5,5], "analyzer":'char_wb',
                "min":1, "max":0.9, "binary":True
            }
        ),
        #Only Content Classifier
        NBClassifier(
            alpha=[0.5], #[1.0, 0.5, 0.1, 0.01, 0.001], 
            content = { 
                "vectorizer":"count", "ngram":[4,5], "analyzer":'char_wb',
                "min":1, "max":0.3, "binary":True
            }
        ),
        # Title and Content Classifier
        NBClassifier(
            alpha=[0.1], #[1.0, 0.5, 0.1, 0.01, 0.001],
            title = { 
                "vectorizer":"count", "ngram":[3,3], "analyzer":'char_wb',
                "min":1, "max":0.9, "binary":True
            }, 
            content = { 
                "vectorizer":"count", "ngram":[3,3], "analyzer":'char_wb',
                "min":1, "max":0.9, "binary":True
            }
        ),
        #WORD 
        NBClassifier(
            alpha= [0.5], #[1.0, 0.5, 0.1, 0.01, 0.001], 
            content = { 
                "vectorizer":"count", "ngram":[1,1], "analyzer":'word',
                "min":1, "max":0.9, "binary":True
            }
        ),
        #Title and Content Classifier
        NBClassifier(
            alpha=[0.5], #[1.0, 0.5, 0.1, 0.01, 0.001],
            title = { 
                "vectorizer":"count", "ngram":[1,1], "analyzer":'word',
                "min":1, "max":0.9, "binary":True
            }, 
            content = { 
                "vectorizer":"count", "ngram":[1,1], "analyzer":'word',
                "min":1, "max":0.9, "binary":True
            }
        ),
        NBClassifier(
            alpha=[0.001], #[1.0, 0.5, 0.1, 0.01, 0.001], 
            content = { 
                "vectorizer":"count", "ngram":[-2,2], "analyzer":'word',
                "min":1, "max":0.3, "binary":True
            }
        ),
        #Title and Content Classifier
        NBClassifier(
            alpha=[0.001], #[1.0, 0.5, 0.1, 0.01, 0.001],
            title = { 
                "vectorizer":"count", "ngram":[-2,2], "analyzer":'word',
                "min":1, "max":1, "binary":False
            }, 
            content = { 
                "vectorizer":"count", "ngram":[-2,2], "analyzer":'word',
                "min":1, "max":0.3, "binary":False
            }
        ),

    ]
    #train and test each classifier. Each classifier will store the scores
    print "- Training Classifiers"
    for index, clf in enumerate(classifiers):
        print "--- classifier %i ---" %index
        clf.train_test(train_df, test_df)
        clf.print_scores()

    # 5. Stack the models

    # filter classifiers with low scores 
    # and store the one with the highest score
    max_score = 0.0 
    max_clf = None
    max_idx = -1
    print "- Filtering Classifiers"
    filtered_classifiers = []
    for index, clf in enumerate(classifiers):
        print "score"
        print clf.fscore["test"]

        if clf.fscore["test"] > max_score:
            max_idx = index
            max_score = clf.fscore["test"]
            max_clf = clf

        if clf.fscore["test"] >= 0.9:
            filtered_classifiers.append(clf)
        else:
            print "- Dropped classifier %i" %index
    
    # Prepare Stacked Data
    print "- Preparing Stacked Data"
    train_stacked = combine_preds(train_df, filtered_classifiers)
    test_stacked = combine_preds(test_df, filtered_classifiers)

    print "-- lens --"
    print len(train_stacked[0])
    print len(test_stacked[0])
    print test_stacked[0]

    train_labels = train_df.category.apply(lambda cat: int(cat=="Criminal")).values.tolist()
    test_labels = test_df.category.apply(lambda cat: int(cat=="Criminal")).values.tolist()

    # Stacking with Logistic Regression
    print "- Training Stacked Classifier"
    from sklearn.model_selection import GridSearchCV
    from sklearn.linear_model import LogisticRegression


    parameters = {"C":[10, 1.0, 0.1, 0.01]}
    lr_clf = LogisticRegression(penalty="l2", random_state=238, n_jobs=4, class_weight="balanced")

    clf = GridSearchCV(lr_clf, parameters)
    
    clf.fit(train_stacked, train_labels)

    
    # score the stacked model
    print "-- STACKED TRAIN SCORES --"
    print_scores(clf, train_stacked, train_labels)
    print "-- STACKED TEST SCORES --"
    precision, recall, fscore, support, _ = print_scores(clf, test_stacked, test_labels)


    # select the best classifier
    print 
    print "--- FINAL SCORES ---"
    if fscore[1] > max_score:
        print "- Stacked model selected"
        train_precision, train_recall, train_fscore, train_support, preds_train = print_scores(clf, train_stacked, train_labels)

        test_precision, test_recall, test_fscore, test_support, preds_test = print_scores(clf, test_stacked, test_labels)
    else:
        print "- Classifier %i selected" %max_idx
        train_precision, train_recall, train_fscore, train_support, preds_train = print_scores(max_clf, train_df, train_labels)
        test_precision, test_recall, test_fscore, test_support, preds_test = print_scores(max_clf, test_df, test_labels)


    # save model
    print 
    print "- Saving model for production."
    pickle.dump( max_clf, open( "../../models/topic_model.p", "wb" ) )

    # Save scores
    scores = {
        "lvl2" : {
            "train": [{
                "precision": train_precision[1],
                "recall": train_recall[1],
                "fscore": train_fscore[1],
                "support": train_support[1],
            }],
            "test": [{
                "precision": test_precision[1],
                "recall": test_recall[1],
                "fscore": test_fscore[1],
                "support": test_support[1],
            }]
        }
    }

    print "- Saving Scores"
    import json
    with open('../../files/topic_scores.json', 'w') as file:
        json.dump(scores, file)


    # Save the results
    print "- Saving results"
    results_df = pd.DataFrame({
        "art_id": train_df["id"].values.tolist() + test_df["id"].values.tolist(),
        "gold": train_df["category"].values.tolist() + test_df["category"].values.tolist(),
        "pred": preds_train.tolist() + preds_test.tolist(),
        "data_set": ["train" for i in range(train_df.shape[0])] +  ["test" for i in range(test_df.shape[0])] 
    })

    # format the predictions
    results_df.loc[:,"pred"] = results_df.pred.apply(lambda x: "Other" if x==0 else "Criminal")
    
    results_df.to_csv("../../files/documents_classified.csv",index=False)

    


