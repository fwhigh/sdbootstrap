from abc import ABCMeta, abstractmethod

class Updater(object):
    '''
    Abstract base class for updaters.
    '''

    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def online_update(self,x1,w1,x2,w2,conf=None):
        '''
        Online update rule.
        '''
        pass
