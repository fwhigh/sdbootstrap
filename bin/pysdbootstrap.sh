#!/usr/bin/env bash

n_data=100000
n_boot=200
ss_rate=0
njobs=6
blocksize=$(awk -v n_data=$n_data -v njobs=$njobs 'BEGIN { print 107/10000*n_data/njobs"k" }')

echo "Block size $blocksize"

function mean_stddev() {
    n_samples=$1
    ss_rate=$2
    awk -v n_samples=$n_samples -v ss_rate=$ss_rate '
    {
        s0 += $2
        s1 += $2*$1
        s2 += $2*$1**2
    }
    END {
        if (n_samples == 0) { n_samples = 1 }
        print s1/s0,sqrt((s0 * s2 - s1 * s1)/(s0 * (s0 - 1)))/sqrt(n_samples/ss_rate)
    }' ;
}
export -f mean_stddev

function inneronlinecmd () {
    sdbootstrap_inner.py --online_update WeightedMeanUpdater ;
    #sdbootstrap_inner.py --online_update BatchWeightedMeanUpdater ;
    #sdbootstrap_inner.py --online_update SuperlinearUpdater ;
    # sdbootstrap_inner.py --online_update MedianUpdater --precision 1e2 ;
    #sdbootstrap_inner.py --online_update QuantileUpdater --precision 1e4 --quantile 0.1 ;
}
export -f inneronlinecmd

function innerbatchcmd () {
    sdbootstrap_inner.py --batch_update WeightedMeanUpdater ;
    #sdbootstrap_inner.py --batch_update BatchWeightedMeanUpdater ;
    #sdbootstrap_inner.py --batch_update SuperlinearUpdater ;
    # sdbootstrap_inner.py --batch_update MedianUpdater --precision 1e2 ;
    #sdbootstrap_inner.py --batch_update QuantileUpdater --precision 1e4 --quantile 0.1 ;
}
export -f innerbatchcmd

# make fake data
if [ ! -f data.txt ]; then
    awk -v n_data=$n_data '
    BEGIN {
        for (i=1;i<=n_data;i++) {
            print rand(),1
        }
    }' > data.txt
fi

echo "serial batch"
time parallel --pipepart --jobs 1 --block 10M -a data.txt innerbatchcmd \
 > pyboot_out0.txt
cat data.txt | mean_stddev $n_data 1
cut -d' ' -f 3,4 pyboot_out0.txt | mean_stddev 0 1

echo "serial chained batch"
time parallel --pipepart --jobs 1 --block $blocksize -a data.txt innerbatchcmd | \
 sdbootstrap_outer.py > pyboot_out1.txt
cat data.txt | mean_stddev $n_data 1
cut -d' ' -f 3,4 pyboot_out1.txt | mean_stddev 0 1

echo "parallel batch"
time parallel --pipepart --jobs $njobs --block $blocksize -a data.txt innerbatchcmd | \
 sdbootstrap_outer.py > pyboot_out2.txt
cat data.txt | mean_stddev $n_data 1
cut -d' ' -f 3,4 pyboot_out2.txt | mean_stddev 0 1

echo "serial online"
time parallel --pipepart --jobs 1 --block 10M -a data.txt inneronlinecmd \
 > pyboot_out3.txt
cat data.txt | mean_stddev $n_data 1
cut -d' ' -f 3,4 pyboot_out3.txt | mean_stddev 0 1

echo "serial chained online"
time parallel --pipepart --jobs 1 --block $blocksize -a data.txt inneronlinecmd | \
 sdbootstrap_outer.py > pyboot_out4.txt
cat data.txt | mean_stddev $n_data 1
cut -d' ' -f 3,4 pyboot_out4.txt | mean_stddev 0 1

echo "parallel online"
time parallel --pipepart --jobs $njobs --block $blocksize -a data.txt inneronlinecmd | \
 sdbootstrap_outer.py > pyboot_out5.txt
cat data.txt | mean_stddev $n_data 1
cut -d' ' -f 3,4 pyboot_out5.txt | mean_stddev 0 1





