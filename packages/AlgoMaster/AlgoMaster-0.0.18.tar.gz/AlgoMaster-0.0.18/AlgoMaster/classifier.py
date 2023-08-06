import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LogisticRegression, RidgeClassifier, SGDClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier, BaggingClassifier, ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import xgboost as xgb
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
import numpy as np
from heapq import nlargest
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV

class Classifier:   
    def __init__(self, X, Y, test_size=0.2, random_state=20):
        self.X = X
        self.Y = Y
        self.sample= None
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(self.X, self.Y, test_size=test_size, stratify=Y, random_state=random_state)
        self.model = [
            LogisticRegression(), KNeighborsClassifier(), GaussianNB(),
            BaggingClassifier(), ExtraTreesClassifier(),
            RidgeClassifier(), SGDClassifier(), RandomForestClassifier(),
            xgb.XGBClassifier(), AdaBoostClassifier(), BernoulliNB(),
            GradientBoostingClassifier(), DecisionTreeClassifier(), SVC()
        ]
        self.model_name = [
            'Logistic Regression', 'KNeighborsClassifier', 'GaussianNB',
            'BaggingClassifier', 'ExtraTreesClassifier', 'RidgeClassifier', 'SGDClassifier',
            'RandomForestClassifier', 'XGBClassifier', 'AdaBoostClassifier',
            'BernoulliNB', 'GradientBoostingClassifier', 'DecisionTreeClassifier', 'SVC'
        ]
        self.model_table = pd.DataFrame(columns=['model name', 'accuracy', 'confusion', 'roc', 'f1', 'recall', 'precision'])
    def format_input_data(self):
        if isinstance(self.sample, np.ndarray):
            if self.sample.ndim == 2 and self.sample.shape[0] == 1:
                return self.sample
            else:
                return self.sample.reshape(1, -1)
        else:
            return np.asarray(self.sample).reshape(1, -1)
    def model_accuracy(self, y_test_f, y_pred_f, model_name):
        acc = accuracy_score(y_test_f, y_pred_f)
        confusion = confusion_matrix(y_test_f, y_pred_f)
        roc = roc_auc_score(y_test_f, y_pred_f)
        f1 = f1_score(y_test_f, y_pred_f)
        recall = recall_score(y_test_f, y_pred_f)
        precision = precision_score(y_test_f, y_pred_f)
        return {'model name': model_name, 'accuracy': acc, 'confusion': confusion, 'roc': roc, 'f1': f1, 'recall': recall, 'precision': precision}
    def model_training(self):
        model_results = []
        for model, model_name in zip(self.model, self.model_name):
            model.fit(self.X_train, self.Y_train)
            y_pred = model.predict(self.X_test)
            model_result = pd.DataFrame([self.model_accuracy(self.Y_test, y_pred, model_name)])
            model_results.append(model_result)
        self.model_table = pd.concat(model_results, ignore_index=True)
        self.model_table = self.model_table.sort_values('accuracy', ascending=False)
        self.model_table.reset_index(drop=True, inplace=True)
        return self.model_table
    def ensemble_prediction(self, count):
        top_models = nlargest(count, self.model_table.iterrows(), key=lambda x: x[1]['accuracy'])
        ensemble_predictions = []
        ensemble_algorithms = []
        for _, model_row in top_models:
            model_index = self.model_name.index(model_row['model name'])
            model = self.model[model_index]
            y_pred = model.predict(self.X_test)
            ensemble_predictions.append((model_index, y_pred))
            ensemble_algorithms.append(model_row['model name'])
        majority_vote = np.apply_along_axis(lambda x: np.argmax(np.bincount(x)), axis=0, arr=np.array([y_pred for _, y_pred in ensemble_predictions]))
        ensemble_name = ', '.join(ensemble_algorithms)
        return self.model_accuracy(self.Y_test, majority_vote, f'Algorithms used for Ensemble [{ensemble_name}]')
    def training(self, model, model_name):
        self.sample = self.format_input_data()
        model.fit(self.X_train, self.Y_train)
        y_pred = model.predict(self.X_test)
        y_predict = model.predict(self.sample)
        return y_predict, self.model_accuracy(self.Y_test, y_pred, model_name)
    def logistic_test(self, pred):
        self.sample = pred
        model = LogisticRegression()
        return self.training(model, 'Logistic Regression')
    def KNeighbors_test(self, pred):
        self.sample=pred
        model = KNeighborsClassifier()
        return self.training(model, 'KNeighborsClassifier')
    def GaussianNB_test(self, pred):
        self.sample=pred
        model = GaussianNB()
        return self.training(model, 'GaussianNB')
    def Bagging_test(self, pred):
        self.sample=pred
        model = BaggingClassifier()
        return self.training(model, 'BaggingClassifier') 
    def ExtraTrees_test(self,pred):
        self.sample=pred
        model = ExtraTreesClassifier()
        return self.training(model, 'ExtraTreesClassifier')
    def Ridge_test(self, pred):
        self.sample=pred
        model = RidgeClassifier()
        return self.training(model, 'RidgeClassifier')
    def SGD_test(self,pred):
        self.sample=pred
        model = SGDClassifier()
        return self.training(model, 'SGDClassifier')   
    def RandomForest_test(self,pred):
        self.sample=pred
        model = RandomForestClassifier()
        return self.training(model, 'RandomForestClassifier')
    def XGB_test(self,pred):
        self.sample=pred
        model = xgb.XGBClassifier()
        return self.training(model, 'XGBClassifier')
    def AdaBoost_test(self, pred):
        self.sample=pred
        model = AdaBoostClassifier()
        return self.training(model, 'AdaBoostClassifier')
    def BernoulliNB_test(self,pred):
        self.sample=pred
        model = BernoulliNB()
        return self.training(model, 'BernoulliNB')
    def GradientBoosting_test(self, pred):
        self.sample=pred
        model = GradientBoostingClassifier()
        return self.training(model, 'GradientBoostingClassifier')
    def DecisionTree_test(self,pred):
        self.sample=pred
        model = DecisionTreeClassifier()
        return self.training(model, 'DecisionTreeClassifier')
    def SVC_test(self,pred):
        self.sample=pred
        model = SVC()
        return self.training(model, 'SVC')
    def hyperparameter_tuning(self):
        model=LogisticRegression()
        param_grid = {
            'C': [0.1, 1, 10, 100, 1000],
            'penalty': ['l2'],
            'tol': [1e-3, 1e-4, 1e-5, 1e-6],
            'fit_intercept': [True, False],
            'intercept_scaling': [1, 10, 100, 1000],
            'class_weight': ['balanced', None],
            'solver': ['newton-cg', 'lbfgs', 'sag', 'saga'],
            'n_jobs': [-1],
            'random_state': [10, 11, 12, 20, 30, 40, 42],
            'warm_start': [True, False],
            'multi_class': ['ovr', 'multinomial', 'auto'],
            'max_iter': [10000,20000,30000]  # Increase max_iter values
        }
        grid_search=RandomizedSearchCV(estimator=model,param_distributions=param_grid,n_iter=5,cv=5,n_jobs=-1,scoring='accuracy')
        grid_search.fit(self.X_train, self.Y_train)
        Y_pred=grid_search.predict(self.X_test)
        lst=[]
        lst.append(self.model_accuracy(self.Y_test, Y_pred,'logistic regression'))
        model=KNeighborsClassifier()
        cv_sets=ShuffleSplit(n_splits=5,test_size=0.2,random_state=42)
        param_grid={
            'n_neighbors':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
            'weights':['uniform','distance'],
            'algorithm':['auto','ball_tree','kd_tree','brute'],
            'leaf_size':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
            'p':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
            'metric':['euclidean','manhattan','chebyshev','minkowski'],
            'n_jobs':[-1],
        }            
        grid_search=RandomizedSearchCV(estimator=model,param_distributions=param_grid,n_iter=5,cv=cv_sets,n_jobs=-1,scoring='accuracy')
        grid_search.fit(self.X_train, self.Y_train)
        Y_pred=grid_search.predict(self.X_test)
        lst.append(self.model_accuracy(self.Y_test, Y_pred,'knn'))   
        model=GaussianNB()
        cv_sets=ShuffleSplit(n_splits=5,test_size=0.2,random_state=42)
        param_grid={
            'var_smoothing':[1e-9,1e-8,1e-7,1e-6,1e-5,1e-4,1e-3,1e-2,1e-1,1,10,100,1000,10000,100000,1000000,10000000,100000000,1000000000],
        }
        grid_search=RandomizedSearchCV(estimator=model,param_distributions=param_grid,n_iter=5,cv=cv_sets,n_jobs=-1,scoring='accuracy')
        grid_search.fit(self.X_train, self.Y_train)
        Y_pred=grid_search.predict(self.X_test)
        lst.append(self.model_accuracy(self.Y_test, Y_pred,'gaussian naive bayes'))
        model=BernoulliNB()
        cv_sets=ShuffleSplit(n_splits=5,test_size=0.2,random_state=42)
        param_grid={
            'alpha':[1e-9,1e-8,1e-7,1e-6,1e-5,1e-4,1e-3,1e-2],
            'binarize':[0,1e-9,1e-8,1e-7,1e-6,1e-5,1e-4,1e-3,1e-2,1e-1,1,10,100,1000,10000,100000,1000000,10000000,100000000,1000000000],
        }
        grid_search=RandomizedSearchCV(estimator=model,param_distributions=param_grid,n_iter=5,cv=cv_sets,n_jobs=-1,scoring='accuracy')
        grid_search.fit(self.X_train, self.Y_train)
        Y_pred=grid_search.predict(self.X_test)
        lst.append(self.model_accuracy(self.Y_test, Y_pred,'bernoulli naive bayes'))
        model=BaggingClassifier()
        cv_sets=ShuffleSplit(n_splits=5,test_size=0.2,random_state=42)
        param_grid={
            'max_samples':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1],
            'max_features':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1],
        }
        grid_search=RandomizedSearchCV(estimator=model,param_distributions=param_grid,n_iter=5,cv=cv_sets,n_jobs=-1,scoring='accuracy')
        grid_search.fit(self.X_train, self.Y_train)
        Y_pred=grid_search.predict(self.X_test)
        lst.append(self.model_accuracy(self.Y_test, Y_pred,'bagging classifier'))
        model=ExtraTreesClassifier()
        cv_sets=ShuffleSplit(n_splits=5,test_size=0.2,random_state=42)
        param_grid={
            'max_depth':[None,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
            'min_samples_leaf':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
            'min_weight_fraction_leaf':[0.0,0.1,0.2,0.3,0.4,0.5],
            'max_features':['sqrt','log2',None],
            'min_impurity_decrease':[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
            'min_samples_split':[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
            'ccp_alpha':[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
        }
        grid_search=RandomizedSearchCV(estimator=model,param_distributions=param_grid,n_iter=5,cv=cv_sets,n_jobs=-1,scoring='accuracy')
        grid_search.fit(self.X_train, self.Y_train)
        Y_pred=grid_search.predict(self.X_test)
        lst.append(self.model_accuracy(self.Y_test, Y_pred,'extra trees classifier'))
        model=RidgeClassifier()
        cv_sets=ShuffleSplit(n_splits=5,test_size=0.2,random_state=42)
        param_grid={
            'alpha':[1e-9,1e-8,1e-7,1e-6,1e-5,1e-4,1e-3,1e-2],
            'fit_intercept':[True,False],
            'copy_X':[True,False],
            'tol':[0.0001,0.001,0.01,0.1,1.0,10.0,100.0,1000.0],
            'random_state':[None,10,11,12,20,30,40,42],
            'positive':[True,False],
            'class_weight':['balanced',None],
        }
        grid_search=RandomizedSearchCV(estimator=model,param_distributions=param_grid,n_iter=5,cv=cv_sets,n_jobs=-1,scoring='accuracy')
        grid_search.fit(self.X_train, self.Y_train)
        Y_pred=grid_search.predict(self.X_test)
        lst.append(self.model_accuracy(self.Y_test, Y_pred,'ridge classifier'))
        model=SGDClassifier()
        cv_sets=ShuffleSplit(n_splits=5,test_size=0.2,random_state=42)
        param_grid={
            'penalty':['l2','l1','elasticnet'],
            'alpha':[0.0001,0.001,0.01,0.1,1.0],
            'tol':[0.0001,0.001,0.01,0.1,1.0],
            'epsilon':[0.0001,0.001,0.01,0.1,1.0,10.0,100.0,1000.0],
            'learning_rate':['optimal','constant','invscaling','adaptive'],
            'eta0':[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
            'power_t':[0.5,0.6,0.7,0.8,0.9,1.0],
            'n_iter_no_change':[5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100],
            'class_weight':['balanced',None],
        }
        grid_search=RandomizedSearchCV(estimator=model,param_distributions=param_grid,n_iter=5,cv=cv_sets,n_jobs=-1,scoring='accuracy')
        grid_search.fit(self.X_train, self.Y_train)
        Y_pred=grid_search.predict(self.X_test)
        lst.append(self.model_accuracy(self.Y_test, Y_pred,'sgd classifier'))
        model=RandomForestClassifier()
        cv_sets=ShuffleSplit(n_splits=5,test_size=0.2,random_state=42)
        param_grid={
            'n_estimators':[10,20,30,40,50,60,70,80,90,100],
            'criterion':['gini','entropy','log_loss'],
            'max_depth':[None,10,20,30,40,50,60,70,80,90,100],
            'min_samples_split':[2,3,4,5,6,7,8,9,10],
            'min_samples_leaf':[1,2,3,4,5,6,7,8,9,10],
            'min_weight_fraction_leaf':[0.0,0.1,0.2,0.3,0.4,0.5],
            'max_features':['sqrt','log2'],
            'max_leaf_nodes':[None,10,20,30,40,50,60,70,80,90,100],
            'ccp_alpha':[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
            'max_samples':[None,10,20,30,40,50,60,70,80,90,100],
        }
        grid_search=RandomizedSearchCV(estimator=model,param_distributions=param_grid,n_iter=5,cv=cv_sets,n_jobs=-1,scoring='accuracy')
        grid_search.fit(self.X_train, self.Y_train)
        Y_pred=grid_search.predict(self.X_test)
        lst.append(self.model_accuracy(self.Y_test, Y_pred,'random forest classifier'))
        model=xgb.XGBClassifier()
        cv_sets=ShuffleSplit(n_splits=5,test_size=0.2,random_state=42)
        param_grid={
            'max_depth':[3,4,5,6,7,8,9,10],
            'learning_rate':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
            'subsample':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
            'colsample_bytree':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
            'colsample_bylevel':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
            'reg_alpha':[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
            'reg_lambda':[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
        }
        grid_search=RandomizedSearchCV(estimator=model,param_distributions=param_grid,n_iter=5,cv=cv_sets,n_jobs=-1,scoring='accuracy')
        grid_search.fit(self.X_train, self.Y_train)
        Y_pred=grid_search.predict(self.X_test)
        lst.append(self.model_accuracy(self.Y_test, Y_pred,'xgboost classifier'))
        model=AdaBoostClassifier()
        cv_sets=ShuffleSplit(n_splits=5,test_size=0.2,random_state=42)
        cv_sets=ShuffleSplit(n_splits=5,test_size=0.2,random_state=42)
        param_grid={
            'learning_rate':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
            'algorithm':['SAMME.R'],
            'random_state':[None,10,11,12,20,30,40,42],
        }
        grid_search=RandomizedSearchCV(estimator=model,param_distributions=param_grid,n_iter=5,cv=cv_sets,n_jobs=-1,scoring='accuracy')
        grid_search.fit(self.X_train, self.Y_train)
        Y_pred=grid_search.predict(self.X_test)
        lst.append(self.model_accuracy(self.Y_test, Y_pred,'ada boost classifier'))
        model=GradientBoostingClassifier()
        cv_sets=ShuffleSplit(n_splits=5,test_size=0.2,random_state=42)
        param_grid={
            'learning_rate':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
            'n_estimators':[10,20,30,40,50,60,70,80,90,100,200,300,400,500,600,700,800,900,1000],
            'subsample':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
            'min_samples_split':[2,3,4,5,6,7,8,9,10],
            'min_samples_leaf':[1,2,3,4,5,6,7,8,9,10],
            'max_depth':[3,4,5,6,7,8,9,10],
        }
        grid_search=RandomizedSearchCV(estimator=model,param_distributions=param_grid,n_iter=5,cv=cv_sets,n_jobs=-1,scoring='accuracy')
        grid_search.fit(self.X_train, self.Y_train)
        Y_pred=grid_search.predict(self.X_test)
        lst.append(self.model_accuracy(self.Y_test, Y_pred,'gradient boosting classifier'))
        model=SVC()
        cv_sets=ShuffleSplit(n_splits=5,test_size=0.2,random_state=42)
        param_grid={
            'C':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
            'kernel':['rbf'],
            'degree':[3,4,5,6,7,8,9,10],
            'gamma':['scale','auto'],
            'random_state':[None,10,11,12,20,30,40,42],
        }
        grid_search=RandomizedSearchCV(estimator=model,param_distributions=param_grid,n_iter=5,cv=cv_sets,n_jobs=-1,scoring='accuracy')
        grid_search.fit(self.X_train, self.Y_train)
        Y_pred=grid_search.predict(self.X_test)
        lst.append(self.model_accuracy(self.Y_test, Y_pred,'svc'))
        model=DecisionTreeClassifier()
        cv_sets=ShuffleSplit(n_splits=5,test_size=0.2,random_state=42)
        param_grid={
            'criterion':['gini'],
            'splitter':['best'],
            'max_depth':[None],
            'min_samples_split':[2,3,4,5,6,7,8,9,10],
            'min_samples_leaf':[1,2,3,4,5,6,7,8,9,10],
            'min_weight_fraction_leaf':[0.0],
            'max_features':[None],
            'random_state':[None,10,11,12,20,30,40,42],
            'max_leaf_nodes':[None],
            'min_impurity_decrease':[0.0],
            'class_weight':[None],
            'ccp_alpha':[0.0],
        }
        grid_search=GridSearchCV(model,param_grid,cv=5,n_jobs=-1)
        grid_search.fit(self.X_train, self.Y_train)
        Y_pred=grid_search.predict(self.X_test)
        lst.append(self.model_accuracy(self.Y_test, Y_pred,'decision tree classifier'))
        return pd.DataFrame(lst,columns=['model name','accuracy','confusion','roc','f1','recall','precision'])
    def hyper_training(self, model, model_name,parameters):
        self.sample = self.format_input_data()
        cv_sets=ShuffleSplit(n_splits=5,test_size=0.2,random_state=42)
        grid_search=RandomizedSearchCV(estimator=model,param_distributions=parameters,n_iter=5,cv=cv_sets,n_jobs=-1,scoring='accuracy')
        grid_search.fit(self.X_train, self.Y_train)
        y_pred=grid_search.predict(self.X_test)
        y_predict=grid_search.predict(self.sample)
        return y_predict, self.model_accuracy(self.Y_test, y_pred,model_name)
    def logistic_hyperparameter(self,pred):
        self.sample = pred
        model=LogisticRegression()
        param_grid = {
            'C': [0.1, 1, 10, 100, 1000],
            'penalty': ['l2'],
            'tol': [1e-3, 1e-4, 1e-5, 1e-6],
            'fit_intercept': [True, False],
            'intercept_scaling': [1, 10, 100, 1000],
            'class_weight': ['balanced', None],
            'solver': ['newton-cg', 'lbfgs', 'sag', 'saga'],
            'n_jobs': [-1],
            'random_state': [10, 11, 12, 20, 30, 40, 42],
            'warm_start': [True, False],
            'multi_class': ['ovr', 'multinomial', 'auto'],
            'max_iter': [10000,20000,30000]  # Increase max_iter values
        }
        return self.hyper_training(model, 'logistic regression',param_grid)
    def knn_hyperparameter(self,pred):
        self.sample=pred
        model=KNeighborsClassifier()
        param_grid={
            'n_neighbors':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
            'weights':['uniform','distance'],
            'algorithm':['auto','ball_tree','kd_tree','brute'],
            'leaf_size':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
            'p':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
            'metric':['euclidean','manhattan','chebyshev','minkowski'],
            'n_jobs':[-1],
        }           
        return self.hyper_training(model, 'knn',param_grid)
    def gaussian_nb_hyperparameter(self,pred):
        self.sample=pred
        model=GaussianNB()
        param_grid={
            'var_smoothing':[1e-9,1e-8,1e-7,1e-6,1e-5,1e-4,1e-3,1e-2,1e-1,1,10,100,1000,10000,100000,1000000,10000000,100000000,1000000000],
        }
        return self.hyper_training(model, 'gaussian naive bayes',param_grid)
    def bernoulli_nb_hyperparameter(self,pred):
        self.sample=pred
        model=BernoulliNB()
        param_grid={
            'alpha':[1e-9,1e-8,1e-7,1e-6,1e-5,1e-4,1e-3,1e-2],
            'binarize':[0,1e-9,1e-8,1e-7,1e-6,1e-5,1e-4,1e-3,1e-2,1e-1,1,10,100,1000,10000,100000,1000000,10000000,100000000,1000000000],
        }
        return self.hyper_training(model, 'bernoulli naive bayes',param_grid)
    def bagging_hyperparameter(self,pred):
        self.sample=pred
        model=BaggingClassifier()
        cv_sets=ShuffleSplit(n_splits=5,test_size=0.2,random_state=42)
        param_grid={
            'max_samples':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1],
            'max_features':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1],
        }
        return self.hyper_training(model, 'bagging',param_grid)
    def extra_trees_hyperparameter(self,pred):
        self.sample=pred
        model=ExtraTreesClassifier()
        param_grid={
            'max_depth':[None,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
            'min_samples_leaf':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
            'min_weight_fraction_leaf':[0.0,0.1,0.2,0.3,0.4,0.5],
            'max_features':['sqrt','log2',None],
            'min_impurity_decrease':[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
            'min_samples_split':[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
            'ccp_alpha':[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
        }
        return self.hyper_training(model, 'extra trees',param_grid)
    def ridge_hyperparameter(self,pred):
        self.sample=pred
        model=RidgeClassifier()
        param_grid={
            'alpha':[1e-9,1e-8,1e-7,1e-6,1e-5,1e-4,1e-3,1e-2],
            'fit_intercept':[True,False],
            'copy_X':[True,False],
            'tol':[0.0001,0.001,0.01,0.1,1.0,10.0,100.0,1000.0],
            'random_state':[None,10,11,12,20,30,40,42],
            'positive':[True,False],
            'class_weight':['balanced',None],
        }
        return self.hyper_training(model, 'ridge',param_grid)
    def sgd_hyperparameter(self,pred):
        self.sample=pred
        model=SGDClassifier()
        param_grid={
            'penalty':['l2','l1','elasticnet'],
            'alpha':[0.0001,0.001,0.01,0.1,1.0],
            'tol':[0.0001,0.001,0.01,0.1,1.0],
            'epsilon':[0.0001,0.001,0.01,0.1,1.0,10.0,100.0,1000.0],
            'learning_rate':['optimal','constant','invscaling','adaptive'],
            'eta0':[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
            'power_t':[0.5,0.6,0.7,0.8,0.9,1.0],
            'n_iter_no_change':[5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100],
            'class_weight':['balanced',None],
        }
        return self.hyper_training(model, 'sgd',param_grid)
    def random_forest_hyperparameter(self,pred):
        self.sample=pred
        model=RandomForestClassifier()
        param_grid={
            'n_estimators':[10,20,30,40,50,60,70,80,90,100],
            'criterion':['gini','entropy','log_loss'],
            'max_depth':[None,10,20,30,40,50,60,70,80,90,100],
            'min_samples_split':[2,3,4,5,6,7,8,9,10],
            'min_samples_leaf':[1,2,3,4,5,6,7,8,9,10],
            'min_weight_fraction_leaf':[0.0,0.1,0.2,0.3,0.4,0.5],
            'max_features':['sqrt','log2'],
            'max_leaf_nodes':[None,10,20,30,40,50,60,70,80,90,100],
            'ccp_alpha':[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
            'max_samples':[None,10,20,30,40,50,60,70,80,90,100],
        }
        return self.hyper_training(model, 'random forest',param_grid)
    def xgb_hyperparameter(self,pred):
        self.sample=pred
        model=xgb.XGBClassifier()
        param_grid={
            'max_depth':[3,4,5,6,7,8,9,10],
            'learning_rate':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
            'subsample':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
            'colsample_bytree':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
            'colsample_bylevel':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
            'reg_alpha':[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
            'reg_lambda':[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
        }
        return self.hyper_training(model, 'xgboost',param_grid)
    def ada_boost_hyperparameter(self,pred):
        self.sample=pred
        model=AdaBoostClassifier()
        param_grid={
            'learning_rate':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
            'algorithm':['SAMME.R'],
            'random_state':[None,10,11,12,20,30,40,42],
        }
        return self.hyper_training(model, 'adaboost',param_grid)
    def gradient_boosting_hyperparameter(self,pred):
        self.sample=pred
        model=GradientBoostingClassifier()
        param_grid={
            'learning_rate':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
            'n_estimators':[10,20,30,40,50,60,70,80,90,100,200,300,400,500,600,700,800,900,1000],
            'subsample':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
            'min_samples_split':[2,3,4,5,6,7,8,9,10],
            'min_samples_leaf':[1,2,3,4,5,6,7,8,9,10],
            'max_depth':[3,4,5,6,7,8,9,10],
        }
        return self.hyper_training(model, 'gradient boosting',param_grid)
    def svc_hyperparameter(self,pred):
        self.sample=pred
        model=SVC()
        param_grid={
            'C':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
            'kernel':['rbf'],
            'degree':[3,4,5,6,7,8,9,10],
            'gamma':['scale','auto'],
            'random_state':[None,10,11,12,20,30,40,42],
        }
        return self.hyper_training(model, 'svc',param_grid)
    def decision_tree_hyperparameter(self,pred):
        self.sample=pred
        model=DecisionTreeClassifier()
        param_grid={
            'min_samples_split':[2,3,4,5,6,7,8,9,10],
            'min_samples_leaf':[1,2,3,4,5,6,7,8,9,10],
            'min_weight_fraction_leaf':[0.0],
            'random_state':[None,10,11,12,20,30,40,42],
            'min_impurity_decrease':[0.0],
            'ccp_alpha':[0.0],
        }
        return self.hyper_training(model, 'decision tree',param_grid)
        
    
    
        