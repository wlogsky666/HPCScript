#!/usr/bin/env python

import os
import subprocess
import time
import datetime

## Debug Option
debug = False
lock = False

## Get rsync file of account list at /home/wwwsync/input/

homeDir = '/home/wwwsync/input/'
lockFile = 'disable_account.txt'
unlockFile = 'enable_account.txt'

if debug:
        homeDir = './'
        print 'Debug Mode...'
        if lock:
                lockFile, unlockFile = unlockFile, lockFile

ima = datetime.datetime.now().strftime("%Y%m%d-%H%M")
log = file('./log/'+datetime.datetime.now().strftime("%Y%m%d"), 'a')

log.write(ima)
log.write('\n[Lock User]')
# Lock Usr
for user in file(homeDir+lockFile).readlines():
        if len(user.strip()) == 0 : continue ;
        ## Chk user has already been locked
        s = os.popen('ssh master "passwd -S '+user.strip()+' | cut -d\' \' -f9"')
        if s.readlines()[0].startswith('locked.') : continue ;

        log.write( user.strip())
        ## Chk usr whether is online
        os.system('pkill -9 -u '+user.strip())
        print 'pkill -9 -u '+user.strip()

        ## Make Usr account expired
        ssh = subprocess.Popen(['ssh', 'master', 'passwd --lock '+user.strip()], shell=False, stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        ## Rename Usr's authorized_keys in /home/USER/.ssh
        os.system('mv /home/'+user.strip()+'/.ssh/authorized_keys /home/'+user.strip()+'/.ssh/xauthorized_keys')


log.write('\n[Unlock User]')
# Unlock Usr
for user in file(homeDir+unlockFile).readlines():
        if len(user.strip()) == 0 : continue;
        ## Chk user has already benn unlocked
        s = os.popen('ssh master "passwd -S '+user.strip()+' | cut -d\' \' -f9"')
        if s.readlines()[0].startswith('set') : continue ;

        log.wrtie(user.strip())
        ## Make Usr account active
        ssh = subprocess.Popen(['ssh', 'master', 'passwd --unlock '+user.strip()], shell=False, stdout=subprocess.PIPE,stderr=subprocess.PIPE)

                 ## Rename Usr's authorized_keys in /home/USER/.ssh
        os.popen('mv /home/'+user.strip()+'/.ssh/xauthorized_keys /home/'+user.strip()+'/.ssh/authorized_keys' )


# wait until passwd refresh
time.sleep(3)
log.write('\n[/var/yp]')

# yp
yp = subprocess.Popen(['ssh', 'master', 'make -C /var/yp'], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

out = yp.stdout.readlines()
for r in out:
        log.write(r)

         
