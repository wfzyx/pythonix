#!/usr/pkg/bin/python2.7
# kill: send given signal to a specific pdi

import sys
import os
import argparse
import signal

def killpid(pid, signame=False, signal='TERM', exitstatus=False):
    if signame:
        try:
          s = eval('signal.SIG'+signal.upper())
        except AttributeError:
          print('Invalid signal')
          return
    else:
        s = 15
    if exitstatus:
        pass
        pass
    os.kill(pid, s)

def main(argv):

    parser = argparse.ArgumentParser()

    parser.add_argument('-s', action='store_true',
        help='Signal name')
    parser.add_argument('-l', action='store_true',
        help='Exit status')
    parser.add_argument('args', nargs=argparse.REMAINDER)

    argv = parser.parse_args()

    argv.signal = 'TERM'
    if argv.s:
        argv.signal = argv.args[0]
        argv.args = args.args[1:]

    if len(argv.args) == 0:
        print('Usage: kill [-sl] pid')
        exit(0)

    killpid(int(argv.args[0]), signame=argv.s, signal=argv.signal, exitstatus=argv.l)

if __name__ == '__main__':
    main(sys.argv)
