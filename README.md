# online-blb
Online Bag of Little Bootstraps

## Features of the OBLB

  1.  Maintains the (possibly multivariate) bootstrap sample distribution.
  1.  The inner bootstrap can be online if an online, importance-weighting update rule is provided.
  1.  The inner bootstrap can be offline if there's no online update rule available, as in regular BLB.
  1.  The data stream can optionally be subsampled, emulating the m-out-of-n bootstrap method.
