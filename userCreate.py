#!/usr/sbin/env python

from __future__ import print_function
import os
import sys

usage = lambda: print('[Usage]\n\tpython '+sys.argv[0]+' User Group Passwd')

## Only root is permitted to create user

shellUser = os.popen('id -un').readlines()[0]
if shellUser == 'root':
        print('Permission denied ! Please run script as admin')
        sys.exit(0)

## Check master

if os.popen("uname -a | awk '{print $2}'").readlines()[0].strip() != 'master':
        print('Not on master node, ssh master plz')
        sys.exit(0)

## Check args

if len(sys.argv) != 4 :
        usage()
        sys.exit(0)

## Check existence of user and group

user, group, password = sys.argv[1:4]
newgrp = True

chkusr = os.popen('id '+user).readlines()
if len(chkusr) > 0 :    ## User exists
        print('user '+user+' already exists')
        sys.exit(0)

chkgrp = os.popen('less /etc/group | grep '+group).readlines()
for grp in chkgrp:
        if grp.startswith(group+':'):
                newgrp = False
if newgrp :
        print('Group not exists, will create group '+group+' automatically')

## Confirm
print('\nConfirm :')
print('\tUser: '+user)
print('\tGroup: '+group)

confirm = raw_input('Are you sure to create account? (yes/no) ..> ')

while confirm != 'yes' and confirm != 'no':
        confirm = raw_input('Please enter yes or no ..> ')

if confirm == 'no' : sys.exit(0)


###################################### SOP #####################################

## Group

if newgrp:
        pass

## User

cmd = 'useradd -m '+user+' -g '+group
print(cmd)
#os.system(cmd)

cmd = 'echo '+password+' | passwd '+user+' --stdin'
print(cmd)
#os.system(cmd)

cmd = 'make -C /var/yp'
print(cmd)
#os.system(cmd)

cmd = 'cp /home/jcchen/.ssh/known_hosts /home/'+user+'/.ssh/'
print(cmd)
#os.system(cmd)

cmd = 'chown '+user+':'+group+' /home/'+user+'/.ssh/known_hosts'
print(cmd)
#os.system(cmd)

cmd = 'mkdir /lustre/lwrok/'+user
print(cmd)
#os.system(cmd)

cmd = 'chown '+user+':'+group+' /lustre/lwork/'+user
print(cmd)
#os.system(cmd)

## Change to user

cmd = 'su - '+user
print(cmd)
#os.system(cmd)

cmd = 'ssh-keygen -t rsa'
print(cmd)
#os.system(cmd)

cmd = 'cp /home/'+user+'/.ssh/id_rsa.pub /home/'+user+'/.ssh/authorized_keys'
print(cmd)
#os.system(cmd)
