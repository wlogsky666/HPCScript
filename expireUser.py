#!/usr/bin/env python

import os
import subprocess


'''
Get rsync file of ban list at 

'''

banList = '/home/?'


for user in file(banList+'list.txt').readline():
	## Chk usr whether is online
	pid = os.popen('who -u | tr -s " " | cut -d " " -f6 ').read()
	os.system('kill -9 '+pid)

	## Make Usr account expired
	ssh = subprocess.Popen(['ssh', 'master', 'chage -E 0'], shell=False, stdout=subprocess.PIPE,stderr=subprocess.PIPE)

	## Rename Usr's authorized_keys in /home/USER/.ssh
	ssh = subprocess.Popen(['ssh', 'master', 'mv /home/'+user+'/.ssh/authorized_keys /home/'+user+'/.ssh/expire_keys'])
