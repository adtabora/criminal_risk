from sklearn.metrics import f1_score, make_scorer, classification_report, precision_recall_fscore_support
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV


class Classifier:
    def __init__(self,clf, params, labels=None):
        self.labels = labels
        f_one_scorer = make_scorer(f1_score,labels=[0], average="weighted")
        self.clf =  GridSearchCV(clf, params, cv=5, scoring= f_one_scorer, verbose=1, n_jobs=4 )
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
        print classification_report(y_train, preds_train ,target_names=self.labels, labels=range(0,self.labels.shape[0]) )
        
        print "- Test Results -"
        preds_test = self.clf.predict(X_test)
        print classification_report(y_test, preds_test,target_names=self.labels, labels=range(0,self.labels.shape[0]))

        #score
        train_scores = precision_recall_fscore_support(y_train, preds_train, labels=range(0,self.labels.shape[0]))
       
        test_scores = precision_recall_fscore_support(y_test, preds_test, labels=range(0,self.labels.shape[0]))

        def format_result(scores):
            data = []
            for i in range(0,self.labels.shape[0]):
                data.append({
                    "precision": scores[0][i],
                    "recall": scores[1][i],
                    "fscore": scores[2][i],
                    "support": scores[3][i],
                })
            return data
                

        score = {
            "labels": self.labels.tolist(),
            "train": format_result(train_scores),
            "test": format_result(test_scores)
        }
        return preds_train, preds_test, score

    # Only return predictions
    def predict(self, X):
        return self.clf.predict(X)


def initialize_classifiers(labels):
    # LVL 1 classifiers 

    lvl_1_classifiers = []

    

    # Classifier 1: sklearn.svm.SVC  0.25
    # from sklearn.svm import SVC
    # parameters = {}
    # svc_clf = SVC(random_state = 452)
    # lvl_1_classifiers.append(Classifier(svc_clf, parameters,labels) )

    # Classifier 2:  K neightbors 0.25 
    # from sklearn.neighbors import KNeighborsClassifier
    # parameters = {}
    # neigh = KNeighborsClassifier(n_jobs=4)
    # lvl_1_classifiers.append(Classifier(neigh, parameters,labels) )


    # Classifier 0: Random Forest
    parameters = {
        "n_estimators": [1000],
        "max_depth": [10], #[3,4,5,8,10,20],
        "min_samples_split" : [4]
    }
    rfc = RandomForestClassifier(random_state= 233, n_jobs=4)
    lvl_1_classifiers.append(Classifier(rfc, parameters,labels) )

    # Classifier 3:  Gradient Tree Boosting 0.00 
    # from sklearn.ensemble import GradientBoostingClassifier
    # gbc = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=324)
    # parameters = {}
    # lvl_1_classifiers.append(Classifier(gbc, parameters,labels) )

    # Classifier 4:  LogisticRegression 0.39 
    from sklearn.linear_model import LogisticRegression
    parameters = {"C":[10, 1.0, 0.1, 0.01]}
    lrc = LogisticRegression(penalty="l1", random_state=238, n_jobs=4, )
    lvl_1_classifiers.append(Classifier(lrc, parameters,labels) )


    # LVL 2 Classifier
    # parameters = {
    #     "n_estimators": [200],
    #     "max_depth": [20],
    #     "min_samples_split" : [4]
    # }
    # rfc = RandomForestClassifier(random_state= 233, n_jobs=4)

    # from sklearn.linear_model import LogisticRegression
    parameters = {"C":[10, 1.0, 0.1, 0.01]}
    rfc = LogisticRegression(penalty="l1", random_state=238, n_jobs=4)


    lvl2 = Classifier(rfc, parameters, labels)

    return lvl_1_classifiers, lvl2