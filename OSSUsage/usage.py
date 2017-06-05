#!/usr/sbin/env python

import os
import datetime
import time
import subprocess

NOW = datetime.datetime.now().strftime("%Y/%m/%d-%H:%M")
CMD1 = 'iostat /dev/mapper/mpathe /dev/mapper/mpathf | tail -n 3 | tr -s " " | cut -d" " -f5,6 | head -n 2'

with open("/home/wlwu/tool/OSSUsage/OSS1.csv", 'a') as f :
	f.write(NOW+',')
	
	## OSS1 
	ssh = subprocess.Popen(["/usr/bin/ssh", 'oss1', CMD1], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	time.sleep(1)
	ssh1 = subprocess.Popen(["/usr/bin/ssh", 'oss1', CMD1], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	rst, rst1 = ssh.stdout.readlines(), ssh1.stdout.readlines()

	prev_read_e, prev_write_e = rst[0].strip().split(' ')
	prev_read_f, prev_write_f = rst[1].strip().split(' ')
	cur_read_e, cur_write_e = rst1[0].strip().split(' ')
	cur_read_f, cur_write_f = rst1[1].strip().split(' ')

	f.write( str(int(cur_read_e)-int(prev_read_e))+',' )
	f.write( str(int(cur_write_e)-int(prev_write_e))+',' )
	f.write( str(int(cur_read_f)-int(prev_read_f))+',' )
        f.write( str(int(cur_write_f)-int(prev_write_f))+',' )

	f.write(prev_read_e+','+prev_write_e+','+ prev_read_f+','+prev_write_f+',')
	f.write(cur_read_e+','+cur_write_e+','+ cur_read_f+','+cur_write_f+'\n')

	#print prev_read_e, prev_write_e
	#print prev_read_f, prev_write_f
	#print cur_read_e, cur_write_e
	#print cur_read_f, cur_write_f

with open("/home/wlwu/tool/OSSUsage/OSS2.csv", 'a') as f :
        f.write(NOW+',')

        ## OSS1
        ssh = subprocess.Popen(["/usr/bin/ssh", 'oss2', CMD1], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(1)
        ssh1 = subprocess.Popen(["/usr/bin/ssh", 'oss2', CMD1], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        rst, rst1 = ssh.stdout.readlines(), ssh1.stdout.readlines()

        prev_read_e, prev_write_e = rst[0].strip().split(' ')
        prev_read_f, prev_write_f = rst[1].strip().split(' ')
        cur_read_e, cur_write_e = rst1[0].strip().split(' ')
        cur_read_f, cur_write_f = rst1[1].strip().split(' ')

        f.write( str(int(cur_read_e)-int(prev_read_e))+',' )
        f.write( str(int(cur_write_e)-int(prev_write_e))+',' )
        f.write( str(int(cur_read_f)-int(prev_read_f))+',' )
        f.write( str(int(cur_write_f)-int(prev_write_f))+',' )

        f.write(prev_read_e+','+prev_write_e+','+ prev_read_f+','+prev_write_f+',')
	f.write(cur_read_e+','+cur_write_e+','+ cur_read_f+','+cur_write_f+'\n')

        #print prev_read_e, prev_write_e
        #print prev_read_f, prev_write_f
        #print cur_read_e, cur_write_e
        #print cur_read_f, cur_write_f
	



