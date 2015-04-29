#!/usr/bin/env bash

n_data=1000
n_boot=10000

function inner_boot() {
    n_boot=$1
    awk -v n_boot=$n_boot -v seed=$RANDOM '
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
            w = poisson(rand())
            if (w == 0) { continue }
            boot[k] = online_update(boot[k],weight[k],$1,w)
            weight[k] = online_weight_update(weight[k],w)
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
    awk -v n_boot=$n_boot '
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
            print k,boot[k]
        }
    }' ;
}
export -f outer_boot

function mean_stddev() {
    n_samples=$1
    awk -v n_samples=$n_samples '
    {
        s0++
        s1 += $1
        s2 += $1**2
    }
    END {
        if (n_samples == 0) { n_samples = 1 }
        print s1/s0,sqrt((s0 * s2 - s1 * s1)/(s0 * (s0 - 1)))/sqrt(n_samples)
    }' ;
}
export -f mean_stddev



# make fake data
if [ ! -f data.txt ]; then
    awk -v n_data=$n_data '
    BEGIN {
        for (i=1;i<=n_data;i++) {
            print rand()
        }
    }' > data.txt
fi

echo "serial standard"

time cat data.txt | inner_boot $n_boot > boot_out.txt
cat data.txt | mean_stddev $n_data
cut -d' ' -f 2 boot_out.txt | mean_stddev 0

echo "serial chained"

time cat data.txt | inner_boot $n_boot | outer_boot $n_boot > boot_out.txt
cat data.txt | mean_stddev $n_data
cut -d' ' -f 2 boot_out.txt | mean_stddev 0


echo "parallel"
#time parallel --pipepart --block 1M -a data.txt inner_boot $n_boot > /dev/null #| outer_boot $n_boot > boot_out.txt
time cat data.txt | parallel --pipe inner_boot $n_boot | outer_boot $n_boot > boot_out.txt
cat data.txt | mean_stddev $n_data
cut -d' ' -f 2 boot_out.txt | mean_stddev 0
# stddev data.txt $n_data

# mean boot_out.txt
# stddev boot_out.txt





