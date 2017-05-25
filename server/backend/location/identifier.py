from classifiers import initialize_classifiers




# formats in X and y
def getXY(df, dropColumns):
    X = df.drop(dropColumns, 1).values
    y = df.iob_tag.values
    # print "-- iob counts --"
    # print df.iob_tag.value_counts()
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
    if pos < 0:
        df.at[df[column] < -pos,column] = 2
   
    return df

# produces features from the predictions
def get_stacked_features(df, lvl_1_classifiers):
    for i in range(len(lvl_1_classifiers)):
        df = add_stacked_feature(i, -1, df)
        df = add_stacked_feature(i, -2, df)
        df = add_stacked_feature(i, 1, df)
        df = add_stacked_feature(i, 2, df)

    return df





# TRAIN
def train_identifier(features_train, features_test):
    print "- format into X and y"
    desc_columns = ["art_id","sent_id", "cs_id","word", "iob_tag"]
    X_train, y_train = getXY(features_train, desc_columns)
    X_test, y_test = getXY(features_test, desc_columns)

    #Initialize classifiers
    lvl_1_classifiers, lv2_classifier = initialize_classifiers()

    print "- start processing classifiers"
    lvl1_scores = []
    for index, clf in enumerate(lvl_1_classifiers):
        print "-- training classifier %i" %index
        clf.train(X_train, y_train, scores=True)
        print "-- predicting classifier %i" %index
        preds_train, preds_test, clf_score = clf.predict_score(X_train, y_train, X_test, y_test)
        lvl1_scores.append(clf_score)

        features_train.loc[:,"pred_"+str(index)] = preds_train
        features_test.loc[:,"pred_"+str(index)] = preds_test

    print "- producing stacked features"
    features_train = get_stacked_features(features_train, lvl_1_classifiers)
    features_test = get_stacked_features(features_test, lvl_1_classifiers)

    print "- format into X and y"
    X_train, y_train = getXY(features_train, desc_columns)
    X_test, y_test = getXY(features_test, desc_columns)
    

    print "- training lvl2 classifier"
    lv2_classifier.train( X_train, y_train, scores=True)

    print "- predicting lv2"
    preds_train, preds_test, lv2_score = lv2_classifier.predict_score(X_train, y_train, X_test, y_test)

    
        
    #return scores
    scores = {"lvl1": lvl1_scores, "lvl2":  lv2_score}

    return preds_train, preds_test, scores



