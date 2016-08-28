from . import Updater
import numpy as np
import pdb

class SuperlinearUpdater(Updater):

    def __init__(self):
        pass

    def superlinear_algo(self,values,weights):
        """
        N^2
        """
        v = 0.0
        for i in range(len(values)**3):
            v += 1.0
        return v


    def batch_update(self,x,w,w_prime,n,conf=None):
        val = self.superlinear_algo(x,w)
        wht = 1
        return (val,wht)

    def online_update(self,x1,w1,x2,w2,conf=None):
        val = x1+1.0
        wht = w1+float(w2)
        return (val,wht)
