#!/usr/pkg/bin/python2.7
from __future__ import print_function

import sys

def main(argv):
  if len(argv) != 2:
    print('Usage: ./countLoc.py <file_to_count.[py | c]')
    return
  file = argv[1]
  mode = file.split('.')[1]
  if mode == 'py':
    cKey = '#'
  elif mode == 'c':
    cKey = '//'
    sKey = '/*'
    eKey = '*/'
  else:
    print('Invalid extension, please input a Python or C code file')
    return

  comment = loc = blank = 0
  with open(file, 'r') as f:
    for line in f.readlines():
      line = line.strip()
      if not line:
        blank += 1
      elif line.startswith(cKey):
        comment += 1
      elif mode == 'c' and line.startswith(sKey) and line.endswith(eKey):
        comment += 1
      elif mode == 'c' and line.startswith(sKey):
        cFlag = True
        comment += 1
      elif mode == 'c' and line.endswith(eKey):
        cFlag = False
        comment += 1
      elif mode == 'c' and cFlag:
        comment += 1
      else:
        loc += 1
  print()
  print('File: ', file)
  print('LoC: ', loc)
  print('Comments: ', comment)
  print('Blank: ', blank)
  print()
      
if __name__ == '__main__':
  main(sys.argv)
