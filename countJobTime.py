#!/usr/bin/env python

'''
This script is used to count used time of each job
Log files are located in /var/spool/torque/server_priv/accounting/ on master node

'''

import os
import datetime
import subprocess

## Get date of yesterday
## Log file will create at ?? every day
day = datetime.date.today() - datetime.timedelta(days=1)

filename = '/var/spool/torque/server_priv/accounting' + day.strftime("%Y%m%d")
#print('Get log file : '+filename)

ssh = subprocess.Popen(['ssh', 'master', 'less '+filename+' | grep -e cput | cut -d" " -f10,22'], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

for line in ssh.stdout.readlines():
        print(line)
        print

