from oblb.config import Config
import numpy as np
import pdb

class InnerBootstrap():
    def __init__(self):
        pass

    def init_boot(self,conf):
        theta_boot = np.zeros(conf.n_boot)
        w_boot = np.zeros(conf.n_boot)
        return theta_boot,w_boot

    def main(self):
        conf = Config()
        (theta_boot,w_boot) = self.init_boot(conf)
        online_update = eval(conf.online_update)
        for line in conf.infile:
            field = line.split(conf.seperator)
            X = float(field[0])
            w_prime = float(field[1])
            for k in range(conf.n_boot):
                w = w_prime*np.random.poisson(lam=1.0)
                if w == 0:
                    continue
                (theta_boot[k], w_boot[k]) = online_update(
                                                  theta_boot[k],
                                                  w_boot[k],
                                                  X,
                                                  w)
        for k in range(conf.n_boot):
            print(conf.seperator.join([str(k),str(theta_boot[k]),str(w_boot[k])]))
