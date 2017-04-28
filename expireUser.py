#!/usr/bin/env python

import os
import subprocess

## Get rsync file of account list at /home/wwwsync/input/

homeDir = '/home/wwwsync/input/'

lockFile = 'disable.txt'
unlockFile = 'enable_aacount.txt'


for user in file(lockFile).readline():
        ## Chk usr whether is online
        pid = os.popen('who -u | grep '+user+' | tr -s " " | cut -d " " -f6 ').read()
        os.system('kill -9 '+pid)

        ## Make Usr account expired
        ssh = subprocess.Popen(['ssh', 'master', 'chage -E 0'+user], shell=False, stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        ## Rename Usr's authorized_keys in /home/USER/.ssh
        ssh = subprocess.Popen(['ssh', 'master', 'mv /home/'+user+'/.ssh/authorized_keys /home/'+user+'/.ssh/expire_keys'])
