# rm. Remove files and/or directories
# TODO: Remove use of 'os' module

import sys
import os
import argparse

def remove(force=False, interactive=False, recursive=False, files=None):
    # TODO: implement recursive removal #
    if interactive and not recursive:
        for i in files:
            if os.path.isfile(i):
                stdin_aux = input('rm: remove commom file "{0}"? '.format(i))
                if stdin_aux.upper() == 'Y':
                    os.remove(i)
            elif os.path.isdir(i):
                print('rm: {0} "{1}": It\'s a directory'
                      .format('unable to remove', i))
            else:
                print('rm: {0} "{1}": File or directory not found'
                      .format('unable to remove', i))
    else:
        for i in files:
            if os.path.isfile(i):
                os.remove(i)
            else:
                print('rm: {0} "{1}": It\'s a directory'
                      .format('unable to remove', i))

def main(argv):

    # Initialize parser #
    parser = argparse.ArgumentParser()

    # Add options #
    parser.add_argument('-i', action='store_true',
                        help='Ask for confirmation before removing')
    parser.add_argument('-f', action='store_true',
                        help='Do not ask for confirmation before\
                              removing')
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
