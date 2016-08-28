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
        parser.add_argument('--update_every', 
                            help='Master update rule: update every N. Default %s' % (Constants.UPDATE_EVERY,),
                            type=int,
                            default=Constants.UPDATE_EVERY)
        parser.add_argument('--no_flush_on_update', 
                            help='Do not flush inner bootstrap distros on update?',
                            action="store_true")
        parser.add_argument('--job',
                           help='Job number. Default %s' % (Constants.JOB,),
                           type=str,
                           default=Constants.JOB)
        parser.add_argument('--separator', 
                            help='Separator. Default "%s"' % (Constants.SEPARATOR,),
                            type=str,
                            default=Constants.SEPARATOR)
        parser.add_argument('--composite_key_separator', 
                            help='Separator. Default "%s"' % (Constants.COMPOSITE_KEY_SEPARATOR,),
                            type=str,
                            default=Constants.COMPOSITE_KEY_SEPARATOR)
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
        parser.add_argument('--model',
                           help='ML model. Default %s' % (Constants.MODEL,),
                           type=str,
                           default=Constants.MODEL)
        parser.add_argument('--test_file',
                           help='Test file. Default %s' % (Constants.TEST_FILE,),
                           type=argparse.FileType('r'),
                           default=Constants.TEST_FILE)
        parser.add_argument('--ema_alpha', 
                            help='Exponential moving average alpha. Default %s' % (Constants.EMA_ALPHA,),
                            type=float,
                            default=Constants.EMA_ALPHA)
        parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                            default=sys.stdin)
        parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                            default=sys.stdout)

        args = parser.parse_args()

        self.n_boot        = args.n_boot
        self.update_every  = args.update_every
        self.no_flush_on_update = args.no_flush_on_update
        self.job           = args.job
        self.separator     = args.separator
        self.composite_key_separator     = args.composite_key_separator
        self.online_update = args.online_update
        self.batch_update  = args.batch_update
        self.precision     = args.precision
        self.quantile      = args.quantile
        self.model         = args.model
        self.test_file     = args.test_file
        self.ema_alpha     = args.ema_alpha
        self.infile        = args.infile
        self.outfile       = args.outfile
