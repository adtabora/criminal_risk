from pos_tagger.preprocess import preprocess
from pos_tagger.features import extract_features
from pos_tagger.classifier import train, predict
from pos_tagger.output_formatter import save_results


def train_classifier(train_sentences, test_sentences):
    features_df = extract_features(train_sentences, test_sentences)
    train(features_df)


def tag(sentences):
    corpora = preprocess(sentences)

    features_df = extract_features(sentences)
    preds = predict(features_df)
    save_results(sentences,preds)
        

#code for unit testing while developing

from nltk.corpus import  conll2002
train_classifier(
    conll2002.iob_sents('esp.train'), 
    conll2002.iob_sents('esp.testa')
    )