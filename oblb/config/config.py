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
        parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                            default=sys.stdin)
        parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                            default=sys.stdout)

        # parser.add_argument('--m0_weeks', 
        #                     help='M0 weeks. Default %s' % (TeradataConstants.DEFAULT_M0_WEEKS,),
        #                     type=int,
        #                     default=TeradataConstants.DEFAULT_M0_WEEKS)
        # parser.add_argument('--drop_first', 
        #                     help='Drop the output table first. Default False',
        #                     action='store_true')
        # parser.add_argument('--verbosity', 
        #                     help='Verbosity level. Default %d' % (self.DEFAULT_VERBOSITY,),
        #                     type=int,
        #                     default=self.DEFAULT_VERBOSITY)
        # parser.add_argument('--dry_run', 
        #                     help='Dry run. Do not execute the SQL. Default False',
        #                     action='store_true')

        args = parser.parse_args()

        self.n_boot        = args.n_boot
        self.separator     = args.separator
        self.online_update = eval(args.online_update)
        self.infile        = args.infile
        self.outfile       = args.outfile
