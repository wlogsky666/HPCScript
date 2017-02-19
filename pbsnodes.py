#!/usr/sbin/env python

from __future__ import print_function
import os
from collections import OrderedDict

def nameById(jobId):
        id = jobId[5:9]
        cmd = "qstat | grep " + id + " | awk '{print $3}'"
        return os.popen(cmd).readlines()[0].strip()

def colorT(text, colorCode):
        return '\x1b['+colorCode+'m'+text+'\x1b[0m'

pbs_cmd = 'pbsnodes -a'

nodeList, status = OrderedDict(), {}
nodeName = ''

for line in os.popen(pbs_cmd).readlines():
        if line.startswith(' '):
                paras = line.strip().split(',')
                for para in paras:
                        p = para.split('=')
                        if p[1].strip() == '' : p[1] = 'None' ;
                        if p[0] not in status:
                                status[p[0].strip()] = p[1].strip()
        else:
                if len(status) > 0 : nodeList[nodeName] = status ;
                nodeName = line.strip()
                status = {}
        # The format of GPU node is different from others

## Print detail of nodes

for node in nodeList:
        detail = nodeList[node]
        state = colorT(detail['state'].upper(), '1;32;40') if detail['state']=='free' else colorT(detail['state'].upper(), '1;34;40')

        print('{0:<10}   {1}'.format('['+node.upper()+']', state))
        print('   Job = {0}'.format(detail['jobs']), end=' ')
        if detail['jobs'] != 'None':
                print('  Owner = {0}'.format(nameById(detail['jobs'])))
        else : print('');

        print('   LoadAverage = {0}'.format(detail['loadave']), end='\t')
        totalMem, availMem = int(detail['totmem'][0:-2]), int(detail['availmem'][0:-2])
        usedMem = float(totalMem-availMem)
        print('Memory Used = {0:8.2f}MB  ['.format(round(usedMem/1024, 2)), end='')

        usedPercent = round(usedMem/totalMem*100, 2)
        if usedPercent >= 75 : print('\x1b[1;31;40m', end='');
        elif usedPercent >= 50 : print('\x1b[1;33;40m', end='');
        elif usedPercent >= 25 : print('\x1b[1;34;40m', end='');
        else :  print('\x1b[1;32;40m', end='');

        for ten in range(int(round(usedPercent/5))):
                print('|', end='')
        for space in range(20-int(round(usedPercent/5))):
                print(' ', end='')
        print( '\x1b[0m]  {0:5.2f}%'.format(usedPercent))

        print('')       ## seperate each line

