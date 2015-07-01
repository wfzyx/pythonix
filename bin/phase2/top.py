# top: gives general info about process

import sys
import os

def _top():
    for proc in os.listdir('/proc'):
        data = open('/proc/{}/psinfo', 'rb').read()
        print(data)

def loopTop():
    op = ''
    while(op != 'q'):
        _top()
	op = raw_input()

def main(argv):
    loopTop()

if __name__ == '__main__':
    main(sys.argv)
