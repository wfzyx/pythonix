# top: gives general info about process

import sys
import os

def _top():
    print("process!!!!!!!!!")

def loopTop():
    op = ''
    while(input() != 'q'):
        _top()

def main(argv):
    loopTop()

if __name__ == '__main__':
    main(sys.argv)
