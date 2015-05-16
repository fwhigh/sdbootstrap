from . import Updater
import pdb

class MedianUpdater(Updater):

    def __init__(self):
        pass

    def batch_update(self,x,w,w_prime,conf=None):
        val = 0.0
        wht = 0.0
        for j in range(len(x)):
            WWW = w[j]*w_prime[j]
            for i in range(int(WWW)):
                if x[j] > val:
                    val = val + 1/conf.precision
                elif x[j] < val:
                    val = val - 1/conf.precision
            wht += WWW
        return (val,wht)


    def online_update(self,x1,w1,x2,w2,conf=None):
        val = x1
        for i in range(int(w2)):
            if x2 > val:
                val = val + 1/conf.precision
            elif x2 < val:
                val = val - 1/conf.precision
        wht=w1+w2
        return (val,wht)
