from oblb.bootstrap import Bootstrap
from oblb.config import Config
import oblb.updater

import numpy as np

# from sklearn.linear_model import ElasticNet
# from sklearn.linear_model import LinearRegression
# from sklearn.tree import DecisionTreeRegressor
# from sklearn.ensemble import AdaBoostRegressor
# from sklearn.ensemble import GradientBoostingRegressor
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.ensemble import ExtraTreesRegressor
# from sklearn.dummy import DummyRegressor
# from sklearn.linear_model import ARDRegression
# from sklearn.svm import SVR

from sklearn.datasets import load_svmlight_file

import sklearn.linear_model
import sklearn.tree
import sklearn.ensemble
import sklearn.dummy

import pdb

class MLInnerBootstrap(Bootstrap):

    def __init__(self):
        pass

    def main(self):
        conf = Config()

        X_test, y_test = load_svmlight_file(conf.test_file)
        X, y = load_svmlight_file(conf.infile)
        n = len(y)

        if conf.model in set(['ElasticNet','LinearRegression']):
            model = getattr(sklearn.linear_model,conf.model)()
        elif conf.model in set(['GradientBoostingRegressor']):
            model = getattr(sklearn.ensemble,conf.model)(
                learning_rate=0.001,
                n_estimators=10000,
                min_samples_leaf=10,
                min_samples_split=100,
                max_depth=2,
                subsample=0.5,
                loss='ls'
                )
            X = X.toarray()
            X_test = X_test.toarray()
        elif conf.model in set(['AdaBoostRegressor']):
            model = getattr(sklearn.ensemble,conf.model)()
            X = X.toarray()
            X_test = X_test.toarray()
        elif conf.model in set(['DummyRegressor']):
            model = getattr(sklearn.dummy,conf.model)()
        else:
            raise("don't recognize model %s" % (conf.model,))

        for k in range(conf.n_boot):
            booti = np.random.randint(0,n,n)
            model.fit(X[booti,:],y[booti])
            y_score = model.predict(X_test)

#            print(separator.join([str(k),str(theta[k]),str(w[k])]))
            for j in range(len(y_score)):
                # key = conf.composite_key_separator.join([str(k),str(j)])
                key = conf.composite_key_separator.join([str(j)])
                print(conf.separator.join([str(key),str(y_score[j]),str(1)]))
