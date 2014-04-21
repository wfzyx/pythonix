# rm. Remove files and/or directories
<<<<<<< HEAD
# TODO: remove use of 'os' module
=======
# TODO: Remove use of 'os' module
>>>>>>> 2ccd8ab8390da5a0593722c71c5e1c2697d92f88

import sys
import os
import argparse

<<<<<<< HEAD
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
=======
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
>>>>>>> 2ccd8ab8390da5a0593722c71c5e1c2697d92f88

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


    if len(argv.files) == 0:
        print('Usage: rm [OPTIONS] FILES')

    remove(argv.files, force=argv.f, interactive=argv.i, recursive=argv.r)

if __name__ == '__main__':
    main(sys.argv)
