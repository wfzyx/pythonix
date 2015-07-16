#!/usr/pkg/bin/python2.7
# rm: simple program to delete files and directories
# TODO: Remove use of 'os' module

import sys
import os
import argparse

def remove(files, force=False, interactive=False, recursive=False):
    if recursive and interactive:
        for i in files:
            if os.path.isdir(i) and not i.endswith('/'):
                i += '/'
            if os.path.isfile(i):
                answer = input('rm: remove common file "{0}"? '.format(i))
                if answer.upper() == 'Y':
                    os.remove(i)
            elif os.path.isdir(i) and len(os.listdir(i)) > 0:
                answer = input('rm: descent into directory "{0}"? '.format(i))
                if answer.upper() == 'Y':
                    subdir = [''.join([i,x]) for x in os.listdir(i)]
                    remove(subdir, force=force,
                           interactive=interactive, recursive=recursive)
                    answer = input('rm: remove directory "{0}"? '.format(i))
                    if answer.upper() == 'Y':
                        os.rmdir(i)
            else:
                answer = input('rm: remove directory "{0}"? '.format(i))
                os.rmdir(i)
    elif recursive:
        for i in files:
            if os.path.isdir(i) and not i.endswith('/'):
                i += '/'
            if os.path.isfile(i):
                os.remove(i)
            elif os.path.isdir(i) and len(os.listdir(i)) > 0:
                subdir = [''.join([i,x]) for x in os.listdir(i)]
                remove(subdir, force=force,
                       interactive=interactive, recursive=recursive)
                os.rmdir(i)
            else:
                os.rmdir(i)
    else:
	for i in files:
          if os.path.isfile(i):
            os.remove(i)
          elif len(os.listdir(i) == 0):
            os.rmdir(i)

def main(argv):

    # Initialize parser #
    parser = argparse.ArgumentParser()

    # Add options #
    parser.add_argument('-i', action='store_true',
        help='Ask for confirmation before removing')
    parser.add_argument('-f', action='store_true',
        help='Do not ask for confirmation before removing')
    parser.add_argument('-r', action='store_true',
        help='Remove recursively')
    parser.add_argument('-R', action='store_true',
        help='Remove recursively')

    parser.add_argument('files', nargs=argparse.REMAINDER)

    argv = parser.parse_args()

    if argv.R:
        argv.r = True


    if len(argv.files) == 0:
        print('Usage: rm [OPTIONS] FILES')
        return

    remove(argv.files, force=argv.f, interactive=argv.i, recursive=argv.r)

if __name__ == '__main__':
    main(sys.argv)
