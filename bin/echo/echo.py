# Echo program, print stuffs in stdout

def main(argv):
  # TODO Find and implement setprogname,setlocale, probably in process part
  # check <sys.cdefs.h>
  
  # setprogname(argv[0])
  # setlocale(LC_ALL, '')
  
  if argv[1] == '-n':
    nflag = 1
    end = ''
  else:
    nflag = 0
    end = '\n'
  
  try:
    print(' '.join(argv[nflag+1:]),end=end)
  except IOError:
    exit(1)
    
  exit(0)

if __name__ == '__main__':
    main(sys.argv)
