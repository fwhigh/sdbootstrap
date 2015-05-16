#!/usr/bin/env bash

function innerbatchcmd () {
    #oblb_ml_inner.py --test_file cadata_test --model LinearRegression --n_boot 100 ;
    oblb_ml_inner.py --test_file cadata_test --model GradientBoostingRegressor --n_boot 100 ;
    #oblb_ml_inner.py --model DummyRegressor ;
}
export -f innerbatchcmd

echo "serial"
time parallel --pipepart --jobs 1 --block 10M -a cadata_train \
 innerbatchcmd \
 | oblb_outer.py \
 > pyboot_out0.txt

echo "parallel"
time parallel --pipepart --jobs 6 --block 160k -a cadata_train \
 innerbatchcmd \
 | oblb_outer.py \
 > pyboot_out1.txt

paste -d' ' \
 <(cut -d' ' -f1 cadata_test) \
 <(sort -t' ' -n -k1,1 pyboot_out0.txt | cut -d' ' -f2) \
 <(sort -t' ' -n -k1,1 pyboot_out1.txt | cut -d' ' -f2) \
 > evaluate.txt

R CMD BATCH --no-save --no-restore plotit.R plotit.log
