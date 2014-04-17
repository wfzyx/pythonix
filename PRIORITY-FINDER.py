# TODO issue with recursion, max stack limit
# TODO make function to auto-set priority

import re
import os

rootdir = os.getcwd()
finc = r'.*?(.c|.h)'
dexc = r'.git'
priority = {}

def dep(file,root):
    l = []
    pat = re.compile(r'#include .*?("|>)')
    f = open(os.path.abspath(root)+'\\'+file,'r').read()
    l = pat.findall(f)
    return (file,root,l)

def lad(path):   
    for root,dirs,files in os.walk(path):
        dirs = [d for d in dirs if not re.match(dexc,d)]
        for dir in dirs:
            lad(dir)       
        files = [f for f in files if not re.match(finc,f)]
        for file in files:  
            try:
                priority = priority[file] = dep(file,root)
            except:
                pass
    
def main():
    lad(rootdir)
    
if __name__ == '__main__':
    main()