#!/usr/pkg/bin/python2.7
from __future__ import print_function
# find: find files and directories

import sys
import os
import argparse

def _find(s=None, root=None):
  if not os.path.isdir(root):
    print('First arg must be a directory')
    return
  l = os.listdir(root)
  for x in l:
    newroot = root+x+'/'
    if os.path.isdir(newroot):
      _find(s=s, root=newroot)
    fulls = os.path.abspath(newroot)
    if fulls.endswith(s):
      print(fulls)


def main(argv):

  # Initialize parser #
  parser = argparse.ArgumentParser()

  # Add options #

  parser.add_argument('files', nargs=argparse.REMAINDER)

  argv = parser.parse_args()

  if len(argv.files) < 2:
    print('Usage: find root expression')
    return

  _find(s=argv.files[-1], root=argv.files[0])

if __name__ == '__main__':
  main(sys.argv)
