from oblb.bootstrap import Bootstrap
from oblb.config import Config
import oblb.updater

import numpy as np

class OuterBootstrap(Bootstrap):

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
            update_id = str(field[0])
            k   = str(field[1])
            X   = float(field[2])
            w   = float(field[3])
            if k not in theta_boot:
                theta_boot[k] = 0.0
                w_boot[k] = 0.0
            if w == 0:
                continue
            (theta_boot[k],w_boot[k])=online_update(theta_boot[k],w_boot[k],X,w,conf=conf)

    def main(self):
        conf = Config()
        online_updater = getattr(oblb.updater,conf.online_update)()
        theta_boot = dict()
        w_boot = dict()
        self.update_bootstrap(theta_boot,w_boot,
                              infile=conf.infile,
                              separator=conf.separator,
                              online_update=online_updater.online_update,
                              conf=conf)
        self.print_bootstrap(theta_boot,w_boot,separator=conf.separator)
