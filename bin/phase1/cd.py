#!/usr/pkg/bin/python2.7
# cd - Change Working Directory 

import sys
import os
import argparse

def cd(path):
  os.chdir(path)

def main(argv):
  parser = argparse.ArgumentParser()
  parser.add_argument('path', nargs=argparse.REMAINDER)
  argv = parser.parse_args()
  cd(argv.path[0])
	
if __name__ == '__main__':
  main(sys.argv)
