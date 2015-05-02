#!/usr/bin/env bash

#http://arxiv.org/pdf/1407.1121v1.pdf

n_data=1000000
precision=1e3

function frugal_q () {
    precision=$1
    quantile=$2
    gawk -v precision=$precision -v quantile=$quantile -v seed=$RANDOM '
    BEGIN {
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
        print quantile,m/precision
    }' quantile_data.txt ;
}
export -f frugal_q

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
    print 0.5,m/precision
}' quantile_data.txt

# frugal quantile
parallel -N1 frugal_q $precision ::: 0.01 0.05 0.1 0.5 0.9 0.95 0.99








