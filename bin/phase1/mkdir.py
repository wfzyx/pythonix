#!/usr/pkg/bin/python2.7
# mkdir - Makes a Directory 

import sys
import os
import argparse

def _cd(directory, path=False, mod='777'):
  mod = int(mod,8)
  if path:
    os.makedirs(directory, mod)
  else:
    os.mkdir(directory, mod)

def main(argv):
  parser = argparse.ArgumentParser()
  parser.add_argument('-p', action='store_true',
        help='Creates full path')
  parser.add_argument('-m', action='store_true',
        help='Give a specific mode')
  parser.add_argument('directory', nargs=argparse.REMAINDER)
  argv = parser.parse_args()

  argv.mod = '777'
  if argv.m:
    argv.mod = argv.directory[0]
    argv.directory = argv.directory[1:]

  _cd(argv.directory[0], path=argv.p, mod=argv.mod)
	
if __name__ == '__main__':
  main(sys.argv)
