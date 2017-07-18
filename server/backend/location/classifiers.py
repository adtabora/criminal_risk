from sklearn.metrics import f1_score, make_scorer, classification_report, precision_recall_fscore_support
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler


class Classifier:
    def __init__(self,clf, params, labels=None, scaler=None):
        self.labels = labels
        f_one_scorer = make_scorer(f1_score,labels=[0], average="weighted")
        self.clf =  GridSearchCV(clf, params, cv=5, scoring= f_one_scorer, verbose=5, n_jobs=4 )
    
        if scaler == None:
            self.scaler = None
        elif scaler == "min_max":
            self.scaler = MinMaxScaler()
        elif scaler == "standard":
            self.scaler = StandardScaler()
        elif scaler == "robust":
            self.scaler = RobustScaler()

        

    
    #train the classifier and print results
    def train(self, X, y, scores=False):
        if self.scaler != None:
            X = self.scaler.fit_transform(X)
        self.clf.fit(X, y)
        if scores:
            print self.clf.best_score_
            print self.clf.best_params_
            print self.clf.cv_results_['mean_train_score']
            print self.clf.cv_results_['mean_test_score']

    # predict and print scores. It returns the predictions
    def predict_score(self, X_train, y_train, X_test, y_test):
        if self.scaler != None:
            X_train = self.scaler.transform(X_train)
            X_test = self.scaler.transform(X_test)
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
        if self.scaler != None:
            X = self.scaler.transform(X)
        return self.clf.predict(X)


def initialize_classifiers(labels):
    # LVL 1 classifiers 

    lvl_1_classifiers = []

    # Classifier 0: Random Forest
    # parameters = {
    #     "n_estimators": [200],
    #     "max_depth": [20], #[3,4,5,8,10,20],
    #     "min_samples_split" : [4]
    # }
    # rfc = RandomForestClassifier(random_state= 233, n_jobs=4)
    # lvl_1_classifiers.append(Classifier(rfc, parameters,labels) )

    # Classifier 1:  LogisticRegression 0.39 
    # from sklearn.linear_model import LogisticRegression
    # parameters = {"C":[ 1.0, 0.5, 0.1, 0.08 ,0.05]}
    # lrc = LogisticRegression(penalty="l1", random_state=238, n_jobs=4, )
    # lvl_1_classifiers.append(Classifier(lrc, parameters,labels) )

    

    # Classifier 2:  K neightbors 0.35 probably needs some feature normalization
    # from sklearn.neighbors import KNeighborsClassifier
    # parameters = {
    #     "weights":["distance"],
    #     "n_neighbors":[10],#[3,5,8,10,20,40],
    #     }
    # neigh = KNeighborsClassifier(n_jobs=4)
    # lvl_1_classifiers.append(Classifier(neigh, parameters,labels,scaler="min_max" ) )


    # Classifier 3:  Gradient Tree Boosting 0.79 with 0.1, 4, 200
    # from sklearn.ensemble import GradientBoostingClassifier
    # gbc = GradientBoostingClassifier(n_estimators=500,  random_state=324,verbose=0)
    # parameters = {
    #     "learning_rate":[0.1],#[1,0.5,0.1,0.05], 
    #     "max_depth":[4],#[3,4,8,10,20]
    #     }
    # lvl_1_classifiers.append(Classifier(gbc, parameters,labels) )

    # Classifier 4: sklearn.svm.SVC  0.25
    from sklearn.svm import SVC
    parameters = {
        "C":[100]#[100.0,20.0,10.0]
    }
    svc_clf = SVC(random_state = 452)
    lvl_1_classifiers.append(Classifier(svc_clf, parameters,labels,scaler="min_max" ) )



    # LVL 2 Classifier
    parameters = {
        "n_estimators": [200],
        "max_depth": [20],
        "min_samples_split" : [4]
    }
    clf = RandomForestClassifier(random_state= 233, n_jobs=4)

    # from sklearn.linear_model import LogisticRegression
    # parameters = {"C":[10, 1.0, 0.1, 0.01]}
    # clf = LogisticRegression(penalty="l1", random_state=238, n_jobs=4)

    # from sklearn import tree
    # parameters = {}
    # clf = tree.DecisionTreeClassifier()


    lvl2 = Classifier(clf, parameters, labels)

    return lvl_1_classifiers, lvl2