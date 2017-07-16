
import pandas as pd
import numpy as np


def extract_true_entities(words):
    data = []
    for index, row in words.iterrows():
        if row.iob_tag[0] == "B":
            data.append([
                row.art_id,
                row.sent_id,
                row.cs_id,
                row.pos,
                row.word
            ])
        elif row.iob_tag[0] == "I":
            if len(data) > 0:
                data[-1][4] += " " + row.word

    df = pd.DataFrame(data, columns=["art_id","sent_id","cs_id","pos","entity"])

    return df


def extract_identified_entities(features, preds, le_iob):
    preds = le_iob.inverse_transform(preds)
    # 6.1 transform the preds
    last = "O"
    for idx, pred in enumerate(preds):
        if last == "B" and pred[0] == "B":
            preds[idx] = "I"
        last = pred[0]

    features.loc[:,"pred"] = preds
    
    data = []
    last_iob = "none"
    for index, row in features.sort_values(by=["cs_id","pos"]).iterrows():
        if row.pred[0] == "B":
            data.append([
                row.art_id,
                row.sent_id,
                row.cs_id,
                row.pos,
                row.word
            ])
        elif row.pred[0] == "I" and last_iob[0] in ["B", "I"]:
            if len(data) > 0:
                data[-1][4] += " " + row.word

        #this statement actually its taking an I-Loc as an B-Loc
        elif row.pred[0] == "I" and last_iob == "none":
            data.append([
                row.art_id,
                row.sent_id,
                row.cs_id,
                row.pos,
                row.word
            ])


        last_iob = row.pred


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

    return {
        "precision": precision,
        "recall": recall,
        "fscore": fscore
    }

    
    