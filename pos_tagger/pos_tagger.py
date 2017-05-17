from nltk.corpus import  conll2002
from nltk.tag import untag, BrillTaggerTrainer, DefaultTagger, UnigramTagger
from nltk.tbl.template import Template
from nltk.tag.brill import Pos, Word



import pickle

import bs4 #beautiful soup
import pandas as pd
import numpy as np
import json
import ast
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
    article_df = pd.read_csv("./files/criminal_articles.csv") 
    article_df.loc[:,"title"] = article_df.title.apply(lambda x: ast.literal_eval(x))
    article_df.loc[:,"content"] = article_df.content.apply(lambda x: ast.literal_eval(x))

    #2. Load tagger
    print "- load tagger"
    tagger = pickle.load( open( "./files/pos_tagger.p", "rb" ) )
    
    #3. Tag the articles
    print "- tagging articles"

    def tagContent(content):
        for index, sentence in enumerate(content):
            #use only words not the NE tags
            sentence = [ word[0] for word in sentence]
            #tag
            content[index] = tagger.tag(sentence)
        return content


    # tag the title
    print "- tagging title"
    article_df.loc[:,"tagged_title"] = article_df.title.apply(
        lambda title: tagger.tag([ word[0] for word in title])
    )

    # tag the content
    print "- tagging content"
    article_df.loc[:,"tagged_content"] = article_df.content.apply(
        lambda content:  tagContent(content)
    )
    
    print "- save tagged articles to csv"
    article_df = article_df.drop(["title","content"], axis=1)
    # article_df.to_json("./files/pos_articles.json")
    article_df.to_csv("./files/pos_articles.csv",index=False, encoding='utf-8')

    print "- Done."

    

