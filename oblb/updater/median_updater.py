from . import Updater
import pdb

class MedianUpdater(Updater):

    def __init__(self):
        pass

    def online_update(self,x1,w1,x2,w2,conf=None):
        if x2 > x1:
            x1 += 1/conf.precision
        elif x2 < x1:
            x1 -= 1/conf.precision
        w1=w1+w2
        return (x1,w1)
