from __future__ import print_function
# ps: gives general info about process of the current user

import sys
import os
import argparse

def listprocs(tty=True, longv=False, notty=False, endpoint=False, all=False):
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

    for proc in procs:
        with open('/proc/{}/psinfo'.format(proc), 'rb') as f:
          procdata = dict(zip(headers,f.read().split(' ')))
          procdata['pid'] = proc
          topdata.append(procdata)
        if procdata['state'] == 'R':
          running += 1
          
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

def main(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('-a', action='store_true',
        help='Show only process with an attached tty')
    parser.add_argument('-e', action='store_true',
        help='Proccess Envirnoment after ps execution')
    parser.add_argument('-E', action='store_true',
        help='endpoint kernel instead of PID')
    parser.add_argument('-f', action='store_true',
        help='Long format')
    parser.add_argument('-l', action='store_true',
        help='Long format')
    parser.add_argument('-x', action='store_true',
        help='Adds processes with no attached tty')
    parser.add_argument('args', nargs=argparse.REMAINDER)

    argv = parser.parse_args()

    if argv.a or argv.e or argv.E or argv.f or argv.l or argv.x:
      listprocs(tty=argv.a, longv=(argv.f or argv.l), notty=argv.x, endpoint=argv.E, all=argv.e)
    else:
      listprocs()

if __name__ == '__main__':
    main(sys.argv)
