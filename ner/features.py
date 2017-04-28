import pandas as pd
import numpy as np


from sklearn.preprocessing import LabelEncoder

import pickle


# receives a POS Tagged sentence with optional IOB tags
def convert_df(sentences, iob=False):
    print "- convert_df"
    s_id = []
    s_word = []
    s_tag = []
    s_iob =[]
    s_pos = []

    for sent_num in range(len(sentences)):
        sent = sentences[sent_num]
        for pos in range(len(sent)):
            word = sent[pos]
            s_id.append(sent_num)
            s_pos.append(pos)
            s_word.append(word[0])
            s_tag.append(word[1])
            if iob:
                s_iob.append(word[2])
            
        
    df = pd.DataFrame({
            "sentence": s_id,
            "pos": s_pos,
            "word": s_word,
            "tag": s_tag,
        })
    if iob:
        df.loc[:,"iob"] = s_iob

    return df

# This function engineers features
def get_ident_features(base_df,  iob=False, train=False,):
    print "- get features"
    df = pd.DataFrame()

    #Trianing Label Encoders
    if train:
        print "- training tag encoder"
        #tag encoder
        le_tag = LabelEncoder()
        le_tag.fit(base_df.tag)
        pickle.dump( le_tag, open( "./files/pos_tag_encoder.p", "wb" ) )
    else:
        print "- load tag encoder"
        le_tag = pickle.load( open( "./files/pos_tag_encoder.p", "rb" ) )
    
    # NE - named entity label
    if iob: 
        df.loc[:,"NE"] = base_df.iob.apply(lambda x: int(x!="O"))
    #tag
    df.loc[:,"tag"] = le_tag.fit_transform(base_df.tag)
    # Uppercase
    df.loc[:,"upper"] = base_df.word.apply(lambda x: int(x[0].isupper())) 
    # Pos
    df.loc[:,"pos"] = base_df.pos
    #first 
    df.loc[:,"first"] = base_df.pos.apply(lambda x: int(x == 0) )
    #size
    df.loc[:,"size"] = base_df.word.apply(lambda x: len(x))
    
    return df




def extract_features(sentences, test_sentences=None):
    print "-- Extract features"
    if test_sentences != None:
        #1. convert to dataframe format
        train_df = convert_df(sentences,iob=True)
        test_df = convert_df(test_sentences,iob=True)
        #2. get identifier features
        train_df = get_ident_features(train_df,iob=True,train=True)
        test_df = get_ident_features(test_df,iob=True,train=False)

        print "-Done."
        return train_df, test_df

    else:
        words_df = convert_df(sentences)
        features_df = get_ident_features(words_df)
        print "-Done."
        return features_df, words_df
