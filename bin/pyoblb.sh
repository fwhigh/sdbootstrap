#!/usr/bin/env bash

n_data=10000
n_boot=200
ss_rate=1

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

# echo "serial online"
# time cat data.txt | \
#  ./oblb_inner.py --online_update WeightedMeanUpdater --precision 1e2 --quantile 0.1 > pyboot_out.txt
# cat data.txt | mean_stddev $n_data 1
# cut -d' ' -f 2 pyboot_out.txt | mean_stddev 0 1

echo "serial batch"
time cat data.txt | \
 ./oblb_inner.py --batch_update WeightedMeanUpdater --precision 1e2 --quantile 0.1 > pyboot_out1.txt
cat data.txt | mean_stddev $n_data 1
cut -d' ' -f 2 pyboot_out1.txt | mean_stddev 0 1


# echo "serial with outer"
# time cat data.txt | ./oblb_inner.py | \
#  ./oblb_outer.py > pyboot_out2.txt
# cat data.txt | mean_stddev $n_data 1
# cut -d' ' -f 2 pyboot_out2.txt | mean_stddev 0 1

echo "parallel online"
time cat data.txt | \
 parallel --block 10k --pipe ./oblb_inner.py --online_update WeightedMeanUpdater --precision 1e4 --quantile 0.1 | \
 ./oblb_outer.py > pyboot_out3.txt
cat data.txt | mean_stddev $n_data 1
cut -d' ' -f 2 pyboot_out3.txt | mean_stddev 0 1

echo "parallel batch"
time gawk -v ss_rate=$ss_rate -v seed=$RANDOM 'BEGIN {srand(seed)} rand() < ss_rate {print}' data.txt | \
 parallel --block 10k --pipe ./oblb_inner.py --batch_update WeightedMeanUpdater --precision 1e4 --quantile 0.1 | \
 ./oblb_outer.py > pyboot_out4.txt
cat data.txt | mean_stddev $n_data 1
cut -d' ' -f 2 pyboot_out4.txt | mean_stddev 0 1




