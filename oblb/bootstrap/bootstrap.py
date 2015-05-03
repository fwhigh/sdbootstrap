import numpy as np

class Bootstrap(object):
    def __init__(self):
        pass

    def init_boot(self,n_boot=None):
        theta_boot = np.zeros(n_boot)
        w_boot = np.zeros(n_boot)
        return theta_boot,w_boot

    def print_bootstrap(self,
                        theta,
                        w,
                        separator=None):
        for k in range(len(theta)):
            print(separator.join([str(k),str(theta[k]),str(w[k])]))
