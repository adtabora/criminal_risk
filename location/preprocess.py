import pandas as pd
import numpy as np
import ast 

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold

# convert the articles.csv into sentences
def convertToSentences(articles):
    print "- Convert to Sentences"
    #convert from string to python object
    articles.tagged_content = articles.tagged_content.apply(lambda x: ast.literal_eval(x))
    
    data = []
    cs_id = -1  #corpus sentence id
    for _, article in articles.iterrows():
        sentences = article.tagged_content
        for sent_ix, sent in enumerate(sentences):
            cs_id +=1
            data.append([
                article.article_id, 
                sent_ix,
                cs_id,
                sent
            ])
    
    df = pd.DataFrame(data,columns=["art_id", "sent_id", "cs_id", "sentence"])
    return df


# split sentences using their distribution of entities
def splitTrainTest(sentences):
    print "- Split Train Test"
    # Count the entities
    print "-- Count entities per sentence"
    def getEntityCount(sentence):
        return sum([ 1 for word in sentence if word[2] == "B-Loc" ])
    entity_counts = sentences.sentence.apply(lambda sent: getEntityCount(sent)).values

    # print "ENTITY COUNTS: %i" % sum(entity_counts)
    sentences.loc[:,"entity_count"] = entity_counts

    # Make a stratified split based on entity counts
    print "-- Stratified split"
    skf = StratifiedKFold(n_splits=5,shuffle=True, random_state= 233 )
    for train_index, test_index in skf.split( np.zeros(sentences.shape[0]), entity_counts):
        sentences_train = sentences.iloc[ train_index ]
        sentences_test = sentences.iloc[ test_index ]
        break #we only need one iteration since it is a simple split

    print "entities per sentence (Original): %0.4f" % (sentences.entity_count.sum() * 1.0 / sentences.shape[0] )
    print "entities per sentence (Train): %0.4f" % (sentences_train.entity_count.sum() * 1.0 / sentences_train.shape[0] )
    print "entities per sentence (Test): %0.4f" % (sentences_test.entity_count.sum() * 1.0 / sentences_test.shape[0] )

    return sentences_train, sentences_test

# convert the sentences to word tokens
def convertToWords(sentences):
    print "- Convert to Word tokens"
    data = []
    for _, sentence in sentences.iterrows():
        for pos, word in enumerate(sentence.sentence):
            data.append([
                sentence.art_id,
                sentence.sent_id,
                sentence.cs_id,
                pos,
                word[0],
                word[1],
                word[2]
            ])

    df = pd.DataFrame(data, columns=["art_id","sent_id","cs_id","pos", "word","pos_tag","iob_tag"])
    return df


def getFeatures(df, le_iob=None, le_tag=None):
    print "- getting features"
    # iob
    #clean the iob
    df.loc[:,"iob_tag"] = df.iob_tag.apply(lambda x: x if x!="B-Org" else "none" )
    if le_iob == None:
        le_iob = LabelEncoder()
        le_iob.fit(df.iob_tag)

    df.loc[:,"iob_tag"] = le_iob.transform(df.iob_tag)
    # print "-- iob tag classes"
    # print le_iob.classes_
    # tag
    if le_tag == None:
        le_tag = LabelEncoder()
        le_tag.fit(df.pos_tag)
    df.loc[:,"pos_tag"] = le_tag.transform(df.pos_tag)
    # print "-- pos tag classes"
    # print le_tag.classes_
    # If word first letter is uppercase
    df.loc[:,"upper"] = df.word.apply(lambda x: x[0].isupper())
    # first word in sentence
    df.loc[:,"first"] = df.pos.apply(lambda x: int(x == 0) )
    # size
    df.loc[:,"size"] = df.word.apply(lambda x: len(x))
    # first sentence
    df.loc[:,"first_sent"] = df.sent_id.apply(lambda x: int(x==0)).values

    # TAGS
    # add tag features by shifting the tag list 
    tags = df.pos_tag.values.tolist()

    df.loc[:,"prev_1"] = tags[-1:] + tags[:-1]
    # df.at[df["pos"] < 1,'prev_1'] = -1
    df.loc[:,"prev_2"] = tags[-2:] + tags[:-2]
    df.at[df["pos"] < 2,'prev_2'] = -1

    df.loc[:,"next_1"] = tags[1:] + tags[:1]
    df.loc[:,"next_2"] = tags[2:] + tags[:2]

    # PREVIOUS WORDS (In spanish the type of location are written before the NE )
    loc_types = ["colonia", "barrio", "residencial","ciudad", "aldea","zona","puente","mercado"]
    words = df.word.apply(lambda x: x.lower() ).values.tolist()
    df.loc[:,"prev_prefix_1"] = words[-1:] + words[:-1]
    df.loc[:,"prev_prefix_1"]  = df.prev_prefix_1.apply(lambda x:  int( x in loc_types ))
    
    df.loc[:,"prev_prefix_2"] = words[-2:] + words[:-2]
    df.loc[:,"prev_prefix_2"]  = df.prev_prefix_2.apply(lambda x:  int( x in loc_types ))

    
    return df, le_iob, le_tag




