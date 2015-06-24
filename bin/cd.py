# cd - Change Working Directory 

import sys
import os
import argparse

def cd(path):
  os.chdir(argv)

def main(argv):
  parser = argparse.ArgumentParser()
  parser.add_argument('path', nargs=argparse.REMAINDER)
  argv = parser.parse_args()
  cd(argv.path)
	
if __name__ == '__main__':
  main(sys.argv)