from .constants import Constants
import argparse
import sys

class Config(object):

    def __init__(self):
        self.parse_args()

    def parse_args(self):
        parser = argparse.ArgumentParser(description='Online distributed bootstrap.')
        parser.add_argument('--n_boot', 
                            help='N bootstrap interations. Default %s' % (Constants.N_BOOT,),
                            type=int,
                            default=Constants.N_BOOT)
        parser.add_argument('--separator', 
                            help='Separator. Default "%s"' % (Constants.SEPARATOR,),
                            type=str,
                            default=Constants.SEPARATOR)
        parser.add_argument('--online_update', 
                            help='Online update function. Default "%s"' % (Constants.ONLINE_UPDATE,),
                            type=str,
                            default=Constants.ONLINE_UPDATE)
        parser.add_argument('--online_bootstrap_update', 
                            help='Online update function. Default "%s"' % (Constants.ONLINE_UPDATE,),
                            type=str,
                            default=Constants.ONLINE_UPDATE)
        parser.add_argument('--precision', 
                            help='Precision of streaming quantile. Default %s' % (Constants.PRECISION,),
                            type=float,
                            default=Constants.PRECISION)
        parser.add_argument('--quantile', 
                            help='Quantile. Default %s' % (Constants.QUANTILE,),
                            type=float,
                            default=Constants.QUANTILE)
        parser.add_argument('--batch_update',
                           help='Batch update function. Default %s' % (Constants.BATCH_UPDATE,),
                           type=str,
                           default=Constants.BATCH_UPDATE)
        parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                            default=sys.stdin)
        parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                            default=sys.stdout)

        args = parser.parse_args()

        self.n_boot        = args.n_boot
        self.separator     = args.separator
        self.online_update = args.online_update
        self.batch_update  = args.batch_update
        self.precision     = args.precision
        self.quantile      = args.quantile
        self.infile        = args.infile
        self.outfile       = args.outfile
