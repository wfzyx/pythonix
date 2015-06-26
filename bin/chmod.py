# chmod: change permissions of given path

import sys
import os
import argparse

def changep(path, mod):
  os.chmod(path, int(mod,8))


def main(argv):

    # Initialize parser #
    parser = argparse.ArgumentParser()

    # # Add options #
    # parser.add_argument('-i', action='store_true',
    #                     help='Ask for confirmation before removing')
    # parser.add_argument('-f', action='store_true',
    #                     help='Do not ask for confirmation before\
    #                           removing')
    #parser.add_argument('-r', action='store_true',
    #help='Remove recursively')
    # Same as -r #
    #parser.add_argument('-R', action='store_true',
    #    help='Remove recursively')

    parser.add_argument('args', nargs=argparse.REMAINDER)

    argv = parser.parse_args()

    # If -R is passed, then -r is set to True #
    #if argv.R:
    #    argv.r = True

    if len(argv.args) == 0:
        print('Usage: chmod [-R] MODE PATH')

    changep(argv.args[1], argv.args[0])

if __name__ == '__main__':
    main(sys.argv)
