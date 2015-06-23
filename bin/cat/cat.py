from __future__ import print_function

# TODO check include/define dependencies

import sys
import argparse
import traceback

def main(argv):
    
    stdout_lock = {}
    
    # TODO process config
    # setprogramname(argv[0])
    # setlocale(LC_ALL, '')
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-b',action='store_true',
                        help='number nonblank output lines')
    parser.add_argument('-e',action='store_true',
                        help='-e implies -v')
    parser.add_argument('-f',action='store_true',
                        help='?..')
    parser.add_argument('-l',action='store_true',
                        help='?..')
    parser.add_argument('-n',action='store_true',
                        help='number all output lines')
    parser.add_argument('-s',action='store_true',
                        help='never more than one single blank line')
    parser.add_argument('-t',action='store_true',
                        help='-t implies -v')
    parser.add_argument('-v',action='store_true',
                        help='use ^ and M- notation, except for LFD and TAB')
    parser.add_argument('files', nargs=argparse.REMAINDER)
    
    argv = parser.parse_args()
    
    if argv.b:
        argv.n = True
    
    if argv.e:
        argv.v = True
        
    if argv.t:
        argv.v = True
        
        
    if not argv.files or (len(argv.files) == 1 and '-' in argv.files):
        try:
            # Behaves like CAT without files #
            while True:
                stdin_aux = raw_input()
                print(stdin_aux)
        except KeyboardInterrupt:
            # Hide traceback from end-user # 
            print()
            traceback.format_exc()

    # Prints files passed #
    
    elif len(argv.files) > 0:
        try:
            for i in argv.files:
                with open(i, 'r') as j:
                    if argv.n:
                        xline = 1
                        if argv.b:
                            for line in j.readlines(): 
                                if line.strip():
                                    fline = '{} {}'.format(xline,line)
                                    print(fline,end='')
                                xline += 1
                        else:
                            for line in j.readlines(): 
                                fline = '{} {}'.format(xline,line)
                                print(fline,end='')
                                xline += 1
                    else:
                        for line in j.readlines(): 
                            print(line,end='')
                print('')                          
                        
        except IOError:
            traceback.format_exc()

            
if __name__ == '__main__':
    main(sys.argv)
