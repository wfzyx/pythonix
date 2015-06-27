# chmod: change permissions of given path

import sys
import os
import argparse

def changep(path, mod, recursive=False):
    if mod.isdigit():
        mod = int(mod,8)
    else:
        # use g+x syntax
        pass
        
    if recursive:
        # go trough tree to apply the mask
        pass
    else:
        os.chmod(path, mod)


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
        print('Usage: chmod [-r] mode path')
        exit(0)

    changep(argv.args[1], argv.args[0], recursive=argv.r)

if __name__ == '__main__':
    main(sys.argv)
