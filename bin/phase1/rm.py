#!/usr/pkg/bin/python2.7
# rm: simple program to delete files and directories
# TODO: Remove use of 'os' module

import sys
import os
import argparse
import random

def _remF(file, verbose=False, scramble=False):
  if verbose:
    print(os.path.abspath(file))
  if scramble:
    with open(file, 'rb+') as f:
      s = sys.getsizeof(f.read())
      f.seek(0)
      f.write(b'0xff')
      f.write(b'0x00')
      i = 2
      while sys.getsizeof(f.read()) <= s and i < s:
        f.seek(i)
        f.write(str.encode(str(hex(random.randint(0,255))))
        i += 1
  os.remove(file)

def _remD(dir, verbose=False):
  if verbose:
    print(os.path.abspath(file))
  os.rmdir(dir)

def _remove(files, dirs=False, force=False, interactive=False, recursive=False, verbose=False, scramble=False):
  if recursive and interactive:
    for i in files:
      if os.path.isdir(i) and not i.endswith('/'):
        i += '/'
      if os.path.isfile(i):
        answer = input('rm: remove common file "{0}"? '.format(i))
        if answer.upper() == 'Y':
          _remF(i, verbose=verbose, scramble=scramble)
      elif os.path.isdir(i) and len(os.listdir(i)) > 0:
        answer = input('rm: descent into directory "{0}"? '.format(i))
        if answer.upper() == 'Y':
          subdir = [''.join([i,x]) for x in os.listdir(i)]
          _remove(subdir, dirs=dirs, force=force, interactive=interactive, recursive=recursive)
          if dirs:
            answer = input('rm: remove directory "{0}"? '.format(i))
            if answer.upper() == 'Y':
              _remD(i, verbose=verbose)
      else:
        if dirs:
          answer = input('rm: remove directory "{0}"? '.format(i))
          _remD(i, verbose=verbose)
  elif recursive:
    for i in files:
      if os.path.isdir(i) and not i.endswith('/'):
        i += '/'
      if os.path.isfile(i):
        _remF(i, verbose=verbose, scramble=scramble)
      elif os.path.isdir(i) and len(os.listdir(i)) > 0:
        subdir = [''.join([i,x]) for x in os.listdir(i)]
        _remove(subdir, dirs=dirs, force=force, interactive=interactive, recursive=recursive)
        if dirs:
          _remD(i, verbose=verbose)
      else:
        if dirs:
          _remD(i, verbose=verbose)
  elif force:
    for i in files:
      if os.path.isfile(i):
        _remF(i, verbose=verbose, scramble=scramble)
      elif dirs:
        _remove(subdir, dirs=dirs, force=force, interactive=interactive, recursive=recursive)
        _remD(i, verbose=verbose)
  else:
    for i in files:
      if os.path.isfile(i):
        _remF(i, verbose=verbose, scramble=scramble)
      elif dirs and len(os.listdir(i) == 0):
        _remD(i, verbose=verbose)

def main(argv):

  # Initialize parser #
  parser = argparse.ArgumentParser()

  # Add options #
  parser.add_argument('-d', action='store_true',
    help='Removes directories as well')
  parser.add_argument('-i', action='store_true',
    help='Ask for confirmation before removing')
  parser.add_argument('-f', action='store_true',
    help='Do not ask for confirmation before removing')
  parser.add_argument('-P', action='store_true',
    help='Scrambles bytes of deleted files')
  parser.add_argument('-r', action='store_true',
    help='Remove recursively')
  parser.add_argument('-R', action='store_true',
    help='Remove recursively')
  parser.add_argument('-v', action='store_true',
    help='Vebose')

  parser.add_argument('files', nargs=argparse.REMAINDER)

  argv = parser.parse_args()
  if argv.i and argv.f:
    argv.f = False
  if argv.R:
    argv.r = True

  if len(argv.files) == 0:
    print('Usage: rm [OPTIONS] FILES')
    return

  _remove(argv.files, force=argv.f, interactive=argv.i, recursive=argv.r, verbose=argv.v, dirs=argv.d, scramble=argv.P)

if __name__ == '__main__':
  main(sys.argv)