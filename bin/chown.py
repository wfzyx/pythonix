# chown: change user and group owner of given path

import sys
import os
import argparse

def changeo(path, mod, recursive=False):
    if ':' in mod:
        u,g = mod.split(':')
    else:
        u,g = mod,'-1'

    if recursive:
        pass
    else:
        os.chown(path,int(u),int(g))


def main(argv):

    parser = argparse.ArgumentParser()

    parser.add_argument('-r', action='store_true',
        help='Remove recursively')
    parser.add_argument('-R', action='store_true', 
        help='Remove recursively')

    parser.add_argument('args', nargs=argparse.REMAINDER)

    argv = parser.parse_args()

    if argv.R:
       argv.r = True

    if len(argv.args) == 0:
        print('Usage: chmod [-R] owner[:group] PATH')
        exit(0)

    changeo(argv.args[1], argv.args[0], recursive=argv.r)

if __name__ == '__main__':
    main(sys.argv)
