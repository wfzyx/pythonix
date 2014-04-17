# TODO create priority rules
# TODO set output to a file

import re
import os
from pprint import pprint

rootdir = os.getcwd()
finc = r'.*?(\.c|\.h)'
priority = {}
done = ['.git']

def dep(file,root):
    l = []
    pat = re.compile(r'#include ["<].*?[">]', re.MULTILINE)
    f = open(os.path.abspath(root)+'\\'+file,'r').read()
    l = pat.findall(f)   
    if l:
        return l
    else:
        return x / 0

def lad(path):
    for root,dirs,files in os.walk(path):
        files = [f for f in files if re.match(finc,f)]
        for file in files:  
            try:
                priority[os.path.abspath(root)[32:]+'\\'+file] = dep(file,root)
            except:
                pass
        for dir in dirs:
            if dir not in done:
                done.append(root)
                lad(dir)
                
        
    
def main():
    lad(rootdir)
    
if __name__ == '__main__':
    main()