#!/usr/pkg/bin/python2.7
# mv: simple program to rename or move files and directories

import sys
import os
import argparse

def _move(o,d):
    os.rename(o, d)

def move(origin, destination, interactive=False, force=False):
    if interactive:
        if os.path.isfile(destination):
            op = input('Replace {0}?[y/n]: ')
            if op.lower() == 'y':
                _move(origin, destination)
    elif force:
        _move(origin, destination)
    else:
        _move(origin, destination)

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store_true',
        help='Ask for confirmation before removing')
    parser.add_argument('-f', action='store_true',
        help='Do not ask for confirmation before removing')

    parser.add_argument('files', nargs=argparse.REMAINDER)

    argv = parser.parse_args()

    if len(argv.files) == 0:
        print('Usage: cp [OPTIONS] file1 file2')
        exit(0)

    move(argv.files[0],argv.files[1],argv.i,argv.f)

if __name__ == '__main__':
    main(sys.argv)