#!/usr/sbin/env python

import os
import json
import datetime

DATE = datetime.datetime.now().strftime("%Y%m%d")
TIME = datetime.datetime.now().strftime("%H:%M")
LOG  = open('/home/wlwu/tool/MailAlert/log/'+DATE, 'a')
LOG.write("\n=================\n")
LOG.write(TIME)
LOG.write("\n=================\n")

# MailList
Mail = { address.strip() for address in file('/home/wlwu/tool/MailAlert/MailAddress').readlines() if len(address.strip()) > 0 }

# NodeList
Node = { node.strip() for node in os.popen('/usr/local/bin/pbsnodes -l all | /usr/bin/cut -d" " -f1')}
Node.update(['oss1', 'oss2', 'mds'])

# Load from Json
with open('/home/wlwu/tool/MailAlert/SendTimes.json', 'r') as st :
        sendTimes = json.load(st)

# Check node
Active = { line.strip() for line in os.popen('/usr/local/bin/pbsnodes -l up | /usr/bin/cut -d" " -f1').readlines()}
Node = Node - Active

# Check lustre
TRY = 2
OSS1_Latency, OSS2_Latency, MDS_Latency = False, False, False
##oss1
S = os.popen('ping -c '+str(TRY)+' oss1 | tail -n 2 | head -n 1 | cut -d"," -f2 | cut -d" " -f2').readlines()[0]
if int(S.strip()) == TRY : Node.remove('oss1')
##oss2
S = os.popen('ping -c '+str(TRY)+' oss2 | tail -n 2 | head -n 1 | cut -d"," -f2 | cut -d" " -f2').readlines()[0]
if int(S.strip()) == TRY : Node.remove('oss2')
##mds
S = os.popen('ping -c '+str(TRY)+' oss1 | tail -n 2 | head -n 1 | cut -d"," -f2 | cut -d" " -f2').readlines()[0]
if int(S.strip()) == TRY : Node.remove('mds')

chk = False
## Produce Mail Content
with open('/home/wlwu/tool/MailAlert/MailText', 'w') as TEXT :

        TEXT.write('***********************************************************\n')
        TEXT.write('                                                           \n')
        TEXT.write('               Notification from NTNU HPC !                \n')
        TEXT.write('                                                           \n')
        TEXT.write('***********************************************************\n')
        TEXT.write('\n')

        for downNode in Node:
                sendTimes[downNode] = sendTimes[downNode]+1
                period = int(sendTimes[downNode])*10
                LOG.write(downNode+' has been offline for '+str(period/60)+' hours '+str(period%60)+' minutes\n')

                if sendTimes[downNode] <= 3 : chk = True ;
                TEXT.write(downNode+' has been offline for '+str(period/60)+' hours '+str(period%60)+' minutes\n')


## Mail to administrator
if chk :
        for address in Mail:
                 os.popen('/usr/bin/cat /home/wlwu/tool/MailAlert/MailText | /usr/bin/mail -s "Notification" '+address)
                LOG.write('Send notification to '+address)
elif len(Node) > 0 :
        LOG.write('Already offline over 30 minutes, skip...\n')
else :
        LOG.write('All green!\n')

##Refresh Json
for r in sendTimes :
        if not r in Node :
                if sendTimes[r] != 0 :
                        LOG.write( r + ' is online now !' )
                sendTimes[r] = 0 ;


## Dump to Json
with open('/home/wlwu/tool/MailAlert/SendTimes.json', 'w') as st :
        json.dump(sendTimes, st)

LOG.write('\n\n')
LOG.close()
