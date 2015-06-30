# top: gives general info about process

import sys
import os

def _getch():
    import termios, tty
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def _top():
    print("process!!!!!!!!!")
    
def loopTop():
    op = ''
    while(_getch() != 'q'):
        _top()

def main(argv):
    loopTop()

if __name__ == '__main__':
    main(sys.argv)
