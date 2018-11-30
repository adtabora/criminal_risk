import pandas as pd
import numpy as np
import ast 
import unicodedata

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold

def sentenceComposition(sent):
    country = 0
    state = 0
    city = 0
    zones = 0
    for word in sent:
        if word[2] == "B-Country":
            country = 1
        if word[2] == "B-State":
            state = 1
        if word[2] == "B-City":
            city = 1
        if word[2] in ["B-Zone","B-Col","B-Bar","B-Res"]:
            zones = 1
    return "%i-%i-%i-%i" %(country,state,city,zones)

def convertToSentences(df, toObject=True):
    if toObject:
        df.tagged_content = df.tagged_content.apply(lambda x: ast.literal_eval(x))
    print "- Convert to Sentences"
    data = []
    cs_id = -1  #corpus sentence id
    for _, article in df.iterrows():
        sentences = article.tagged_content
        for sent_ix, sent in enumerate(sentences):
            cs_id +=1
            data.append([
                article.article_id, 
                sent_ix,
                cs_id,
                sent,
                sentenceComposition(sent)
            ])

    df = pd.DataFrame(data, columns=["art_id","sent_id","cs_id","sentence", "cat"])
    return df

def sentenecesToWords(df):
    print "- Sentences to Words"
    data = []
    for _, sent in df.iterrows():
        for pos, word in enumerate(sent.sentence):
            data.append([
                sent.art_id, 
                sent.sent_id,
                sent.cs_id,
                pos,
                word[0],
                word[1],
                word[2]
            ]) 
    df = pd.DataFrame(data, columns=["art_id","sent_id","cs_id","pos", "word","pos_tag","iob_tag"])

    #clean the iob
    df.loc[:,"iob_tag"] = df.iob_tag.apply(lambda x: x if x not in ["B-Misc", "I-Misc"] else "none" )
    df.loc[:,"iob_tag"] = df.iob_tag.apply(lambda x: x if x not in ["B-Res", "I-Res"] else x[:2]+"Zone" )
    # separate the geo-entity classification from the IOB tag
    df.loc[:, "iob"] = df.iob_tag.apply(lambda x: "I" if x != "none"  else "O" )
    df.loc[:, "geo_type"] = df.iob_tag.apply(lambda x: x[2:] if x != "none"  else x )

    return df

def wordsToEntities(df):
    print "- Words to Entities"
    data = []
    for idx, row in df.iterrows():
        if row.iob_tag[0] in ["B","n"]:
            data.append([row])
        else:
            data[-1].append(row)
    
    entity_df = pd.DataFrame({ 
        "entity":data
    })

    entity_df.loc[:,"cat"] = entity_df.entity.apply(lambda x: x[0].geo_type + "_" + str(len(x)))
    entity_df.loc[:,"category"] = entity_df.entity.apply(lambda x: x[0].geo_type)
    entity_df.loc[:,"size"] = entity_df.entity.apply(lambda x: len(x))

    low_cats = entity_df.cat.value_counts()[ entity_df.cat.value_counts() < 8 ].index.values
    safety = 10
    while low_cats.shape[0] > 0 and safety > 0:
        for cat in low_cats:
            entity_df.at[entity_df["cat"]==cat,"cat"] = cat[:-1] + str( int(cat[-1]) - 1 )
        low_cats = entity_df.cat.value_counts()[ entity_df.cat.value_counts() < 8 ].index.values
        safety -= 1
    
    return entity_df
    

def entitiesToWords(df, columns):
    print "- Entities to Words"
    data = []
    for _, row in df.iterrows():
        for entity in row.entity:
            data.append(entity)
            
    df = pd.DataFrame(data, columns=columns)
    return df
# convert the sentences to word tokens
def convertToWords(articles):
    articles.tagged_content = articles.tagged_content.apply(lambda x: ast.literal_eval(x))
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
    df.loc[:,"iob_tag"] = df.iob_tag.apply(lambda x: x if x not in ["B-Res", "I-Res"] else x[:2]+"Zone" )
    # separate the geo-entity classification from the IOB tag
    df.loc[:, "iob"] = df.iob_tag.apply(lambda x: "B" if x != "none"  else "O" )
    df.loc[:, "geo_type"] = df.iob_tag.apply(lambda x: x[2:] if x != "none"  else x )
    
    return df

# split sentences using the distribution of entities 
def splitTrainTest(df):
    print "- Split Train Test"

    # Make a stratified split based on entity counts
    print "-- Stratified split"
    skf = StratifiedKFold(n_splits=5,shuffle=True, random_state= 773 )  #233

    count = 0
    for train_index, test_index in skf.split( df, df.cat.tolist()):
        train_df = df.loc[train_index]
        test_df = df.loc[test_index]

        if count == 3:
            break #we only need one iteration since it is a simple split
        count += 1

    print "--  Distribution"
    dist_df = pd.DataFrame({})
    dist_df["original"] = df.cat.value_counts() / df.shape[0]
    dist_df["train"] = train_df.cat.value_counts() / train_df.shape[0]
    dist_df["test"] = test_df.cat.value_counts() / test_df.shape[0]
    print dist_df
    return train_df, test_df




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


