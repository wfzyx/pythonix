# mkdir - Makes a Directory 

import sys
import os
import argparse

def cd(directory):
  os.mkdir(directory)

def main(argv):
  parser = argparse.ArgumentParser()
  parser.add_argument('directory', nargs=argparse.REMAINDER)
  argv = parser.parse_args()
  cd(argv.directory)
	
if __name__ == '__main__':
  main(sys.argv)