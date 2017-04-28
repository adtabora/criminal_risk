from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

import pickle


def getXY(df):
    print "- get X and Y"
    X = df.drop("NE",1).values
    y = df.NE.values
    
    return X, y

def train_classifier(X,y, cv=False ):
    print "- train classifier"
    clf = RandomForestClassifier(n_estimators=100, random_state= 233, n_jobs=2)
    
    #If it doesn't require to cross validate
    clf.fit(X, y)
    print "train score: %0.6f" %clf.score(X,y)
    return clf
        

def test_classifier(clf,X_test,y_test):
    print "test score: %0.6f" %clf.score(X_test,y_test)
    print

    preds = clf.predict(X_test)
    print confusion_matrix(y_test, preds)
    print 

    print(classification_report(y_test, preds))
    print




def train(train_df, test_df):
    print "-- Training Tagger"

    X_train, y_train = getXY(train_df)
    X_test, y_test = getXY(test_df)

    #Train and test
    clf = train_classifier(X_train,y_train)
    test_classifier(clf,X_test,y_test)

    #4. save classifier
    print "- saving identifier"
    pickle.dump( clf, open( "./files/identifier.p", "wb" ) )

    print "- Done."

def predict(features_df):
    print "-- Predicting Named Entities"

    print "- loading identifier"
    clf = pickle.load( open( "./files/identifier.p", "rb" ) )

    print "- predicting"
    X_pred = features_df.values
    y_pred = clf.predict(X_pred)

    return y_pred

