from features import extract_ident_features
import identifier

from nltk.corpus import  conll2002
import pandas as pd
import ast 




#This function train a NE identifier. It only assigns 1 if it identifies a NE word.
def train_identifier():
    #1. prepare data
    print "-- Prepare Data"
    train_sentences = conll2002.iob_sents('esp.train')
    test_sentences = conll2002.iob_sents('esp.testa')
    #2. extract features
    train_df, test_df = extract_ident_features(train_sentences, test_sentences)
    #3. train     
    clf = identifier.train(train_df, test_df)
    

#IT ONLY WORKS FOR ONE ARTICLE AT A TIME...
def tag_articles():

    print "- read tagged articles csv"
    article_df = pd.read_csv("./files/pos_articles.csv")    


    # article_df = article_df.head()  #just for testing purposes
    #1. prepare data
    # article_df.loc[:,"tagged_title"] = article_df.tagged_title.apply(lambda x: ast.literal_eval(x))
    article_df.loc[:,"tagged_content"] = article_df.tagged_content.apply(lambda x: ast.literal_eval(x))

    sentences = article_df.loc[0].tagged_content
    #2. extract features
    feature_df, words_df = extract_ident_features(sentences)
    #3. predict
    preds = identifier.predict(feature_df.drop("NE",1))
    
    # print words_df[words_df["NE"]==1] #just for testing purposes
    print "- saving result to json"
    words_df.loc[:,"NE"] = preds 
    words_df.to_json("./files/NE_words.json")

    


