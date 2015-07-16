#!/usr/pkg/bin/python2.7
from __future__ import print_function
# top: gives general info about process

import sys
import os

users = {}
with open('/etc/passwd', 'r') as f:
  for x in f:
    aux = x.split(':')
    users[aux[2]] = aux[0]


def _top():
    rows = int(os.popen('stty', 'r').read().split(' ')[0])
    headers = ['psi_v','type','endpoint','name','state','blocked','priority',
        'utime','stime','execycleshi','execycleslo', 'tmemory', 'cmemory', 
        'smemory', 'sleep', 'parentpid', 'realuid', 'effectiveuid', 'procgrp',
        'nicevalue', 'vfsblock', 'blockproc', 'ctrltty', 'kipchi', 'kipclo', 
        'kcallhi', 'kcalllo']

    txtheader = ['pid','realuid','priority','nicevalue','tmemory','state',
      'utime','execcycleslo','name']

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
    print('something about memory')
    print('cpu line 1')
    print('cpu line 2')
    print()
    print('{0: >5} {1: <8} {2: >3} {3: >4} {4: >5} {5: >5} {6: >6} {7: >7} {8: >7}'.format('PID', 'USERNAME', 'PRI', 'NICE', 'SIZE', 'STATE', 'TIME', 'CPU', 'COMMAND'))

    for proc,i in zip(topdata,range(8,rows)):
        for txt in txtheader:
            if txt == 'pid':
              s = '{0: >5}'
              value = proc[txt]
            elif txt == 'realuid':
              s = '{0: <8}'
              value = users[proc[txt]]
            elif txt == 'priority':
              s = '{0: >3}'
              value = proc[txt]
            elif txt == 'nicevalue':
              s = '{0: >4}'
              value = proc[txt]
            elif txt == 'tmemory':
              s = '{0: >5}'
              value = str(int(proc[txt])/1024)+'k'
            elif txt == 'state':
              s = '{0: >5}'
              value = 'RUN' if proc[txt] == 'R' else ''
            elif txt == 'utime':
              s = '{0: >6}'
              secs = int(proc[txt])
              mins = secs/60
              if mins >= 60:
                hours = mins//60
                mins = mins%60
              else:
                hours = 0
              value = str(hours)+':'+'{0:0>2}'.format(str(mins))
            elif txt == 'execcycleslo':
              s = '{0: >6}%'
              value = proc[txt] if txt in proc else '0.00'
            else:
              s = '{0}'
              value = proc[txt]
            print(s.format(value), end=' ')
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
