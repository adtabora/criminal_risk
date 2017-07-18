import preprocess as process
import identifier
from  entities import extract_true_entities, extract_identified_entities, score_entities
import pandas as pd

from sklearn.preprocessing import LabelEncoder


def execute():
    # 1. Read 
    articles_df = pd.read_csv("../../files/pos_articles.csv")
    
    # 2.
    words_df = process.convertToWords(articles_df)

    # 3. train a label encoder for POS tags using the whole corpus
    le_tag = LabelEncoder()
    le_tag.fit(words_df.pos_tag.values.tolist() )
    # 4. Generate new features
    features_df, le_iob, _ = process.getFeatures(words_df.copy(), le_tag= le_tag)
    # 5. Convert to Entities
    entities_df = process.wordsToEntities(features_df)
    # 6. Split 
    entities_train, entities_test = process.splitTrainTest(entities_df)
    
    # 7. Transform to Word format
    features_train = process.entitiesToWords(entities_train,columns=features_df.columns)
    features_test = process.entitiesToWords(entities_test,columns=features_df.columns)

    

    #7.5 save features for testing purposes
    features_train.to_csv("../../files/ner_features_train.csv",index=False, encoding="utf-8")
    features_test.to_csv("../../files/ner_features_test.csv",index=False, encoding="utf-8")


    # 8. Train the identifier.
    labels = le_iob.classes_
    pred_train, pred_test, scores = identifier.train_identifier(features_train, features_test, labels)
    

 

    # 9. Score based on identified entities
    true_ent_train = extract_true_entities(features_train)
    true_ent_test = extract_true_entities(features_test)

    # print "true ent train shape %i" %true_ent_train.shape[0]
    # print "true ent test shape %i" %true_ent_test.shape[0]

    ident_ent_train = extract_identified_entities(features_train, pred_train, le_iob)
    ident_ent_test = extract_identified_entities(features_test, pred_test, le_iob)
    # print "ident ent train shape %i" %ident_ent_train.shape[0]
    # print "ident ent test shape %i" %ident_ent_test.shape[0]

    print "--- TRAIN SCORES ---"
    train_score = score_entities(true_ent_train, ident_ent_train)
    print
    print "--- TEST SCORES ---"
    test_score = score_entities(true_ent_test, ident_ent_test)
    print 

    scores["entity_score"] = {
        "train": train_score,
        "test": test_score
    }

    # 10. Save scores and results
    print "- Saving Scores"
    import json
    with open('../../files/identifier_scores.json', 'w') as file:
        json.dump(scores, file)

    
    print "- Saving Results"
    result_train = features_train
    # result_train.loc[:,"word"] =result_train.word.apply(lambda x: unicode(x,"utf8") )
    result_train.loc[:,"pred"] = le_iob.inverse_transform(pred_train)
    result_train.loc[:,"dataset"] = "train"

    result_test = features_test
    # result_test.loc[:,"word"] =result_test.word.apply(lambda x: unicode(x,"utf8") )
    result_test.loc[:,"pred"] = le_iob.inverse_transform(pred_test)
    result_test.loc[:,"dataset"] = "test"

    results_df = pd.concat([result_train, result_test])
    results_df.to_csv("../../files/words_classified.csv",index=False, encoding="utf-8")


    # Save entity results
    print "- Saving Entity Results"
    ident_ent_train.loc[:,"dataset"] = "train"
    ident_ent_test.loc[:,"dataset"] = "test"
    ident_ent = pd.concat([ident_ent_train, ident_ent_test])
    ident_ent.to_csv("../../files/entities.csv",index=False, encoding="utf-8")


