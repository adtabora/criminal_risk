import pandas as pd
import numpy as np
import unicodedata

# very useful functions to avoid mispellings problems.
# you'll thank me later
def to_ascii(s):
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')

def sent_to_ascii(sentences):
    for sent_ix, sent in enumerate(sentences):
        for word_ix, word in enumerate(sent):
            sentences[sent_ix][word_ix][0] =  to_ascii(word[0])
    return sentences
            
def rel_to_ascii(relationships):
    for rel_ix, rel in enumerate(relationships):
        relationships[rel_ix][0]["word"] = to_ascii(relationships[rel_ix][0]["word"])
        relationships[rel_ix][1]["word"] = to_ascii(relationships[rel_ix][1]["word"])
    return relationships


def format_relationship_tags(relationships):

    for ix, rel in enumerate(relationships):
        relationships[ix][0]["tag"] = rel[0]["tag"][2:]
        relationships[ix][1]["tag"] = rel[1]["tag"][2:]
    return relationships

# getEntitydf
# gets entities with the distances in words between them. i.e. "next_words"
def getEntitydf(article):
    data = []
    word_count = 0
    for sent_id, sent in enumerate(article.full_text):
        for pos, word in enumerate(sent):
            if word[1][0] == "B":
                if len(data) > 0:
                    data[-1][-1] = word_count
                word_count = 0
                data.append([word[0].lower(),word[1][2:], sent_id, pos, 0 ])
            elif word[1][0] == "I":
                data[-1][0] += " " + word[0].lower()
            else:
                word_count += 1

    entity_df = pd.DataFrame(data, columns=["entity", "tag", "sent_id", "pos", "next_words"])
    return entity_df   

def getEntities(content):
    entities = []
    for sent in content:
        for word in sent:
            if word[1][0] == "B":
                entities.append({"word": word[0].lower(),"tag":word[1][2:]})
            elif word[1][0] == "I":
                entities[-1]["word"] += " " + word[0].lower()
                
    #eliminate duplicates
    unique_entities = []
    for itm in entities:
        if itm not in unique_entities:
            unique_entities.append(itm)
                
    return unique_entities


# getPairs
# generates all the possible pairs of relationships
def getPairs(article):

    country_entities = [x for x in article.entities if  x["tag"]=="Country"]
    state_entities = [x for x in article.entities if  x["tag"]=="State"]
    city_entities = [x for x in article.entities if  x["tag"]=="City"]
    zone_entities = [x for x in article.entities if  x["tag"] in ["Zone","Col","Res","Bar"]]

    pairs = []
    for child in zone_entities:
        for parent in city_entities + state_entities + country_entities:
            relation = int([child,parent] in article.relationships)
            pairs.append([article.article_id,child["tag"],child["word"],parent["tag"],parent["word"],child,parent, relation])

    for child in city_entities:
        for parent in  state_entities + country_entities:
            relation = int([child,parent] in article.relationships)
            pairs.append([article.article_id, child["tag"],child["word"],parent["tag"],parent["word"],child,parent, relation])

    for child in state_entities:
        for parent in country_entities:
            relation = int([child,parent] in article.relationships)
            pairs.append([article.article_id, child["tag"],child["word"],parent["tag"],parent["word"],child,parent, relation])
            
    relations_df = pd.DataFrame(pairs,columns=["art_id",  "c_tag","c_word","p_tag","p_word","child","parent","label"])
    relations_df.loc[:,"rel_type"] = relations_df.c_tag +["-" for x in range(relations_df.shape[0])] +relations_df.p_tag 
    return relations_df


def getDepartmentGazetteer():
    dep_mun_df = pd.read_csv("../../files/DepartamentosMunicipios.csv", encoding="utf-8")

    dep_mun_df= dep_mun_df.append(pd.DataFrame([
            [u"francisco morazan",u"comayaguela"],
            [u"francisco morazan",u"distrito central"], 
        ],columns= dep_mun_df.columns), ignore_index=True
    )

    dep_mun_df.Departamento = dep_mun_df.Departamento.apply(lambda x: to_ascii(x).lower() )
    dep_mun_df.Municipio = dep_mun_df.Municipio.apply(lambda x: to_ascii(x).lower() )
    dep_mun_df.loc[:,"combined"] = dep_mun_df.Municipio + ["-" for i in range(dep_mun_df.shape[0])] + dep_mun_df.Departamento

    return dep_mun_df


def getWorldCititesGazetteer():
    world_cities = pd.read_csv("../../files/ciudades_mundo.csv", encoding="utf-8")
    world_cities.country = world_cities.country.apply(lambda x: to_ascii(x).lower() )
    world_cities.city = world_cities.city.apply(lambda x: to_ascii(x).lower() )
    world_cities.loc[:,"combined"] = world_cities.city + ["-" for i in range(world_cities.shape[0])] + world_cities.country
    return world_cities



