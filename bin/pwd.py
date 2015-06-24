# PWD - Print Working Directory - prints global path to current 

import sys
import os

def main(argv):
  print(os.getcwd())

if __name__ == '__main__':
  main(sys.argv)
