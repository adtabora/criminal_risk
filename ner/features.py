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



#
def extract_ident_features(sentences, test_sentences=None):
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
        words_df = convert_df(sentences, iob=True)
        features_df = get_ident_features(words_df,iob=True)
        print "-Done."
        return features_df, words_df

#
def get_classif_features(base_df, iob=False, train=False):
    print "- get classifier features"
    df = pd.DataFrame()

    #Trianing Label Encoders
    if train:
        print "- training tag encoder"
        #tag encoder
        le_tag = LabelEncoder()
        le_tag.fit(base_df.tag)
        pickle.dump( le_tag, open( "./files/pos_tag_encoder.p", "wb" ) )
        print "- training iob encoder"
        #iob encoder
        le_iob = LabelEncoder()
        le_iob.fit(base_df.iob)
        print "- le_iob tags"
        print le_iob.classes_ 
        pickle.dump( le_iob, open( "./files/iob_tag_encoder.p", "wb" ) )
    else:
        print "- loading tag encoder"
        le_tag = pickle.load( open( "./files/pos_tag_encoder.p", "rb" ) )
        print "- loading iob encoder"
        le_iob = pickle.load( open( "./files/iob_tag_encoder.p", "rb" ) )
    
    # iob
    if iob: 
        df.loc[:,"iob"] = le_iob.transform(base_df.iob)
        df.loc[:,"NE"] = base_df.iob.apply(lambda x: int(x != "O"))
    else:
        #the other case has the NE incorporated
        df.loc[:,"NE"] = base_df.NE
    #Named Entity
    
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

    #relative tags features
    tags = df.tag.values.tolist()
    df.loc[:,"prev_1"] = [-1] + tags[:-1]
    #removing the prev_1 tag for all the first word in each sentence
    df.at[df["pos"] == 0,'prev_1'] = -1

    df.loc[:,"prev_2"] = [-1,-1] + tags[:-2]
    #removing the prev_2 tag for all the first and second word in each sentence
    df.at[(df["pos"] == 0) | (df["pos"] == 1),'prev_2'] = -1

    #TODO: Correct the last 2 words of each sentence
    df.loc[:,"next_1"] = tags[1:] + [-1]
    df.loc[:,"next_2"] = tags[2:] + [-1,-1]

    #relative NE features
    nes = df.NE.values.tolist()
    df.loc[:,"prevNE_1"] = [0] + nes[:-1]
    df.at[df["pos"] == 0,'prevNE_1'] = 0
    df.loc[:,"prevNE_2"] = [0,0] + nes[:-2]
    df.at[(df["pos"] == 0) | (df["pos"] == 1),'prevNE_2'] = 0

    #TODO: Correct the last 2 words of each sentence
    df.loc[:,"nextNE_1"] = nes[1:] + [0]
    df.loc[:,"nextNE_2"] = nes[2:] + [0,0]


    # tag_df = pd.get_dummies(df.tag,prefix="tag_")
    # for column in tag_df.columns:
    #     df.loc[:,column] = tag_df[column]

    return df


#
def extract_classif_features(sentences, test_sentences=None):
    print "-- Extract features"
    if test_sentences != None:
        #1. convert to dataframe format
        train_df = convert_df(sentences,iob=True)
        test_df = convert_df(test_sentences,iob=True)

        #2. get classifier features
        train_df = get_classif_features(train_df,iob=True,train=True)
        test_df = get_classif_features(test_df,iob=True,train=False)

        #Filter only NE since that is what we are trying to classify
        train_df = train_df[train_df["NE"]==1]
        test_df = test_df[test_df["NE"]==1]

        print "-Done."
        return train_df, test_df

    else:
        
        
        words_df = sentences
        features_df = get_classif_features(words_df)

        #Filter only NE since that is what we are trying to classify
        features_df = features_df[features_df["NE"]==1]
        words_df = words_df[words_df["NE"]==1]
        print "-Done."
        return features_df, words_df
