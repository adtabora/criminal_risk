from classifiers import initialize_classifiers
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report, precision_recall_fscore_support



# formats in X and y
def getXY(df, dropColumns):
    X = df.drop(dropColumns, 1).values
    y = df.iob.values
    # print "-- iob counts --"
    # print df.iob.value_counts()
    return X, y

# add stacked features 
def add_stacked_feature(clf_ix, pos, df):
    preds = df["pred_"+str(clf_ix)].values.tolist()
    # decide column name
    if pos < 0:
        column = "pred" + str(clf_ix) + "_prev_" + str(-pos)
    elif pos > 0:
        column = "pred" + str(clf_ix) + "_next_" + str(pos)
    else:
        print "- ERROR: 0 value passed"
        return None
    # shift list
    df.loc[:,column ] = preds[pos:] + preds[:pos]
    # correct the values for the first words
    # if pos < 0:
    #     df.at[df[column] < -pos,column] = 1
   
    return df

# produces features from the predictions
def get_stacked_features(df, lvl_1_classifiers):
    for i in range(len(lvl_1_classifiers)):
        df = add_stacked_feature(i, -1, df)
        df = add_stacked_feature(i, -2, df)
        df = add_stacked_feature(i, 1, df)
        df = add_stacked_feature(i, 2, df)

    return df



# Very simple classifier that uses the gazetteer
def gazetteer_classify(df):
    preds = ((df["in_Country"] | df["in_State"] | df["in_City"]) & df["upper"]).apply(lambda x: int(not x)).tolist()
    return preds


def getOnlyB(df):
    temp_df = df.copy()
    temp_df.loc[:,"B"] = np.zeros(temp_df.shape[0])
    last = 1
    last_artid = -1
    for idx, word in temp_df.iterrows():        
        if ( last == 1 and word.s_pred == 0 ) or last_artid != word.art_id :
            temp_df.loc[idx,"B"] = 1
        last = word.s_pred
        last_artid = word.art_id
    
    return temp_df[temp_df["B"]==1].drop("B",1)

# TRAIN
def train_identifier(features_train, features_test):

    print "- format into X and y"
    desc_columns = ["art_id","sent_id", "cs_id","word", "iob_tag","iob" ,"geo_type"]
    X_train, y_train = getXY(features_train, desc_columns)
    X_test, y_test = getXY(features_test, desc_columns)
    print "- number of features: %i" %len(X_train[0])

    #Initialize classifiers
    lvl_1_classifiers, lv2_classifier, lv3_classifier = initialize_classifiers()

    print "- start processing classifiers"
    stack_features_train = features_train.copy()  #[desc_columns]
    stack_features_test = features_test.copy() #[desc_columns]
    lvl1_scores = []
    for index, clf in enumerate(lvl_1_classifiers):
        print "-- training classifier %i" %index
        # print np.bincount(y_train)
        clf.train(X_train, y_train, scores=True)
        print "-- predicting classifier %i" %index
        preds_train, preds_test, clf_score = clf.predict_score(X_train, y_train, X_test, y_test)
        lvl1_scores.append(clf_score)

        stack_features_train.loc[:,"pred_"+str(index)] = preds_train
        stack_features_test.loc[:,"pred_"+str(index)] = preds_test

    print "- producing stacked features"
    stack_features_train = get_stacked_features(stack_features_train, lvl_1_classifiers)
    stack_features_test = get_stacked_features(stack_features_test, lvl_1_classifiers)
    

    print "- format into X and y"
    # print stack_features_train.loc[0:10]
    X_train, y_train = getXY(stack_features_train, desc_columns)
    X_test, y_test = getXY(stack_features_test, desc_columns)

    print "- number of features: %i" %len(X_train[0])
    
    # print "--- DEBUG X_TRAIN ----"
    # print stack_features_train.columns
    # print desc_columns
    # print X_train
    # print y_train

    print "- training lvl2 classifier"
    lv2_classifier.train( X_train, y_train, scores=True)

    print "- predicting lv2"
    preds_train, preds_test, lv2_score = lv2_classifier.predict_score(X_train, y_train, X_test, y_test)


    # . Prepare to classify JUST the entities
    stack_features_train["s_pred"] = preds_train
    stack_features_test["s_pred"] = preds_test
    
    # cat_train = stack_features_train[stack_features_train["s_pred"]==0]
    # cat_test = stack_features_test[stack_features_test["s_pred"]==0]
    cat_train = getOnlyB(stack_features_train)
    cat_test = getOnlyB(stack_features_test)

    X_train = cat_train.drop(desc_columns, 1).values
    #small change now only classifying the geo type
    y_train = cat_train.iob_tag.apply(lambda x: x[2:]).values

    X_test = cat_test.drop(desc_columns, 1).values
    #small change now only classifying the geo type
    y_test = cat_test.iob_tag.apply(lambda x: x[2:]).values

    print "- training lvl3 classifier"
    lv3_classifier.train( X_train, y_train, scores=True)

    print "- predicting lv3"
    final_preds_train, final_preds_test, lv3_score = lv3_classifier.predict_score(X_train, y_train, X_test, y_test)

    geo_preds_train = pd.Series(final_preds_train, index = cat_train.index )
    geo_preds_test = pd.Series(final_preds_test, index = cat_test.index )

    final_train = stack_features_train.copy()
    final_test = stack_features_test.copy()

    final_train.loc[:,"pred_geo"] = geo_preds_train
    final_test.loc[:,"pred_geo"] = geo_preds_test


    #packing models
    final_model = {
        "lv1": lvl_1_classifiers,
        "lv2": lv2_classifier,
        "lv3": lv3_classifier
    }


        
    #return scores
    scores = {"lvl1": lvl1_scores, "lvl2":  lv2_score, "lvl3": lv3_score}

    return final_train, final_test , scores, final_model





