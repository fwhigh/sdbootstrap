#!/usr/bin/env python

import numpy as np
from sklearn.cross_validation import ShuffleSplit
import time
import pdb

pipeline = lambda x: np.mean(x)

def streaming_mean(s0,s1):
    return s1/float(s0)

def streaming_stddev(s0,s1,s2):
    return np.sqrt((s0 * s2 - s1 * s1)/float(s0 * (s0 - 1)))

def streaming_weighted_stddev(s0,s1,s2,w1):
    return np.sqrt((s0 * s2 - s1 * s1)/float(s0 * s0 - w1))

def online_bootstrap(data,boot_val_arr,boot_weight_arr,weight,n_boot):
    for j in range(n_boot):
        weight[j] = np.random.poisson(1) # valid for large n_data
        if weight[j] == 0:
            continue
        # this is the inner Monte Carlo pipeline of the bootstrap (e.g., mean)
        # combined with the previous iteration, with the appropriate weights.
        # eg, weights in linear modeling.
        boot_val = np.average(np.array([data,boot_val_arr[j]]),
                              weights=np.array([weight[j],boot_weight_arr[j]]))
        # update for the next iteration
        boot_val_arr[j] = boot_val 
        boot_weight_arr[j] = boot_weight_arr[j] + weight[j] # statistical weight to carry through

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

n_data=int(100)
n_boot=int(1e3)
n_split=int(4)

data = np.zeros(n_data)
boot_mean = np.zeros(n_boot)
online_mean = 0.
online_se = 0.
online_boot_mean = 0.
online_boot_stddev = 0.

# fake data
for i in range(n_data):
    data[i] = np.random.randn()
 
print "Data mean ", np.mean(data)
print "Data SE ", np.std(data)/np.sqrt(len(data))



# bootstrap the mean
print
time1 = time.time()
for j in range(n_boot):
    booti = np.random.random_integers(0, n_data-1,n_data)
    boot_mean[j] = pipeline(data[booti])

print "Bootstrap mean ", np.mean(boot_mean)
print "Bootstrap SD ", np.std(boot_mean)
time2 = time.time()
print 'took %0.3f ms' % ((time2-time1)*1000.0)



# online mean and standard error
print
time1 = time.time()
s0 = 0.
s1 = 0.
s2 = 0.
for i in range(n_data):
    s0 = s0 + 1
    s1 = s1 + data[i]
    s2 = s2 + data[i]**2

online_mean = streaming_mean(s0,s1)
online_stddev = streaming_stddev(s0,s1,s2)
online_se = online_stddev/np.sqrt(float(s0))

print "Online mean ", online_mean
print "Online SE ", online_se
time2 = time.time()
print 'took %0.3f ms' % ((time2-time1)*1000.0)



# online bootstrap mean
print
time1 = time.time()
boot_val_arr = np.zeros(n_boot)
boot_weight_arr = np.zeros(n_boot)
weight = np.zeros(n_boot)
# one
# for j in range(n_boot):
#     weight[j] = np.random.poisson(1) # valid for large n_data
#     #weight[j] = np.random.binomial(n_data,1/float(n_data))
for i in range(n_data):
    online_bootstrap(data[i],boot_val_arr,boot_weight_arr,weight,n_boot)

online_boot_mean = np.mean(boot_val_arr)
online_boot_stddev = np.std(boot_val_arr)

print "Online boot mean ", online_boot_mean
print "Online boot SD ", online_boot_stddev
time2 = time.time()
print 'took %0.3f ms' % ((time2-time1)*1000.0)




# online bag of little bootstraps
print
time1 = time.time()
all_boot_val_arr = np.zeros(n_boot)
all_boot_weight_arr = np.zeros(n_boot)
rs = chunks(range(n_data),n_data/n_split)
for k_arr in rs:
    boot_val_arr = np.zeros(n_boot)
    boot_weight_arr = np.zeros(n_boot)
    weight = np.zeros(n_boot)
    for i in k_arr:
        online_bootstrap(data[i],boot_val_arr,boot_weight_arr,weight,n_boot)
    for j in range(n_boot):
        boot_val = np.average(np.array([all_boot_val_arr[j],boot_val_arr[j]]),
                              weights=np.array([all_boot_weight_arr[j],boot_weight_arr[j]]))
        # update for the next iteration
        all_boot_val_arr[j] = boot_val 
        all_boot_weight_arr[j] = all_boot_weight_arr[j] + boot_weight_arr[j] # statistical weight to carry through

online_boot_mean = np.mean(all_boot_val_arr)
online_boot_stddev = np.std(all_boot_val_arr)

print "Online BLB mean ", online_boot_mean
print "Online BLB SD ", online_boot_stddev
time2 = time.time()
print 'took %0.3f ms' % ((time2-time1)*1000.0)


#pdb.set_trace()
