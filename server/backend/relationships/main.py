import pandas as pd
import ast 

from preprocess import to_ascii, sent_to_ascii, rel_to_ascii, \
getEntitydf, getPairs, getFeatures, getEntities, format_relationship_tags

from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import f1_score, make_scorer, classification_report, precision_recall_fscore_support
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold

import pickle

def process_data(articles):
    # convert string into array
    articles.loc[:,"title"] = articles.title.apply(lambda x: ast.literal_eval(x) )
    articles.loc[:,"content"] = articles.content.apply(lambda x: ast.literal_eval(x) )
    articles.loc[:,"relationships"] = articles.relationships.apply(lambda x: ast.literal_eval(x) )
    #convert to ascii
    articles.title = articles.title.apply(lambda x: sent_to_ascii([x]) if x != None else x )
    articles.content = articles.content.apply(lambda x: sent_to_ascii(x) if x != None else x )
    articles.relationships = articles.relationships.apply(lambda x: rel_to_ascii(x) if x != None else x )

    # get all the full text
    articles.loc[:,"full_text"] = articles.title.apply(lambda x: x) + articles.content 

    articles.loc[:,"entities"] = articles.full_text.apply(lambda x: getEntities(x))

    articles.relationships.apply(lambda x: format_relationship_tags(x))

    relationships = pd.DataFrame()
    for _, article in articles.iterrows():
        if len(article.relationships) == 0:
            continue
        # get entities distance in the article
        entity_df = getEntitydf(article)
        # generate possible relationship pairs
        relations_df = getPairs(article)
        # generate features
        features_df = getFeatures(relations_df,entity_df)
        features_df.loc[:,"art_id"] = article.article_id
        # append the relationships to the final dataframe
        relationships = pd.concat([relationships,features_df])
    
    print "relationships size %i,%i"%(relationships.shape)
    return relationships

def get_X(df, desc_columns):
    le_ctag = LabelEncoder()
    le_ptag = LabelEncoder()
    le_reltyp = LabelEncoder()
    #encode c_tag and p_tag
    df.loc[:,"c_tag"] = le_ctag.fit_transform(df.c_tag)
    df.loc[:,"p_tag"] = le_ptag.fit_transform(df.p_tag)
    df.loc[:,"rel_type"] = le_reltyp.fit_transform(df.rel_type)

    labelers = {
        "le_ctag": le_ctag,
        "le_ptag": le_ptag,
        "le_reltyp": le_reltyp
    }
    return df.drop(desc_columns,1).values, labelers

#trains a model and scores it
def train_score(model, params, X_train, y_train, X_test, y_test,labels=[1]):
    f_one_scorer = make_scorer(f1_score,labels=labels, average="weighted")
    clf = GridSearchCV(model, params, cv=5, scoring= f_one_scorer, verbose=1, n_jobs=4 )
    clf.fit(X_train, y_train)

    print clf.best_score_
    print clf.best_params_
    print clf.cv_results_['mean_train_score']
    print clf.cv_results_['mean_test_score']
        
    print "- Train Results -"
    preds_train = clf.predict(X_train)

    print classification_report(y_train, preds_train )
    
    print "- Test Results -"
    preds_test = clf.predict(X_test)
    print classification_report(y_test, preds_test)
    
    return clf, preds_train, preds_test


 
def score_classifier(df):
    rel_types = [
        ["State-Country"], 
        ["City-Country"], 
        ["City-State"], 
        ["Zone-Country","Col-Country","Bar-Country","Res-Country"],
        ["Zone-State","Col-State","Bar-State","Res-State"],
        ["Zone-City","Col-City","Bar-City","Res-City"],
    ]

    data = []
    
    for rel_type in rel_types:
        #get all labels of the rel_type
        true_values = df[df["rel_type"].isin(rel_type)].label.values
        preds =  df[df["rel_type"].isin(rel_type)].pred.values
        score =  precision_recall_fscore_support(true_values, preds, average="binary", pos_label=1)
        data.append({
            "precision": score[0],
            "recall": score[1],
            "fscore": score[2],
            "support":  true_values.sum()   #score[3],
        })
  
    return data
    


def execute():
    # 1. Read CSV
    print "- Read CSV"
    articles = pd.read_csv("../../files/criminal_articles.csv")
    # only use train articles
    articles = articles[articles["article_id"]<2000]

    # 2. Preprocess Data and convert from article datafram to a relationship dataframe
    print "- Preprocess Data"
    relationships = process_data(articles)

    #descriptor columns
    desc_columns = [ 'art_id', 'c_word', 'p_word', 'child', 'parent', 'distances', 'label']
    X, labelers = get_X(relationships.copy(), desc_columns)
    y = relationships.label.values

    # 3. Split the data
    print "- Split the data"
    skf = StratifiedKFold(n_splits=5,shuffle=True, random_state= 773 )
    for train_index, test_index in skf.split( X, y):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        break

    # 4. Train/Test Classifier
    print "- Train the classifier"
    parameters = {
        "n_estimators": [200],
        "max_depth": [8], # [3,4,5,8,10,20],
        "min_samples_split" : [ 4], #[4,8,10,20,40],
        "max_features": [.3], # [.8,.5,.3,.1]
    }
    rfc = RandomForestClassifier(random_state= 233, n_jobs=4)

    clf, preds_train, preds_test = train_score(rfc, parameters, X_train, y_train, X_test, y_test)   

    # 5. Score the model by each relationship category
    print "- Score the model"

    # train
    train_relationships = relationships.reset_index(drop=True).ix[train_index]
    train_relationships.loc[:,"pred"] = preds_train
    train_scores = score_classifier(train_relationships)

    # train
    test_relationships = relationships.reset_index(drop=True).ix[test_index]
    test_relationships.loc[:,"pred"] = preds_test
    test_scores = score_classifier(test_relationships)

    labels = [
        "State-Country", "City-Country", "City-State", 
        "Zones-Country", "Zones-State","Zones-City"
    ]
    scores = {
        "labels" : labels,
        "train": train_scores,
        "test": test_scores
    }

    # 6. Save Scores
    print "- Saving Scores"
    import json
    with open('../../files/relationships_scores.json', 'w') as file:
        json.dump(scores, file)

    print "- Saving Model"
    rel_model = {
        "model": clf,
        "labelers": labelers
    }
    pickle.dump( rel_model, open( "../../models/rel_model.p", "wb" ) )
