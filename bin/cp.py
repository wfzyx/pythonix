# cp: simple program to copy files and directories

import sys
import os
import argparse

def copy(files):
    with open(origin, 'rb') as in_file:
        with open(destination, 'wb') as out_file:
            data = in_file.read(1024)
            while data:
                out_file.write(data)
                data = in_file.read(1024)
                


def main(argv):

    # Initialize parser #
    parser = argparse.ArgumentParser()

    # # Add options #
    # parser.add_argument('-i', action='store_true',
    #                     help='Ask for confirmation before removing')
    # parser.add_argument('-f', action='store_true',
    #                     help='Do not ask for confirmation before\
    #                           removing')
    parser.add_argument('-r', action='store_true',
    help='Remove recursively')
    # Same as -r #
    parser.add_argument('-R', action='store_true',
        help='Remove recursively')

    parser.add_argument('files', nargs=argparse.REMAINDER)

    # argv = parser.parse_args()

    # # If -R is passed, then -r is set to True #
    # if argv.R:
    #     argv.r = True

    if len(argv.files) == 0:
        print('Usage: cp [OPTIONS] file1 file2')

        copy(argv.files)

        if __name__ == '__main__':
            main(sys.argv)
