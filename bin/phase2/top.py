from __future__ import print_function
# top: gives general info about process

import sys
import os

def _top():
    rows, columns = os.popen('stty size', 'r').read().split()
    headers = ['psi_v','type','endpoint','name','state','blocked','priority',
        'utime','stime','execycleshi','execycleslo', 'tmemory', 'cmemory', 
        'smemory', 'sleep', 'parentpid', 'realuid', 'effectiveuid', 'procgrp',
        'nicevalue', 'vfsblock', 'blockproc', 'ctrltty', 'kipchi', 'kipclo', 
        'kcallhi', 'kcalllo']

    txtheader = ['pid','realuid','nicevalue','tmemory','priority','state',
        'utime','utime','name']

    procs = [id for id in os.listdir('/proc') if id.isdigit()]
    topdata = []    
    running = 0
    print('something about load averages')

    for proc in procs:
        with open('/proc/{}/psinfo'.format(proc), 'rb') as f:
	    procdata = dict(zip(headers,f.read().split(' ')))
	procdata['pid'] = proc
        topdata.append(procdata)
        if procdata['state'] == 'R':
          running += 1

    print('{0} processes: {1} running, {2} sleeping'.format(len(procs),running , len(procs)-running))
    print('somethinbg about memory')
    print('cpu line 1')
    print('cpu line 2')
    print()        
    print('PID|UID|PRI|NICE|SIZE|STATE|TIME|CPU|COMMAND')

    for proc,i in zip(topdata,range(6,rows)):
        for txt in txtheader:
            print('{:}'.format(proc[txt]), end='|')
        print()

def loopTop():
    op = ''
    while(op != 'q'):
        _top()
	op = raw_input()

def main(argv):
    loopTop()

if __name__ == '__main__':
    main(sys.argv)
