#!/usr/sbin/env python

import os
import json

#MailList
Mail = { address.strip() for address in file('MailAddress').readlines() if len(address.strip()) > 0 }

#NodeList 
Node = {'node'+str(i) for i in range(1, 45)}
Node.update({'bigmem'+str(i) for i in range(1, 7)})
Node.update({'gpu'+str(i) for i in range(1, 3)})

#Load from Json
with open('SendTimes.json', 'r') as st :
	sendTimes = json.load(st)

#Check node state
for line in os.popen('pbsnodes -l all | tr -s " "').readlines():
        nodeName, state = line.strip().split(' ')[0:2]
        if state.strip() == 'free' or state == 'job-exclusive' :
                Node.remove(nodeName)

chk = False
## Produce Mail Content
TEXT = file('MailText', 'w')

TEXT.write('***************************************************************\n')
TEXT.write('  								   \n')
TEXT.write('                   Notice from NTNU HPC !                      \n')
TEXT.write('                                                               \n')
TEXT.write('***************************************************************\n')
TEXT.write('\n')

for downNode in Node:
	sendTimes[downNode] = sendTimes[downNode]+1
	print downNode+' has been offline for '+str(sendTimes[downNode]*10)+' minutes\n'

	if sendTimes[downNode] <= 3 : chk = True ;
	TEXT.write(downNode+' has been offline for '+str(sendTimes[downNode]*10)+' minutes\n')

TEXT.close()

## Mail to administrator
if chk :
	for address in Mail:
		os.popen('cat MailText | mail -s "Notice from HPC!" '+address) 
		print 'Send notification to ', address 
elif len(Node) > 0 :
	print 'Already offline over 30 minutes, skip...'
else :
	print 'All green!'	

##Refresh Json
for r in sendTimes :
	if not r in Node : sendTimes[r] = 0 ;

## Dump to Json
with open('SendTimes.json', 'w') as st :
	json.dump(sendTimes, st)
