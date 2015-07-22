#!/usr/pkg/bin/python2.7
from __future__ import print_function

import sys
import py_compile

def main(argv):

  if len(argv) != 2:
    print('Usage: ./gpyc.py <file_to_compile.py>')
    return

  file = argv[1]
  py_compile.compile(file)  
      
if __name__ == '__main__':
  main(sys.argv)