from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import StratifiedKFold
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import precision_recall_fscore_support

import scipy.sparse as sp

import pandas as pd
stop_words = pd.read_json("../../files/stopwords.json")[0].values.tolist()

# A Multinomial Naive Bayes Classifier
class NBClassifier():
    alpha = None
    title = None
    content = None

    accuracy = {"train": 0.0,"test":0.0 }
    precision = {"train": 0.0,"test":0.0 }
    recall = {"train": 0.0,"test":0.0 }
    fscore = {"train": 0.0,"test":0.0 }


    def __init__(self, alpha, title=None, content=None ):
        self.alpha = alpha
        if title != None:
            self.title = title    
            # self.title.min = title.min if title.min else 1
            # self.title.max = title.max if title.max else 1

        self.content = content


    def train_test(self, train, test):

        labels_train = train.category.apply(lambda x:  int(x=="Criminal") ).values
        labels_test = test.category.apply(lambda x:  int(x=="Criminal") ).values
        #

        #CV grid the hard way...
        scores =[]
        for a in self.alpha:
            avg_fscore = 0.0
            skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=943)
            for train_index, test_index in skf.split(train, labels_train):

                X_train_title = sp.csr_matrix([])
                X_test_title = sp.csr_matrix([])
                X_test_content = sp.csr_matrix([])
                X_train_content = sp.csr_matrix([])

                # Split
                X_train, X_test = train.iloc[train_index], train.iloc[test_index]
                y_train, y_test = labels_train[train_index], labels_train[test_index]

                # Vectorizers
                if self.title:
                    X_train_title, X_test_title = self.vect_fit_transform(X_train, X_test, params=self.title, column="title")
                if self.content:
                    X_train_content, X_test_content = self.vect_fit_transform(X_train, X_test, params=self.content,column="content")
                
                # join both X
                if self.title and self.content:
                    X_train = sp.hstack((X_train_title, X_train_content), format='csr')
                    X_test  = sp.hstack((X_test_title , X_test_content ), format='csr')
                elif self.title:
                    X_train = X_train_title
                    X_test = X_test_title
                elif self.content:
                    X_train = X_train_content
                    X_test = X_test_content

                #fit a classifier
                clf = MultinomialNB(alpha=a)
                clf.fit(X_train, y_train)

                # get scores 
                # y_pred_train = clf.predict(X_train)
                y_pred_test = clf.predict(X_test)
                # prec, rec, f1, supp = precision_recall_fscore_support(y_train,y_pred_train)
                prec, rec, f1, supp = precision_recall_fscore_support(y_test,y_pred_test)

                avg_fscore += f1[1]
            #append fscore
            scores.append( avg_fscore / 5.0 )

        # select best parameter based on score
        max_index = scores.index(max(scores))

        self.best_parameter = self.alpha[max_index]
        # train with all the data using the best param
        self.train_test_all(train, test)


    def train_test_all(self, train, test ):

        labels_train = train.category.apply(lambda x:  int(x=="Criminal") ).values
        labels_test = test.category.apply(lambda x:  int(x=="Criminal") ).values

        X_train_title = sp.csr_matrix([])
        X_test_title = sp.csr_matrix([])
        X_test_content = sp.csr_matrix([])
        X_train_content = sp.csr_matrix([])
        #vectorize
        if self.title:
            X_train_title, X_test_title, self.title_vec = self.vect_fit_transform(train, test, params=self.title, column="title", return_vec=True)
        if self.content:
            X_train_content, X_test_content, self.content_vec = self.vect_fit_transform(train, test, params=self.content, column="content", return_vec=True)

        if self.title and self.content:
            X_train = sp.hstack((X_train_title, X_train_content), format='csr')
            X_test  = sp.hstack((X_test_title , X_test_content ), format='csr')
        elif self.title:
            X_train = X_train_title
            X_test = X_test_title
        elif self.content:
            X_train = X_train_content
            X_test = X_test_content

        self.clf = MultinomialNB(alpha=self.best_parameter)
        self.clf = self.clf.fit(X_train,labels_train )

        #scores
        y_pred_train = self.clf.predict(X_train)
        prec, rec, f1, supp = precision_recall_fscore_support(labels_train,y_pred_train)
        self.precision["train"] = prec[0]
        self.recall["train"] = rec[0]
        self.fscore["train"] = f1[0]

        y_pred_test = self.clf.predict(X_test)
        prec, rec, f1, supp = precision_recall_fscore_support(labels_test, y_pred_test)
        self.precision["test"] = prec[1]
        self.recall["test"] = rec[1]
        self.fscore["test"] = f1[1]

    def predict_log_proba(self, df):
        if self.title:
            X_title = self.title_vec.transform(df.title.values)
        if self.content:
            X_content = self.content_vec.transform(df.content.values)

        if self.title and self.content:
            X = sp.hstack((X_title, X_content), format='csr')
        elif self.title:
            X = X_title
        elif self.content:
            X = X_content
            
        return self.clf.predict_log_proba(X)


    def vect_fit_transform(self, train_df, test_df, params, column, return_vec=False):
        vectorizer = CountVectorizer(
                min_df= params["min"] ,        max_df= params["max"], 
                ngram_range= params["ngram"],  binary= params["binary"],
                #max_features=700,  
                analyzer='char_wb', stop_words=stop_words, 
        )

        vectorizer.fit(train_df[train_df["category"]=="Criminal"][column].values)
        X_train = vectorizer.transform(train_df[column].values)
        X_test = vectorizer.transform(test_df[column].values)
        if return_vec:
            return X_train, X_test, vectorizer
        else:
            return X_train, X_test



    
    def print_scores(self):
        print "Best Parameter: alpha= %0.4f" %self.best_parameter
        print "precision %0.4f, %0.4f" %(self.precision["train"], self.precision["test"])
        print "recall    %0.4f, %0.4f" %(self.recall["train"], self.recall["test"])
        print "fscore    %0.4f, %0.4f" %(self.fscore["train"], self.fscore["test"])
        # print "support   %0.4f, %0.4f" %(self.support["train"], self.support["test"])
