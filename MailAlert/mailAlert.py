#!/usr/sbin/env python

import os
import json

#MailList
Mail = { address.strip() for address in file('MailAddress').readlines() if len(address.strip()) > 0 }

#NodeList 
Node = { node.strip() for node in os.popen('pbsnodes -l all | cut -d" " -f1')}

#Load from Json
with open('SendTimes.json', 'r') as st :
	sendTimes = json.load(st)
	
#Check node state
Active = { line.strip() for line in os.popen('pbsnodes -l up | cut -d" " -f1').readlines()}
Node = Node.difference(Active)

chk = False
## Produce Mail Content
with open('MailText', 'w') as TEXT :

 	TEXT.write('***********************************************************\n')
        TEXT.write('                                                           \n')
        TEXT.write('                  Notice from NTNU HPC !                   \n')
        TEXT.write('                                                           \n')
        TEXT.write('***********************************************************\n')
        TEXT.write('\n')

	for downNode in Node:
		sendTimes[downNode] = sendTimes[downNode]+1
		print downNode+' has been offline for '+str(sendTimes[downNode]*10)+' minutes\n'

		if sendTimes[downNode] <= 3 : chk = True ;
		TEXT.write(downNode+' has been offline for '+str(sendTimes[downNode]*10)+' minutes\n')

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
