#!/usr/sbin/env python

from __future__ import print_function
import os
import sys

usage = lambda: print('[Usage]\n\tpython '+sys.argv[0]+' User Passwd Group')

## Only root is permitted to create user

shellUser = os.popen('id -un').readlines()[0].strip()
print("Check root  ... "+shellUser)
if shellUser != 'root':
        print('Permission denied ! Please run script as admin')
        sys.exit(0)

## Check on master node or not

node = os.popen("uname -a | awk '{print $2}'").readlines()[0].strip()
print('Check node  ... '+node)
if node != 'master':
        print('Not on master node, ssh master plz')
        sys.exit(0)

## Check args

print('Check args  ... '+('OK' if len(sys.argv) == 4 else 'X') )
if len(sys.argv) != 4 :
        usage()
        sys.exit(0)

## Check existence of user and group

user, password, group = sys.argv[1:4]
newgrp = True

print('Check user  ... ', end='')
chkusr = os.popen('less /etc/passwd | grep '+user).readlines()
for u in chkusr:
        if u.startswith(user+':'):
                print(user+' already exists')
                sys.exit(0)

print('unduplicated');

print('Check group ... ', end='')
chkgrp = os.popen('less /etc/group | grep '+group).readlines()
for grp in chkgrp:
        if grp.startswith(group+':'):
                newgrp = False
                break
if newgrp :
        print(group+' not exists, ', end='')
        print('will create group '+group+' automatically')
else : print(grp.strip())

## Confirm
print('\n[Confirmation] ')
print('\tUser  : '+user)
print('\tPasswd: '+password)
print('\tGroup : '+group)

confirm = raw_input('Are you sure to create account? (y/n) ..> ')

while confirm != 'y' and confirm != 'n':
        confirm = raw_input('Please enter y or n ..> ')

if confirm == 'n' : sys.exit(0)


###################################### SOP #####################################

## Group

if newgrp:
        cmd = 'groupadd '+group
        print(cmd)
        #os.system(cmd)

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

cmd = 'echo -e "\n\n\n" | ssh-keygen -t rsa'
print(cmd)
#os.system(cmd)

cmd = 'cp /home/'+user+'/.ssh/id_rsa.pub /home/'+user+'/.ssh/authorized_keys'
print(cmd)
#os.system(cmd)

#os.system('exit')
