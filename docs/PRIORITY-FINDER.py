# IMPORTANT place this program into minix root to search into code base

import re
import os

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
    dpen = {}
    for key in priority:
        for doc in priority[key]:
            if doc in dpen:
                dpen[doc] += 1
            else:   
                dpen[doc] = 1
                
    priority = []
    for key in dpen.keys():
        priority.append((key,dpen[key]))
        
    priority = sorted(priority, key=lambda tuple: tuple[1],reverse=True)
    with open('PRIORITY_LIST','w') as f:
        for item in priority:
            line = ' '.join([str(x) for x in item])
            f.write(line+'\n')
