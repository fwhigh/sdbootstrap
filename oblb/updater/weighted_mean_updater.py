from . import Updater
import numpy as np
import pdb

class WeightedMeanUpdater(Updater):

    def __init__(self):
        pass

    def batch_update(self,x,w,w_prime,n,conf=None):
        # val = np.sum(w2*x2)/np.sum(w2)
        # wht = np.sum(w2)
        num = 0.0
        wht = 0.0
        for i in range(len(x)):
            num += w_prime[i]*w[i]*x[i]
            wht += w_prime[i]*w[i]
        val = num/float(wht)
        return (val,wht)

    def online_update(self,x1,w1,x2,w2,conf=None):
        val = (w1*x1+w2*x2)/float(w1+w2)
        wht = w1+w2
        return (val,wht)
