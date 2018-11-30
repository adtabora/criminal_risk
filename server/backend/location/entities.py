
import pandas as pd
import numpy as np


def extract_entities(words, io_column, geo_column):
    data = []
    last_artid = -1
    last_io = 1
    for index, row in words.iterrows():
        # if row[column][0] == "B":
        if (row[io_column]==0 and last_io == 1) or (row.art_id != last_artid and row[io_column]==0):
            data.append([
                row.art_id,
                row.sent_id,
                row.cs_id,
                row.pos,
                row.word,
                #correction of leaking
                #row.geo_type   
                row[geo_column]  #[2:]  
            ])
        # elif row[column][0] == "I":
        elif row[io_column]==0 and last_io == 0:
            if len(data) > 0:
                data[-1][4] += " " + row.word
        last_artid = row.art_id
        last_io = row[io_column]

    df = pd.DataFrame(data, columns=["art_id","sent_id","cs_id","pos","entity","geo_type"])

    return df


def score_entities(true, pred ):
    geo_types =["Country","State","City","Zone","Col","Bar"]

    data = []
    for geo_type in geo_types:
        # Find the true positives
        true_positive = 0
        for index, entity in pred[pred["geo_type"]==geo_type].iterrows():
            result = true[ (true["geo_type"] == geo_type)
                          & (true["cs_id"] == entity.cs_id)
                          & (true["pos"] == entity.pos)
                          & (true["entity"] == entity.entity)
                         ]
            if len(result) > 0:
                true_positive += 1

        support = true[true["geo_type"]==geo_type].shape[0]
        if true_positive == 0:
            precision =0.0
            recall = 0.0
            fscore = 0.0
        else:
            total_pos = pred[pred["geo_type"]==geo_type].shape[0]
            if total_pos == 0:
                precision = 0
            else:
                precision = true_positive * 1.0 / total_pos
            recall = true_positive * 1.0 / support
            fscore = (precision * recall)*2.0 / (precision + recall)
        data.append([geo_type,precision,recall,fscore,support ])

    scores_df = pd.DataFrame(data,columns=["geo_type","precision","recall","fscore","support"])

    support = scores_df["support"].sum() 
    if support == 0:
        f1_result = 0
        precision = 0
        recall = 0
    else:
        f1_result = (scores_df["fscore"] * scores_df["support"]).sum() / support
        precision = (scores_df["precision"] * scores_df["support"]).sum() / support
        recall = (scores_df["recall"] * scores_df["support"]).sum() / support
    
    scores_df = scores_df.append( pd.DataFrame([["Total",precision, recall, f1_result,support ]], columns=["geo_type","precision","recall","fscore","support"]) )

    return scores_df