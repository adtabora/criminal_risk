
import pandas as pd
import numpy as np


def extract_true_entities(words):
    data = []
    for index, row in words.iterrows():
        if row.iob_tag == "B-Loc":
            data.append([
                row.art_id,
                row.sent_id,
                row.cs_id,
                row.pos,
                row.word
            ])
        elif row.iob_tag == "I-Loc":
            if len(data) > 0:
                data[-1][4] += " " + row.word

    df = pd.DataFrame(data, columns=["art_id","sent_id","cs_id","pos","entity"])

    return df


def extract_identified_entities(features, preds, le_iob):
    preds = le_iob.inverse_transform(preds)
    features.loc[:,"pred"] = preds
    
    data = []
    for index, row in features.sort_values(by=["cs_id","pos"]).iterrows():
        if row.pred == "B-Loc":
            data.append([
                row.art_id,
                row.sent_id,
                row.cs_id,
                row.pos,
                row.word
            ])
        elif row.pred == "I-Loc":
            if len(data) > 0:
                data[-1][4] += " " + row.word

    df = pd.DataFrame(data, columns=["art_id","sent_id","cs_id","pos","entity"])

    return df


def score_entities(true, pred):

    # Find the true positives
    true_positive = 0
    for index, entity in pred.iterrows():
        result = true[(true["cs_id"] == entity.cs_id)
                      & (true["pos"] == entity.pos)
                      & (true["entity"] == entity.entity)
                     ]
        if len(result) > 0:
            true_positive += 1


    print "true positives: %i" %true_positive
    print "predicted positives: %i" % pred.shape[0]
    print "real positives: %i" % true.shape[0]
    
    precision = true_positive * 1.0 / pred.shape[0]
    print "precision: %0.4f" %precision
    recall = true_positive * 1.0 / true.shape[0]
    print "recall: %0.4f" %recall

    fscore = (precision + recall) / 2.0
    print "fscores: %0.4f" %fscore

    
    