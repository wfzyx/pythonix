#!/usr/pkg/bin/python2.7
# rm: simple program to delete files and directories
# TODO: Remove use of 'os' module

import sys
import os
import argparse

def _removedir(d):
    if os.path.isdir(d) and len(os.listdir(d)) == 0:
        os.rmdir(d)
    else:
        print("rmdir: {} isn't a directory or isn't empty".format(d))    

def removedir(dirs, pathlike=False):
    for i in dirs:
        if pathlike:        
            pass
        else:
            _removedir(i)
        
def main(argv):

    # Initialize parser #
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', action='store_true',
        help='Remove all non-empty dirs')

    parser.add_argument('dirs', nargs=argparse.REMAINDER)

    argv = parser.parse_args()

    if len(argv.dirs) == 0:
        print('Usage: rmdir [-p] directories')

    removedir(argv.dirs, argv.p)

if __name__ == '__main__':
    main(sys.argv)