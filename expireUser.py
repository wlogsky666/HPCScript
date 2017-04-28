#!/usr/bin/env python

import os
import subprocess

## Get rsync file of account list at /home/wwwsync/input/

homeDir = '/home/wwwsync/input/'

lockFile = 'disable.txt'
unlockFile = 'enable_aacount.txt'


# Lock Usr
for user in file(lockFile).readlines():
         ## Chk usr whether is online
        pid = os.popen('who -u | grep -w '+user.strip()+' | tr -s " " | cut -d " " -f6 ').read()

        # Kick Usr
        if len(pid) > 0 :
                os.system('kill -9 '+pid)

        ## Make Usr account expired
        ssh = subprocess.Popen(['ssh', 'master', 'chage -E 0 '+user.strip()], shell=False, stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        ## Rename Usr's authorized_keys in /home/USER/.ssh
        os.popen('mv /home/'+user.strip()+'/.ssh/authorized_keys /home/'+user.strip()+'/.ssh/expire_keys' )

# Unlock Usr
for user in file(unlockFile).readlines():
        ## Make Usr account active
        ssh = subprocess.Popen(['ssh', 'master', 'chage -E -1 '+user.strip()], shell=False, stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        ## Rename Usr's authorized_keys in /home/USER/.ssh
        os.popen('mv /home/'+user.strip()+'/.ssh/expire_keys /home/'+user.strip()+'/.authorized_keys' )
