from features import extract_classif_features
import classifier

from nltk.corpus import  conll2002
import pandas as pd
import pickle




#This function train a NE classifier. Given identified NE, it assigns a label.
# TODO: Labels:  LOC, etc..
def train_classifier():
    #1. prepare data
    print "-- Prepare Data"
    train_sentences = conll2002.iob_sents('esp.train')
    test_sentences = conll2002.iob_sents('esp.testa')
    
    #2. extract features
    train_df, test_df = extract_classif_features(train_sentences, test_sentences)
    #3. train     
    clf = classifier.train(train_df, test_df)
    

def tag_articles():

    print "- read NE tagged words csv"
    #1. prepare data
    article_df = pd.read_json("./files/NE_words.json")    
    article_df = article_df[article_df[ "sentence"]<=2]  #just for testing purposes
    
    #2. extract features
    feature_df, words_df = extract_classif_features(article_df)
    #3. predict
    preds = classifier.predict(feature_df)
    
    #print words_df.head(40)#just for testing purposes
    print "- saving result to json"
    words_df.loc[:,"iob"] = preds 

    #read iob labeler
    le_iob = pickle.load( open( "./files/iob_tag_encoder.p", "rb" ) )
    print le_iob.classes_
    # print le_iob.classes_
    words_df.loc[:,"iob"] = le_iob.inverse_transform(words_df.iob)
    words_df.to_json("./files/iob_words.json")

    print words_df

    print "- Done."

    


