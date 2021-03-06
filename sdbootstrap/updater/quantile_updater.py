from . import Updater
import numpy as np

class QuantileUpdater(Updater):

    def __init__(self):
        pass

    def online_update(self,x1,w1,x2,w2,conf=None):
        val=x1
        for i in range(int(w2)):
            r=np.random.rand()
            if x2 > val and r > 1-conf.quantile:
                val = val + 1/conf.precision
            elif x2 < val and r < 1-conf.quantile:
                val = val - 1/conf.precision
        wht=w1+w2
        return (val,wht)