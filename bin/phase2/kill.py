# kill: send given signal to a specific pdi

import sys
import os
import argparse

def changep(pid, sig=15, signame=False, exstatus=False):
    if signame:
        pass
    if exstatus:
        pass
    os.kill(pid, sig)

def main(argv):

    parser = argparse.ArgumentParser()

    parser.add_argument('-s', action='store_true',
        help='Signal name')
    parser.add_argument('-l', action='store_true',
        help='Exit status')
    parser.add_argument('args', nargs=argparse.REMAINDER)

    argv = parser.parse_args()

    if argv.R:
        argv.r = True

    if len(argv.args) == 0:
        print('Usage: kill [-sl] pid')
        exit(0)

    changep(argv.args[-1], signame=argv.s, exstatus=argv.l)

if __name__ == '__main__':
    main(sys.argv)
