from oblb.bootstrap import Bootstrap
from oblb.config import Config
import oblb.updater
import numpy as np
import pdb

class InnerBootstrap(Bootstrap):

    def __init__(self):
        pass

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
                w = w_prime*np.random.poisson(lam=1.0)
                if w == 0:
                    continue
                (theta_boot[k],w_boot[k])=online_update(theta_boot[k],w_boot[k],X,w,conf=conf)

    def main(self):
        conf = Config()
        online_updater = getattr(oblb.updater,conf.online_update)()
        (theta_boot,w_boot) = self.init_boot(n_boot=conf.n_boot)
        self.update_bootstrap(theta_boot,w_boot,
                              infile=conf.infile,
                              separator=conf.separator,
                              online_update=online_updater.online_update,
                              conf=conf)
        self.print_bootstrap(theta_boot,w_boot,separator=conf.separator)