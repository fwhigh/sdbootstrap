from oblb.bootstrap import Bootstrap
from oblb.config import Config
import oblb.updater
import numpy as np
import pdb

class InnerBootstrap(Bootstrap):

    def __init__(self):
        pass

    def poisson(self,randu):
        if randu < 0.3678794:
            return 0
        elif randu < 0.7357589:
            return 1
        elif randu < 0.9196986:
            return 2
        elif randu < 0.9810118:
            return 3
        elif randu < 0.9963402:
            return 4
        elif randu < 0.9994058:
            return 5
        elif randu < 0.9999168:
            return 6
        elif randu < 0.9999898:
            return 7
        elif randu < 0.9999989:
            return 8
        elif randu < 0.9999999:
            return 9
        else:
            return 10

    def batch_update_bootstrap(self,
                               theta_boot,
                               w_boot,
                               infile=None,
                               separator=None,
                               batch_update=None,
                               conf=None):
        X_dict = dict()
        w_prime_dict = dict()
        i=0
        for line in infile:
            field = line.split(separator)
            X_dict[i] = float(field[0])
            w_prime_dict[i] = float(field[1])
            i += 1
        n = i
        X = np.zeros(n)
        w_prime = np.zeros(n)
        for i in range(n):
            X[i] = X_dict[i]
            w_prime[i] = w_prime_dict[i]
        for k in range(len(theta_boot)):
            booti = np.random.randint(0,n-1,n)
            (theta_boot[k],w_boot[k])=batch_update(X[booti],w_prime[booti],conf=conf)

    def update_bootstrap(self,
                         theta_boot,
                         w_boot,
                         infile=None,
                         separator=None,
                         online_update=None,
                         conf=None):
        for line in infile:
            field = line.split(separator)
            X = float(field[0])
            w_prime = float(field[1])
            for k in range(len(theta_boot)):
                #w = w_prime*np.random.poisson(lam=1.0)
                w = w_prime*self.poisson(np.random.rand())
                if w == 0:
                    continue
                (theta_boot[k],w_boot[k])=online_update(theta_boot[k],w_boot[k],X,w,conf=conf)

    def main(self):
        conf = Config()
        (theta_boot,w_boot) = self.init_boot(n_boot=conf.n_boot)
        if conf.batch_update is not '':
            updater = getattr(oblb.updater,conf.batch_update)()
            self.batch_update_bootstrap(theta_boot,w_boot,
                                        infile=conf.infile,
                                        separator=conf.separator,
                                        batch_update=updater.batch_update,
                                        conf=conf)
        else:
            updater = getattr(oblb.updater,conf.online_update)()
            self.update_bootstrap(theta_boot,w_boot,
                                  infile=conf.infile,
                                  separator=conf.separator,
                                  online_update=updater.online_update,
                                  conf=conf)
        self.print_bootstrap(theta_boot,w_boot,separator=conf.separator)
