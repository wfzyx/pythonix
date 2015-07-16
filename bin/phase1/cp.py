#!/usr/pkg/bin/python2.7
# cp: simple program to copy files and directories

import sys
import os
import argparse

def _copy(origin, destination):
    try:
        with open(origin, 'rb') as in_file:
            with open(destination, 'wb') as out_file:
                data = in_file.read(1024)
                while data:
                    out_file.write(data)
                    data = in_file.read(1024)
    except:
        print('cp ERROR')
        exit(1)

def copy(origin, destination, recursive=False, interactive=False, force=False):
    if recursive:
        if interactive:
            pass
    if interactive:
        if os.path.isfile(destination):
            answer = input('cp: overwrite file "{0}" [Y/N]? '.format(destination))
            if answer.upper() == 'Y':
                _copy(origin, destination)

def main(argv):

    # Initialize parser #
    parser = argparse.ArgumentParser()

    # Add options -pfsmvx #
    parser.add_argument('-i', action='store_true',
        help='Ask for confirmation before copying')
    parser.add_argument('-f', action='store_true',
        help='Do not ask for confirmation before removing')
    
    parser.add_argument('-r', action='store_true',
    help='Remove recursively')    
    parser.add_argument('-R', action='store_true',
        help='Remove recursively')

    parser.add_argument('files', nargs=argparse.REMAINDER)

    argv = parser.parse_args()

    # If -R is passed, then -r is set to True #
    if argv.R:
        argv.r = True

    if len(argv.files) == 0:
        print('Usage: cp [OPTIONS] file1 file2')
        exit(0)

    copy(argv.files[0],argv.files[1])

if __name__ == '__main__':
    main(sys.argv)
