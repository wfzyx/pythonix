# rm: simple program to delete files and directories
# TODO: Remove use of 'os' module

import sys
import os
import argparse

def remove(dirs):
  for i in dirs:
    if os.path.isdir(i) and len(os.listdir(i)) == 0:
      os.rmdir(i)
    else:
      print("rmdir: {} isn't a directory or isn't empty".format(i))

def main(argv):

    # Initialize parser #
    parser = argparse.ArgumentParser()

    # Add options #
    #parser.add_argument('-i', action='store_true',
    #                    help='Ask for confirmation before removing')
    #parser.add_argument('-f', action='store_true',
    #                    help='Do not ask for confirmation before\
    #                          removing')
    #parser.add_argument('-r', action='store_true',
    #                    help='Remove recursively')
    # Same as -r #
    #parser.add_argument('-R', action='store_true',
    #                    help='Remove recursively')

    parser.add_argument('dirs', nargs=argparse.REMAINDER)

    argv = parser.parse_args()

    # If -R is passed, then -r is set to True #
    #if argv.R:
    #    argv.r = True


    if len(argv.dirs) == 0:
        print('Usage: rm [OPTIONS] DIR DIRECTORIES')

    remove(argv.dirs)

if __name__ == '__main__':
    main(sys.argv)