# getFeatures
def getFeatures(relations_df,entity_df):
    #get the distances for each pair
    distances = []
    num_c_entity = []
    num_p_entity = []
    c_first = []
    p_first = []
    c_first_sent = []
    p_first_sent = []
    c_title = []
    p_title = []
    for _, pair in relations_df.iterrows():
        pair_distances = []

        #Number of occurences of the same entity
        num_c = entity_df[(entity_df["entity"]== pair.c_word)&(entity_df["tag"]== pair.c_tag)].shape[0]
        num_p = entity_df[(entity_df["entity"]== pair.p_word)&(entity_df["tag"]== pair.p_tag)].shape[0]
        num_c_entity.append(num_c)
        num_p_entity.append(num_p)

        #Is it in the first entity in the whole document?
        c_fe = 0 in entity_df[(entity_df["entity"]==pair.c_word)&(entity_df["tag"]==pair.c_tag)].index
        p_fe = 0 in entity_df[(entity_df["entity"]==pair.p_word)&(entity_df["tag"]==pair.p_tag)].index
        c_first.append(c_fe)
        p_first.append(p_fe)

        #Is it in the title?
        c_t = 0 in entity_df[(entity_df["entity"]==pair.c_word)&(entity_df["tag"]==pair.c_tag)].sent_id.values
        p_t = 0 in entity_df[(entity_df["entity"]==pair.p_word)&(entity_df["tag"]==pair.p_tag)].sent_id.values
        c_title.append(c_t)
        p_title.append(p_t)

        #Is it in the first sentence?
        c_fs = 1 in entity_df[(entity_df["entity"]==pair.c_word)&(entity_df["tag"]==pair.c_tag)].sent_id.values
        p_fs = 1 in entity_df[(entity_df["entity"]==pair.p_word)&(entity_df["tag"]==pair.p_tag)].sent_id.values
        c_first_sent.append(c_fs)
        p_first_sent.append(p_fs)

        indices = entity_df[(entity_df["entity"].isin([ pair.c_word,pair.p_word ])) \
                            & (entity_df["tag"].isin([pair.c_tag,pair.p_tag]))].index

        indices = sorted(indices)
        for i in range(len(indices)-1):
            for j in range(i+1,len(indices)):
                if entity_df.loc[indices[i]].tag == entity_df.loc[indices[j]].tag:
                    continue
                entity = entity_df.loc[indices[i]].entity
                distance = entity_df.loc[indices[i]:indices[j]-1].next_words.sum()
                #counting the entities in between
                if indices[j]-1 - indices[i] > 0: 
                    distance += entity_df.loc[indices[i]+1:indices[j]-1].next_words.count()
                pair_distances.append( distance )

        distances.append(pair_distances)
        
        

    relations_df.loc[:,"distances"] = pd.Series(distances)

    #minimum distance
    relations_df.loc[:,"minDistance"] = relations_df.distances.apply(lambda x: min(x))
    relations_df.loc[:,"maxDistance"] = relations_df.distances.apply(lambda x: max(x))
    relations_df.loc[:,"num_c_entity"] = num_c_entity
    relations_df.loc[:,"num_p_entity"] = num_p_entity

    relations_df.loc[:,"c_first"] = c_first
    relations_df.loc[:,"p_first"] = p_first
    relations_df.loc[:,"c_first_sent"] = c_first_sent
    relations_df.loc[:,"p_first_sent"] = p_first_sent
    relations_df.loc[:,"c_title"] = c_title
    relations_df.loc[:,"p_title"] = p_title
    
    #title or first
    relations_df.loc[:,"p_torf"] = relations_df.p_first_sent | relations_df.p_title
    relations_df.loc[:,"c_torf"] = relations_df.c_first_sent | relations_df.c_title
    
    relations_df.loc[:,"p_first"] = p_first
    
    
    relations_df.loc[:,"min_all"] = relations_df.child.apply(lambda x:  relations_df[relations_df["child"]==x].minDistance.min() )
    relations_df.loc[:,"num_rels"] = relations_df.child.apply(lambda x:  relations_df[relations_df["child"]==x].child.count() )
   
    # gazetteer features
    dep_mun_df = getDepartmentGazetteer()
    world_cities = getWorldCititesGazetteer()

    in_state_country = []
    in_city_state = []
    in_city_country = []

    city_states = []
    for ix, rel in relations_df.iterrows():
        # 2-1
        if rel.c_tag == "State":
            #search first in Honduras
            if rel.c_word in dep_mun_df.Departamento.values and rel.p_word == "honduras":
                in_state_country.append(1)
    #         elif rel.c_word in other_states:  #This could be improved by getting the list of USA, Mexico Colombia and others
            else:
                in_state_country.append(0)
                
        else:
            in_state_country.append(0)
                
        # 3-2
        if rel.c_tag == "City" and  rel.p_tag =="State":
            if rel.c_word +"-"+ rel.p_word in dep_mun_df.combined.values:
                in_city_state.append(1)
                city_states.append([rel.c_tag,rel.c_word, rel.art_id])
            else:
                in_city_state.append(0)
        else:
            in_city_state.append(0)
                
        
        # 3-1
        if rel.c_tag == "City"and rel.p_tag == "Country":
            #if the same entity has a relationship with a state then implicit relation
            
            if [rel.c_tag, rel.c_word,rel.art_id] in city_states:
                in_city_country.append(0)
                
            elif rel.c_word in dep_mun_df.Municipio.values and rel.p_word == "honduras":
                
                in_city_country.append(1)
            elif rel.c_word + "-" + rel.p_word in world_cities.combined.values:
                
                in_city_country.append(1)
            else:
        #             print rel.c_word + "-" + rel.p_word
                in_city_country.append(0)
        
        else:
            in_city_country.append(0)
    
    relations_df.loc[:,"state_country"] = in_state_country
    relations_df.loc[:,"city_state"] = in_city_state
    relations_df.loc[:,"city_country"] = in_city_country


    return relations_df 