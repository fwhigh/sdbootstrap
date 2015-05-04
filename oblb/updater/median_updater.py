from . import Updater
import pdb

class MedianUpdater(Updater):

    def __init__(self):
        pass

    def online_update(self,x1,w1,x2,w2,conf=None):
        m=x1*1
        if x2 > x1:
            m += 1/conf.precision
        elif x2 < x1:
            m -= 1/conf.precision
        return (m,w1+w2)
