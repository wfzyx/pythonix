#!/usr/pkg/bin/python2.7
from __future__ import print_function

import sys
import argparse
import traceback

def _cat(files, numberall=False, numbernb=False, escapenot=False, singleblank=False):
  try:
    for i in files:
      with open(i, 'r') as j:
        if numberall:
          xline = 1
          for line in j.readlines():
            fline = '{0: >6}  {1}'.format(xline,line)
            print(fline,end='')
            xline += 1
        elif numbernb:
          xline = 1
          for line in j.readlines():
            if line.strip():
                fline = '{0: >6}  {1}'.format(xline,line)
                print(fline,end='')
                xline += 1
            else:
                print()
        else:
          for line in j.readlines(): 
            print(line)
      print()
  except IOError:
    traceback.format_exc()

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
  
  if argv.b and argv.n:
    argv.b = True
    argv.n = False
  
  if argv.e or argv.t:
    argv.v = True
    
  # if not argv.files or (len(argv.files) == 1 and '-' in argv.files):
  if len(argv.files) == 0:
    try:
      # Behaves like CAT without files #
      while True:
        stdin_aux = raw_input()
        print(stdin_aux)
    except KeyboardInterrupt:
      # Hide traceback from end-user # 
      print()
      traceback.format_exc()

  _cat(files=argv.files,numberall=argv.n, numbernb=argv.b, escapenot=argv.v, singleblank=argv.s)
      
if __name__ == '__main__':
  main(sys.argv)
