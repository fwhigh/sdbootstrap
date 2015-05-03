#!/usr/bin/env bash

n_data=10000
n_boot=1000
ss_rate=0.1

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
time cat data.txt | ./oblb_inner.py > pyboot_out.txt
cat data.txt | mean_stddev $n_data 1
cut -d' ' -f 2 pyboot_out.txt | mean_stddev 0 1
