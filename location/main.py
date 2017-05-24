import preprocess as process
import identifier
from  entities import extract_true_entities, extract_identified_entities, score_entities
import pandas as pd

from sklearn.preprocessing import LabelEncoder

# read 
articles_df = pd.read_csv("../files/pos_articles.csv")
sentences_df = process.convertToSentences(articles_df)

# print sentences_df.head()

sent_train, sent_test = process.splitTrainTest(sentences_df)

words_train = process.convertToWords(sent_train)
words_test = process.convertToWords(sent_test)

# print words_train.loc[30:80]


#train a label encoder for tags using the whole corpus
le_tag = LabelEncoder()
le_tag.fit(words_train.pos_tag.values.tolist() + words_test.pos_tag.values.tolist())

features_train, le_iob, _ = process.getFeatures(words_train.copy(), le_tag= le_tag)
features_test, _,_ = process.getFeatures(words_test.copy(), le_iob, le_tag)

pred_train, pred_test = identifier.train_identifier(features_train, features_test)


# Score based on identified entities
true_ent_train = extract_true_entities(words_train)
true_ent_test = extract_true_entities(words_test)

# print "true ent train shape %i" %true_ent_train.shape[0]
# print "true ent test shape %i" %true_ent_test.shape[0]

ident_ent_train = extract_identified_entities(features_train, pred_train, le_iob)
ident_ent_test = extract_identified_entities(features_test, pred_test, le_iob)
# print "ident ent train shape %i" %ident_ent_train.shape[0]
# print "ident ent test shape %i" %ident_ent_test.shape[0]

print "--- TRAIN SCORES ---"
score_entities(true_ent_train, ident_ent_train)
print
print "--- TEST SCORES ---"
score_entities(true_ent_test, ident_ent_test)
print 


