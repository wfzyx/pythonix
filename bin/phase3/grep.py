#!/usr/pkg/bin/python2.7
from __future__ import print_function
# grep: serach for string patterns in files

import sys
import os
import argparse
import re

def _fg(file, pattern, ops):
  with open(file, 'r') as f:
    text = f.readlines()
    z = len(text)
    for i in range(z):
      line = text[i]
      result = pattern.match(line.strip())
      if not result: result = (ops.pattern in line.strip())
      if result:
        if ops.A:
          if i < ops.A_num:
            j = i
          else:
            j = ops.A_num
          print(''.join(text[i-j:i]), end='')
        print(line, end='')
        if ops.B:
          if i+ops.B_num > z:
            j = z-i
          else:
            j = ops.B_num
          print(''.join(text[i+1:i+j+1]), end='')

def _grep(args):
  pattern = re.compile(args.pattern if not args.i else args.pattern.lower())
  for file in args.files:
    _fg(file, pattern, args)


def main(argv):

  # Initialize parser #
  parser = argparse.ArgumentParser()

  # Add options #
  parser.add_argument('-A', dest='A_num', action='store', type=int,
    help='Prints traliing lines for each match')
  parser.add_argument('-B', dest='B_num', action='store', type=int,
    help='Prints leading lines for each match')
  parser.add_argument('-i', action='store_true',
    help='Makes pattern case insensitive')

  parser.add_argument('files', nargs=argparse.REMAINDER)

  argv = parser.parse_args()

  argv.A = False
  argv.B = False
  if argv.A_num:
    argv.A = True
  if argv.B_num:
    argv.B = True

  if len(argv.files) < 2:
    parser.print_help()
    return

  argv.pattern = argv.files[0]
  argv.files = argv.files[1:]

  _grep(args=argv)

if __name__ == '__main__':
  main(sys.argv)
