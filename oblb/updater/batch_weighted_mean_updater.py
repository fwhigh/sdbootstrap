from . import Updater
import numpy as np
import pdb

class BatchWeightedMeanUpdater(Updater):

    def __init__(self):
        pass

    def weighted_avg(self,values,weights):
        """
        Return the weighted average and standard deviation.

        values, weights -- Numpy ndarrays with the same shape.
        """
        average = np.average(values, weights=weights)
        return average

    def weighted_std(self,values,weights):
        """
        Return the weighted average and standard deviation.

        values, weights -- Numpy ndarrays with the same shape.
        """
        average = np.average(values, weights=weights)
        variance = np.average((values-average)**2, weights=weights)  # Fast and numerically precise
        return np.sqrt(variance)

    def fake_superlinear_algo(self,values,weights):
        """
        Return the weighted average and standard deviation.

        values, weights -- Numpy ndarrays with the same shape.
        """
        v = 0
        for i in range(len(values)):
            for j in range(len(values)):
                v += 1
        return v


    def batch_update(self,x,w,w_prime,n,conf=None):
        x_arr = np.zeros(int(n))
        WWW_arr = np.zeros(int(n))
        for i in x:
            x_arr[i] = x[i]
            WWW_arr[i] = w[i]*w_prime[i]
        val = self.weighted_avg(x_arr,WWW_arr)
        wht = np.sum(WWW_arr)
        return (val,wht)

    def online_update(self,x1,w1,x2,w2,conf=None):
        val = (w1*x1+w2*x2)/float(w1+w2)
        wht = w1+w2
        return (val,wht)
