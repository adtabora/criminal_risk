import preprocess as process
import identifier
from  entities import extract_true_entities, extract_identified_entities, score_entities
import pandas as pd

from sklearn.preprocessing import LabelEncoder


def execute_identifier():
    # read 
    articles_df = pd.read_csv("../../files/pos_articles.csv")
    sentences_df = process.convertToSentences(articles_df)

    # print sentences_df.head()

    sent_train, sent_test = process.splitTrainTest(sentences_df)

    words_train = process.convertToWords(sent_train)
    words_test = process.convertToWords(sent_test)

    # print words_train.loc[30:80]


    #train a label encoder for tags using the whole corpus
    le_tag = LabelEncoder()
    le_tag.fit(words_train.pos_tag.values.tolist() + words_test.pos_tag.values.tolist())

    features_train, le_iob, _ = process.getFeatures(words_train.copy(), le_tag= le_tag)
    features_test, _,_ = process.getFeatures(words_test.copy(), le_iob, le_tag)

    pred_train, pred_test, scores = identifier.train_identifier(features_train, features_test)


    # Score based on identified entities
    true_ent_train = extract_true_entities(words_train)
    true_ent_test = extract_true_entities(words_test)

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

    # Save scores
    print "- Saving Scores"
    import json
    with open('../../files/identifier_scores.json', 'w') as file:
        json.dump(scores, file)

    # Save results
    print "- Saving Results"

    result_train = words_train
    # result_train.loc[:,"word"] =result_train.word.apply(lambda x: unicode(x,"utf8") )
    result_train.loc[:,"pred"] = le_iob.inverse_transform(pred_train)
    result_train.loc[:,"dataset"] = "train"

    result_test = words_test
    # result_test.loc[:,"word"] =result_test.word.apply(lambda x: unicode(x,"utf8") )
    result_test.loc[:,"pred"] = le_iob.inverse_transform(pred_test)
    result_test.loc[:,"dataset"] = "test"

    results_df = pd.concat([result_train, result_test])
    results_df.to_csv("../../files/words_classified.csv",index=False, encoding="utf-8")


