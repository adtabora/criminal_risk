import preprocess as process
import identifier
from  entities import extract_entities, score_entities
import pandas as pd

import pickle

from sklearn.preprocessing import LabelEncoder


def execute():
    # 1. Read 
    articles_df = pd.read_csv("../../files/pos_articles.csv")
    #only use the articles for training
    articles_df = articles_df[articles_df["article_id"]<2000]

    # . Convert to Sentences
    sentences_df = process.convertToSentences(articles_df)
    # . Split
    sentences_train, sentences_test = process.splitTrainTest(sentences_df)
    # . convert to Words
    words_train = process.sentenecesToWords(sentences_train)
    words_test = process.sentenecesToWords(sentences_test)

    # . train a label encoder for POS tags using the whole corpus
    le_tag = LabelEncoder()
    le_tag.fit(words_train.pos_tag.values.tolist() +  words_test.pos_tag.values.tolist())
    # . Generate new features
    features_train, le_iob, _ = process.getFeatures(words_train.copy(), le_tag= le_tag)
    features_test, _, _ = process.getFeatures(words_test.copy(), le_tag= le_tag, le_iob=le_iob)


    #7.5 save features for testing purposes
    features_train.to_csv("../../files/ner_features_train.csv",index=False, encoding="utf-8")
    features_test.to_csv("../../files/ner_features_test.csv",index=False, encoding="utf-8")
    print "-- Features saved! --"

    # 8. Train the identifier.
    pred_train, pred_test, scores, final_model = identifier.train_identifier(features_train, features_test)
    

    # 9. Score based on identified entities
    print "-- extract entities --"
    print "-true identities"
    true_ent_train = extract_entities(features_train,"iob", "geo_type")
    true_ent_test = extract_entities(features_test ,"iob", "geo_type")
    

    print "true ent train shape %i" %true_ent_train.shape[0]
    print "true ent test shape %i" %true_ent_test.shape[0]
    print true_ent_test

    print "-pred identities"
    ident_ent_train = extract_entities(pred_train,"s_pred", "pred_geo")
    ident_ent_test = extract_entities(pred_test,"s_pred", "pred_geo")
    print "ident ent train shape %i" %ident_ent_train.shape[0]
    print "ident ent test shape %i" %ident_ent_test.shape[0]
    print ident_ent_test


    print "--- TRAIN SCORES ---"
    train_score = score_entities(true_ent_train, ident_ent_train)
    print train_score
    print 
    print "--- TEST SCORES ---"
    test_score = score_entities(true_ent_test, ident_ent_test)
    print test_score
    print 


    scores["entity_score"] = {
        "labels": train_score.geo_type.values.tolist(),
        "train": train_score.to_dict(orient='records'),
        "test": test_score.to_dict(orient='records')
    }

    

    # 10. Save scores and results
    print "- Saving Scores"
    import json
    with open('../../files/identifier_scores.json', 'w') as file:
        json.dump(scores, file)

    
    print "- Saving Results"
    # HAVE TO RETHINK THIS PART!
    # result_train = features_train
    # result_train.loc[:,"pred"] = pred_train
    # result_train.loc[:,"dataset"] = "train"

    # result_test = features_test
    # result_test.loc[:,"pred"] = pred_test
    # result_test.loc[:,"dataset"] = "test"

    # results_df = pd.concat([result_train, result_test])
    # results_df.to_csv("../../files/words_classified.csv",index=False, encoding="utf-8")


    # Save entity results
    print "- Saving Entity Results"
    ident_ent_train.loc[:,"dataset"] = "train"
    ident_ent_test.loc[:,"dataset"] = "test"
    ident_ent = pd.concat([ident_ent_train, ident_ent_test])
    ident_ent.to_csv("../../files/entities.csv",index=False, encoding="utf-8")

    print "- Saving final Model"
    final_model["le_tag"] = le_tag
    final_model["le_iob"] = le_iob
    pickle.dump( final_model, open( "../../models/NER_model.p", "wb" ) )



