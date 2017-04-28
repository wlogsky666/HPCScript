#!/usr/bin/env python

import os
import subprocess

## Get rsync file of account list at /home/wwwsync/input/

homeDir = '/home/wwwsync/input/'

lockFile = 'disable.txt'
unlockFile = 'enable_aacount.txt'


# Lock User
for user in file(lockFile).readlines():
        ## Chk usr whether is online
        cmd = 'who -u | tr -s " " | cut -d " " -f1,6'
        rst = os.popen(cmd).read()
        name = rst.split(' ')[0]
        pid = rst.split(' ')[1]

        if name == user.strip(): 
	        print(name, pid)
	        os.system('kill -9 '+pid)

        ## Make Usr account expired
        ssh = subprocess.Popen(['ssh', 'master', 'chage -E 0 '+name], shell=False, stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        ## Rename Usr's authorized_keys in /home/USER/.ssh
        os.popen('mv /home/'+name+'/.ssh/authorized_keys /home/'+name+'/.ssh/expire_keys' )



for user in file(unlockFile).readlines():

		## Make Usr account active
        ssh = subprocess.Popen(['ssh', 'master', 'chage -E -1 '+name], shell=False, stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        ## Rename Usr's authorized_keys in /home/USER/.ssh
        os.popen('mv /home/'+name+'/.ssh/expire_keys /home/'+name+'/.authorized_keys' )