def hot_encode(df,columns):
    for column in columns:
        dummies = pd.get_dummies(df[column], prefix=column)
        df = pd.concat([df, dummies], axis=1)

        df = df.drop(column, axis=1)
    return df


def getFeatures(df, le_iob=None, le_tag=None, root_folder="../../"):
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
    upper = df.upper.values.tolist()
    df.loc[:,"upper_prev1"] = [0] + upper[:-1]
    df.loc[:,"upper_next1"] =  upper[1:] + [0]
    # first word in sentence
    df.loc[:,"first"] = df.pos.apply(lambda x: int(x == 0) )
    # first sentence
    df.loc[:,"first_sent"] = df.sent_id.apply(lambda x: int(x==0)).values
    # size
    df.loc[:,"size"] = df.word.apply(lambda x: len(x))
    

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
    words = df.word.apply(lambda x: x.lower() ).values.tolist()

    prev_words_1 = pd.Series(words[-1:] + words[:-1])
    prev_words_2 = pd.Series(words[-2:] + words[:-2])



    def isin_trigger(trigger_words, name):
        df.loc[:,"trigger"+name+"1"]  = prev_words_1.apply(lambda x:  int( x in trigger_words )).values.tolist()
        df.loc[:,"trigger"+name+"2"]  = prev_words_2.apply(lambda x:  int( x in trigger_words )).values.tolist()

    #trigger state
    state_words = ["estado", "departamento"] #review if region should be here
    isin_trigger(state_words, "state")

    #trigger city
    city_words = ["ciudad","aldea"]
    isin_trigger(city_words, "city")

    #trigger zone?
    zone_words = ["zona","puente","mercado","bulevar","comunidad","como","-","ruta"]
    isin_trigger(zone_words, "zone")
    
    # Trigger Colonia
    isin_trigger(["colonia"], "colonia")

    # Trigger Barrio
    isin_trigger(["barrio"], "barrio")
    # Trigger Residencial
    isin_trigger(["residencial"], "residencial")




    # Trigger Features
    trigger_words = ["en","de","del","la"]
    df.loc[:,"trigger_1"] = words[-1:] + words[:-1]
    df.loc[:,"trigger_1"]  = df.trigger_1.apply(lambda x:  int( x in trigger_words ))
    
    df.loc[:,"trigger_2"] = words[-2:] + words[:-2]
    df.loc[:,"trigger_2"]  = df.trigger_2.apply(lambda x:  int( x in trigger_words ))

    #Gazetteer features
    countries_df = pd.read_csv(root_folder + "files/countries.csv", encoding="utf-8")
    dep_mun_df = pd.read_csv(root_folder + "files/DepartamentosMunicipios.csv", encoding="utf-8")
    world_cities = pd.read_csv(root_folder + "files/ciudades_mundo.csv", encoding="utf-8")
    
    dep_mun_df= dep_mun_df.append(pd.DataFrame([
        [u"francisco morazan",u"comayaguela"],
        [u"francisco morazan",u"distrito central"], 
    ],columns= dep_mun_df.columns), ignore_index=True
    )


    #converting to ascii because of accents (tilde)
    countries_df.value = countries_df.value.apply(lambda x: to_ascii(x).lower() )
    dep_mun_df.Departamento = dep_mun_df.Departamento.apply(lambda x: to_ascii(x).lower() )
    dep_mun_df.Municipio = dep_mun_df.Municipio.apply(lambda x: to_ascii(x).lower() )
    world_cities.city = world_cities.city.apply(lambda x: to_ascii(x).lower() )
    #dropping city "Colonia" from Germany because it's causing problems
    world_cities = world_cities[world_cities["city"]!="colonia"]

    country = []
    state = []
    city = []

    words = df.word.apply(lambda x: to_ascii(x).lower() ).values.tolist()
    prev_2 = ["",""] + words[:-2]
    prev_1 = [""] + words[:-1]
    next_1 = words[1:] + [""]
    next_2 = words[2:] + ["",""]

    #convert to dummies
    # columns = ["prev_1", "prev_2","next_1","next_2","pos_tag"]
    # df = hot_encode(df,columns)

    
    #Sentence Size
    sentence_size = pd.DataFrame({
        "cs_id":df.cs_id.value_counts().index.values,
        "sent_size": df.cs_id.value_counts().values
    })
    
    df = df.merge(sentence_size, left_on='cs_id', right_on='cs_id', how='left')

    cities_gazette = np.concatenate([dep_mun_df.Municipio.values, world_cities.city.values])

    for idx in range(len(words)):
        word_list = [prev_2[idx],prev_1[idx],words[idx],next_1[idx],next_2[idx]]
        #.tolist() + ["ee. uu.","ee uu","eeuu"]
        country.append( entity_in_gazette(word_list,countries_df.value.values  ) )
        state.append( entity_in_gazette(word_list,dep_mun_df.Departamento.values) )
        city.append( entity_in_gazette(word_list, cities_gazette ) )

    df.loc[:,"in_Country"] = country
    df.loc[:,"in_State"] = state
    df.loc[:,"in_City"] = city

    
    return df, le_iob, le_tag





