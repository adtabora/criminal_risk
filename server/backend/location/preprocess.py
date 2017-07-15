import pandas as pd
import numpy as np
import ast 
import unicodedata

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold

# split sentences using the distribution of entities 
def splitTrainTest(df):
    print "- Split Train Test"

    #convert from string to python object
    df.tagged_content = df.tagged_content.apply(lambda x: ast.literal_eval(x))
    # Count the entities
    print "-- Count entities per Article"
    def getEntityCount(sentence):
        return sum([ 1 for word in sentence if word[2][0] == "B"  ])

    counts = []
    for _, article in df.iterrows():
        article_count = 0
        sentences = article.tagged_content
        for sent in sentences:
            article_count += getEntityCount(sent)
        counts.append(article_count)
    df.loc[:,"entity_count"] = counts 

    # Make a stratified split based on entity counts
    print "-- Stratified split"
    skf = StratifiedKFold(n_splits=5,shuffle=True, random_state= 233 )
    for train_index, test_index in skf.split( df, df.entity_count.tolist()):
        train_df = df.loc[train_index]
        test_df = df.loc[test_index]
        break #we only need one iteration since it is a simple split

    print "entities per article (Original): %0.4f" % (sum(counts) * 1.0  / len(counts) )
    print "entities per article (Train): %0.4f" % (train_df.entity_count.sum()  * 1.0 / train_df.shape[0] )
    print "entities per article (Test): %0.4f" % (test_df.entity_count.sum()  * 1.0 / test_df.shape[0] )

    print "number of articles(Original): %i" % df.shape[0]
    print "number of articles(Train): %i" % train_df.shape[0]
    print "number of articles(Test): %i" % test_df.shape[0]

    return train_df, test_df

# convert the sentences to word tokens
def convertToWords(articles):
    print "- Convert to Word tokens"
    data = []
    cs_id = -1  #corpus sentence id
    for _, article in articles.iterrows():
        sentences = article.tagged_content
        for sent_ix, sent in enumerate(sentences):
            cs_id +=1
            for pos, word in enumerate(sent):
                data.append([
                    article.article_id, 
                    sent_ix,
                    cs_id,
                    pos,
                    word[0],
                    word[1],
                    word[2]
                ])        
    df = pd.DataFrame(data, columns=["art_id","sent_id","cs_id","pos", "word","pos_tag","iob_tag"])
    
    #clean the iob
    df.loc[:,"iob_tag"] = df.iob_tag.apply(lambda x: x if x not in ["B-Misc", "I-Misc"] else "none" )
    # separate the geo-entity classification from the IOB tag
    df.loc[:, "iob"] = df.iob_tag.apply(lambda x: "B" if x != "none"  else "O" )
    df.loc[:, "geo_type"] = df.iob_tag.apply(lambda x: x[2:] if x != "none"  else x )
    
    return df


# very useful function to avoid mispellings problems.
def to_ascii(s):
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')

# finds if a word or a group of words are contained in a gazette
# words parameter is a list of 5 words where the 3rd word is the base word 
# and the others are the previous or next words
def entity_in_gazette(words,gazette):
    #use base word
    if words[2] in gazette:
        return 1
    # bigram
    elif " ".join(words[1:3]) in gazette \
        or " ".join(words[2:4]) in gazette:
        return 1
    # trigram
    elif  " ".join(words[0:3]) in gazette \
        or " ".join(words[1:4]) in gazette \
        or " ".join(words[2:5]) in gazette:
        return 1
    else:
        return 0

def getFeatures(df, le_iob=None, le_tag=None):
    print "- getting features"
    # iob
    if le_iob == None:
        le_iob = LabelEncoder()
        le_iob.fit(df.iob)
    df.loc[:,"iob"] = le_iob.transform(df.iob)

    print "-- iob tag classes"
    print le_iob.classes_
    # tag
    if le_tag == None:
        le_tag = LabelEncoder()
        le_tag.fit(df.pos_tag)
    df.loc[:,"pos_tag"] = le_tag.transform(df.pos_tag)
    # print "-- pos tag classes"
    # print le_tag.classes_
    # If word first letter is uppercase
    df.loc[:,"upper"] = df.word.apply(lambda x: int(x[0].isupper()) )
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
    loc_types = ["colonia", "barrio", "residencial","ciudad", 
    "aldea","zona","puente","mercado","bulevar","centro","estado"]
    words = df.word.apply(lambda x: x.lower() ).values.tolist()
    df.loc[:,"prev_prefix_1"] = words[-1:] + words[:-1]
    df.loc[:,"prev_prefix_1"]  = df.prev_prefix_1.apply(lambda x:  int( x in loc_types ))
    
    df.loc[:,"prev_prefix_2"] = words[-2:] + words[:-2]
    df.loc[:,"prev_prefix_2"]  = df.prev_prefix_2.apply(lambda x:  int( x in loc_types ))

    #Gazette features
    countries_df = pd.read_csv("../../files/countries.csv", encoding="utf-8")
    dep_mun_df = pd.read_csv("../../files/DepartamentosMunicipios.csv", encoding="utf-8")
    world_cities = pd.read_csv("../../files/ciudades_mundo.csv", encoding="utf-8")
    #converting to ascii because of accents (tilde)
    countries_df.value = countries_df.value.apply(lambda x: to_ascii(x).lower() )
    dep_mun_df.Departamento = dep_mun_df.Departamento.apply(lambda x: to_ascii(x).lower() )
    dep_mun_df.Municipio = dep_mun_df.Municipio.apply(lambda x: to_ascii(x).lower() )
    world_cities.city = world_cities.city.apply(lambda x: to_ascii(x).lower() )

    country = []
    state = []
    city = []

    words = df.word.apply(lambda x: to_ascii(x).lower() ).values.tolist()
    prev_2 = ["",""] + words[:-2]
    prev_1 = [""] + words[:-1]
    next_1 = words[1:] + [""]
    next_2 = words[2:] + ["",""]


    cities_gazette = np.concatenate([dep_mun_df.Municipio.values, world_cities.city.values])

    for idx in range(len(words)):
        word_list = [prev_2[idx],prev_1[idx],words[idx],next_1[idx],next_2[idx]]
        
        country.append( entity_in_gazette(word_list,countries_df.value.values) )
        state.append( entity_in_gazette(word_list,dep_mun_df.Departamento.values) )
        city.append( entity_in_gazette(word_list, cities_gazette ) )

    df.loc[:,"in_Country"] = country
    df.loc[:,"in_State"] = state
    df.loc[:,"in_City"] = city
    
    return df, le_iob, le_tag




