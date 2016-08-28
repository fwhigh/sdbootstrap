import numpy as np
import time

class Bootstrap(object):
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

    def multinomial(self,n):
        w_prime = np.zeros(n)
        booti = np.random.randint(0,n,n)
        for i in booti:
            w_prime[i] += 1
        return w_prime

    def print_bootstrap(self,
                        theta,
                        w,
                        id=None,
                        separator=None,
                        update_id=None):
        if update_id is None:
            update_id = time.time()
        for k in theta:
            print(separator.join([str(update_id),str(k),str(theta[k]),str(w[k])]))
