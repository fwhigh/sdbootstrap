from oblb.bootstrap import Bootstrap
from oblb.config import Config
import oblb.updater
import numpy as np
import sys
import pdb

class InnerBootstrap(Bootstrap):

    def __init__(self):
        pass

    def batch_update_bootstrap(self,
                               theta_boot,
                               w_boot,
                               infile=None,
                               separator=None,
                               batch_update=None,
                               conf=None,
                               use_np_multinomial=False):
        X_dict = dict()
        w_dict = dict()
        i=0
        for line in infile:
            if ''.join(line.split()) == '':
                continue
            field = line.split(separator)
            X_dict[i] = float(field[0])
            w_dict[i] = float(field[1])
            i += 1
        n = i
        if use_np_multinomial:
            p = np.repeat(1/float(n),n)
        w_prime = np.zeros(n)
        for k in range(conf.n_boot):
            if use_np_multinomial:
                w_prime = np.random.multinomial(n,p)
            else:
                w_prime = self.multinomial(n)
            (theta_boot[k],w_boot[k])=batch_update(X_dict,w_dict,w_prime,n,conf=conf)

    def update_bootstrap(self,
                         theta_boot,
                         w_boot,
                         infile=None,
                         separator=None,
                         online_update=None,
                         conf=None,
                         use_np_poisson=True):
        for line in infile:
            if ''.join(line.split()) == '':
                continue
            field = line.split(separator)
            X = float(field[0])
            w = float(field[1])
            for k in range(conf.n_boot):
                if k not in theta_boot:
                    theta_boot[k] = 0.0
                    w_boot[k] = 0.0
                if use_np_poisson:
                    w_prime = w*np.random.poisson(lam=1.0)
                else:
                    w = w_prime*self.poisson(np.random.rand())
                if w_prime == 0:
                    continue
                (theta_boot[k],w_boot[k])=online_update(theta_boot[k],w_boot[k],X,w_prime,conf=conf)

    def main(self):
        conf = Config()
        theta_boot = dict()
        w_boot = dict()
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
