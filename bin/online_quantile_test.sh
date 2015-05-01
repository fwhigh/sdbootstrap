#!/usr/bin/env bash

#http://arxiv.org/pdf/1407.1121v1.pdf

n_data=1000000
precision=1e4
quantile=0.3

# make fake data
if [ ! -f quantile_data.txt ]; then
    awk -v n_data=$n_data '
    BEGIN {
        for (i=1;i<=n_data;i++) {
            print rand(),1
        }
    }' > quantile_data.txt
fi

# frugal median
gawk -v precision=$precision '
{
    $1=$1*precision
    if ($1 > m) {
        m++
    } else if ($1 < m) {
        m--
    }
}
END {
    print m/precision
}' quantile_data.txt

# frugal quantile
# NOTE: THERE'S A TYPO IN THE FRUGAL QUANTILE ARXIV PAPER
gawk -v precision=$precision -v quantile=$quantile -v seed=$RANDOM '
BEGiN {
    srand(seed)
}
{
    r=rand()
    $1=$1*precision
    if ($1 > m && r > 1-quantile) {
        m++
    } else if ($1 < m && r < 1-quantile) {
        m--
    }
}
END {
    print m/precision
}' quantile_data.txt
