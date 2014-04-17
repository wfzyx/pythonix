# rm. Remove files and/or directories

import sys
import argparse
import traceback

def main(argv):

    # Initialize parser #
    parser = argparse.ArgumentParser()

    # Add options #
    parser.add_argument('-i', action='store_true',
                        help='Ask for confirmation before removing files')
    parser.add_argument('-f', action='store_true',
                        help='Do not ask for confirmation before\
                              removing files')
    parser.add_argument('-r', action='store_true',
                        help='Remove recursively')
    # Same as -r #
    parser.add_argument('-R', action='store_true',
                        help='Remove recursively')

    parser.add_argument('files', nargs=argparse.REMAINDER)

    argv = parser.parse_args()

    # If -R is passed, then -r is set to True #
    if argv.R:
        argv.r = True
    
    if argv.i:
        pass
