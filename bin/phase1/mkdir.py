#!/usr/pkg/bin/python2.7
# mkdir - Makes a Directory 

import sys
import os
import argparse

def cd(directory):
  os.mkdir(directory)

def main(argv):
  # [-p] [-m mode]
  parser = argparse.ArgumentParser()
  parser.add_argument('directory', nargs=argparse.REMAINDER)
  argv = parser.parse_args()
  cd(argv.directory[0])
	
if __name__ == '__main__':
  main(sys.argv)