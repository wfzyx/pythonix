# TODO check include/define dependencies

import sys
import argparse

def main(argv):
    
    stdout_lock = {}
    
    # TODO process config
    # setprogramname(argv[0])
    # setlocale(LC_ALL, '')
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-b',action='store_true',help='number nonblank output lines')
    parser.add_argument('-e',action='store_true',help='-e implies -v')
    parser.add_argument('-f',action='store_true',help='?..')
    parser.add_argument('-l',action='store_true',help='?..')
    parser.add_argument('-n',action='store_true',help='number all output lines')
    parser.add_argument('-s',action='store_true',help='never more than one single blank line')
    parser.add_argument('-t',action='store_true',help='-t implies -v')
    parser.add_argument('-v',action='store_true',help='use ^ and M- notation, except for LFD and TAB')
    flags = parser.parse_args()
    
    if len(argv) < 2:
        print('usage: cat [-beflnstv] [-] [file ...]')
        exit(0)
    
    if flags.b:
        flags.n = True
    
    if flags.e:
        flags.v = True
        
    if flags.t:
        flags.v = True
    
    
    
if __name__ == '__main__':
    main(sys.argv)