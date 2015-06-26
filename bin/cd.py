# cd - Change Working Directory 

import sys
import os
import argparse

def cd(path):
  print('going to:', path)
  os.chdir(path)
  print('debug:', os.getcwd())

def main(argv):
  parser = argparse.ArgumentParser()
  parser.add_argument('path', nargs=argparse.REMAINDER)
  argv = parser.parse_args()
  cd(argv.path[0])
	
if __name__ == '__main__':
  main(sys.argv)
