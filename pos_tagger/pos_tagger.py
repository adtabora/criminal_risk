from nltk.corpus import  conll2002
from nltk.tag import untag, BrillTaggerTrainer, DefaultTagger, UnigramTagger
from nltk.tbl.template import Template
from nltk.tag.brill import Pos, Word



import pickle

import bs4 #beautiful soup
import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize

# Function that trains a Brill Taggers using Unigram as backoff 
def train(train_sentences):
    print "- Default Tagger"
    default_tagger = DefaultTagger('NC')

    print "- Unigram Tagger"
    unigram_tagger = UnigramTagger(train_sentences,backoff=default_tagger)


    print "- Templates"
    #These templates define the features to be used for the brill tagger
    # relatively to the word position.
    Template._cleartemplates() 
    templates = [
        Template(Pos([-1])), 
        Template(Pos([-1]), Word([0])), 
        Template(Pos([-2])), 
        Template(Pos([-2]), Word([0])),
        Template(Pos([1])), 
    ]
    print "- Brill Tagger"
    tt = BrillTaggerTrainer(unigram_tagger, templates, trace=1)
    tagger = tt.train(train_sentences, max_rules=1000)

    print "- Done."

    return tagger






def train_tagger():
    print "--- Train Tagger ---"
    #1. prepare data
    train_sentences = conll2002.tagged_sents('esp.train')
    test_sentences = conll2002.tagged_sents('esp.testa')
    #2. train brill tagger
    tagger = train(train_sentences)
    #3. test brill tagger
    print "- test score: %0.4f" %tagger.evaluate(test_sentences)
    #4. save tagger into a file
    print "- saving tagger"
    pickle.dump( tagger, open( "./files/pos_tagger.p", "wb" ) )

    print "-- DONE."


def tag_articles():
    #1. read articles
    print "- read articles csv"
    article_df = pd.read_csv("./files/articles.csv")    


    #2. Load tagger
    print "- load tagger"
    tagger = pickle.load( open( "./files/pos_tagger.p", "rb" ) )
    
    #3. Process, clean and tag
    #source_column is to be changed in the future
    source_column = "content" 
    articles = []
    print "- processing and tagging articles"
    for art_index, article in article_df.iterrows():
        raw_text = article[source_column]
        soup = bs4.BeautifulSoup(raw_text, 'html.parser')
        text = soup.get_text().replace("\n","")
        sentences = text.split(".")
        for sent_index in range(len(sentences)):
            tagged_sent = tagger.tag(  word_tokenize( sentences[sent_index] ) )
            #append
            articles.append([
                art_index,
                sent_index,
                tagged_sent
            ])
    
    print "- save tagged articles to csv"
    tagged_articles = pd.DataFrame(articles,columns=["article_id","sent_id","tagged_sent"])
    tagged_articles.to_csv("./files/tagged_articles.csv",index=False)

    print "- Done."

    

