from . import Updater

class WeightedMeanUpdater(Updater):

    def __init__(self):
        pass

    def online_update(self,x1,w1,x2,w2,conf=None):
        x1 = (w1*x1+w2*x2)/(w1+w2)
        w1 = w1+w2
        return (x1,w1)
