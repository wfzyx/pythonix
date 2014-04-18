# rm. Remove files and/or directories

import sys
import os
import argparse
import traceback

def remove(force=False, interactive=False, recursive=False, files=None):
    if recursive:
        if interactive:
            for i in files:
                with open(i) as j:
                    answer = input('rm: remove common file "i"?')
                    if answer.upper
    elif 

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
    
    remove(force=argv.f, interactive=argv.i, 
           recursive=argv.r, files=argv.files)

if __name__ == '__main__':
    main(sys.argv)
