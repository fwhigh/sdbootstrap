from sdbootstrap.bootstrap import Bootstrap
from sdbootstrap.config import Config
import sdbootstrap.updater

import numpy as np

class MLOuterBootstrap(Bootstrap):

    def __init__(self):
        pass

    def update_bootstrap(self,
                         theta_boot,
                         w_boot,
                         infile=None,
                         separator=None,
                         model=None,
                         conf=None):
        for line in infile:
            field = line.split(separator)
            k = float(field[0])
            X = float(field[1])
            w = float(field[2])
            if w == 0:
                continue
            model.train(X,y)

    def main(self):
        conf = Config()
        model = getattr(sdbootstrap.updater,conf.online_update)()
        (theta_boot,w_boot) = self.init_boot(n_boot=conf.n_boot)
        self.update_bootstrap(theta_boot,w_boot,
                              infile=conf.infile,
                              separator=conf.separator,
                              model=model,
                              conf=conf)
        self.print_bootstrap(theta_boot,w_boot,separator=conf.separator)
