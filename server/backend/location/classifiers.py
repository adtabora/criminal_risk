from sklearn.metrics import f1_score, make_scorer, classification_report, precision_recall_fscore_support
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV


class Classifier:
    def __init__(self,clf, params):
        f_one_scorer = make_scorer(f1_score,average="weighted", labels=[0,1] )
        self.clf =  GridSearchCV(clf, params, cv=5, scoring= f_one_scorer, verbose=1 )
    #train the classifier and print results
    def train(self, X, y, scores=False):
        self.clf.fit(X, y)
        if scores:
            print self.clf.best_score_
            print self.clf.best_params_
            print self.clf.cv_results_['mean_train_score']
            print self.clf.cv_results_['mean_test_score']

    # predict and print scores. It returns the predictions
    def predict_score(self, X_train, y_train, X_test, y_test):
        print "- Train Results -"
        preds_train = self.clf.predict(X_train)
        print(classification_report(y_train, preds_train,labels=[0,1]))
        
        print "- Test Results -"
        preds_test = self.clf.predict(X_test)
        print(classification_report(y_test, preds_test,labels=[0,1]))

        #score
        train_scores = precision_recall_fscore_support(y_train, preds_train,labels=[0,1])
       
        test_scores = precision_recall_fscore_support(y_test, preds_test,labels=[0,1])

        def format_result(scores):
            data = []
            for i in range(0,2):
                data.append({
                    "precision": scores[0][i],
                    "recall": scores[1][i],
                    "fscore": scores[2][i],
                    "support": scores[3][i],
                })
            return data
                

        score = {
            "train": format_result(train_scores),
            "test": format_result(test_scores)
        }
        return preds_train, preds_test, score

    # Only return predictions
    def predict(self, X):
        return self.clf.predict(X)


def initialize_classifiers():
    # LVL 1 classifiers 

    lvl_1_classifiers = []

    # Classifier 0: Random Forest
    parameters = {
        "n_estimators": [200],
        "max_depth": [20],
        "min_samples_split" : [4]
    }
    rfc = RandomForestClassifier(random_state= 233, n_jobs=4)
    lvl_1_classifiers.append(Classifier(rfc, parameters) )


    # LVL 2 Classifier
    parameters = {
        "n_estimators": [200],
        "max_depth": [20],
        "min_samples_split" : [4]
    }
    rfc = RandomForestClassifier(random_state= 233, n_jobs=4)

    lvl2 = Classifier(rfc, parameters)

    return lvl_1_classifiers, lvl2