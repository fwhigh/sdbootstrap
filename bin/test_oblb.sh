#!/usr/bin/env bash

n_data=10000
n_boot=1000
ss_rate=0.1

function inner_boot() {
    n_boot=$1
    gawk -v n_boot=$n_boot -v seed=$RANDOM '
    function poisson(randu) {
        if (randu < 0.3678794) {
            return 0
        } else if (randu < 0.7357589) {
            return 1
        } else if (randu < 0.9196986) {
            return 2
        } else if (randu < 0.9810118) {
            return 3
        } else if (randu < 0.9963402) {
            return 4
        } else if (randu < 0.9994058) {
            return 5
        } else if (randu < 0.9999168) {
            return 6
        } else if (randu < 0.9999898) {
            return 7
        } else if (randu < 0.9999989) {
            return 8
        } else if (randu < 0.9999999) {
            return 9
        } else  {
            return 10
        }
    }
    function online_update(x1,w1,x2,w2) {
        return (w1*x1 + w2*x2)/(w1 + w2)
    }
    function online_weight_update(w1,w2) {
        return (w1 + w2)
    }
    BEGIN {
        srand(seed)
    }
    {
        for (k=1;k<=n_boot;k++) {
            w = $2*poisson(rand())
            if (w == 0) { continue }
            boot[k] = online_update(boot[k],weight[k],$1,w)
            weight[k] = online_weight_update(weight[k],w)
            #num=(boot[k]*weight[k]+$1*w)
            #denom=(weight[k]+w)
            #boot[k]=num/denom
            #weight[k]=denom
        }
    }
    END {
        for (k in boot) {
            print k,boot[k],weight[k]
        }
    }' ;
}
export -f inner_boot

function outer_boot() {
    n_boot=$1
    gawk -v n_boot=$n_boot '
    function online_update(x1,w1,x2,w2) {
        return (w1*x1 + w2*x2)/(w1 + w2)
    }
    function online_weight_update(w1,w2) {
        return (w1 + w2)
    }
    {
        boot[$1] = online_update(boot[$1],weight[$1],$2,$3)
        weight[$1] = online_weight_update(weight[$1],$3)
    }
    END {
        for (k in boot) {
            print k,boot[k],weight[$1]
        }
    }' ;
}
export -f outer_boot

function mean_stddev() {
    n_samples=$1
    ss_rate=$2
    awk -v n_samples=$n_samples -v ss_rate=$ss_rate '
    {
        s0++
        s1 += $1
        s2 += $1**2
    }
    END {
        if (n_samples == 0) { n_samples = 1 }
        print s1/s0,sqrt((s0 * s2 - s1 * s1)/(s0 * (s0 - 1)))/sqrt(n_samples/ss_rate)
    }' ;
}
export -f mean_stddev



# make fake data
if [ ! -f data.txt ]; then
    awk -v n_data=$n_data '
    BEGIN {
        for (i=1;i<=n_data;i++) {
            print rand(),1
        }
    }' > data.txt
fi

echo "serial standard"
time cat data.txt | inner_boot $n_boot > boot_out.txt
cat data.txt | mean_stddev $n_data 1
cut -d' ' -f 2 boot_out.txt | mean_stddev 0 1

echo "serial subsampled"
time gawk -v ss_rate=$ss_rate -v seed=$RANDOM 'BEGIN {srand(seed)} rand() < ss_rate {print}' data.txt | \
 inner_boot $n_boot > boot_out.txt
cat data.txt | mean_stddev $n_data 1
cut -d' ' -f 2 boot_out.txt | mean_stddev 0 $ss_rate

echo "serial chained"
time gawk -v ss_rate=$ss_rate -v seed=$RANDOM 'BEGIN {srand(seed)} rand() < ss_rate {print}' data.txt | \
 inner_boot $n_boot | \
 outer_boot $n_boot > boot1_out.txt
cat data.txt | mean_stddev $n_data 1
cut -d' ' -f 2 boot1_out.txt | mean_stddev 0 $ss_rate

echo "parallel"
#time parallel --pipepart --block 1M -a data.txt inner_boot $n_boot > /dev/null #| outer_boot $n_boot > boot_out.txt
time gawk -v ss_rate=$ss_rate -v seed=$RANDOM 'BEGIN {srand(seed)} rand() < ss_rate {print}' data.txt | \
 parallel --block 10k --pipe inner_boot $n_boot | \
 outer_boot $n_boot > boot2_out.txt
cat data.txt | mean_stddev $n_data 1
cut -d' ' -f 2 boot2_out.txt | mean_stddev 0 $ss_rate







