#!/bin/bash

## This script syncs data between hpc and web server
## HPC:/home/wwwsync/output -> WEB:/home/hpc/input
## WEB:/home/hpc/ouput -> HPC:/home/wwwsync/input

## Execute every hour or xx:55 by root


NOW=$(date +"%Y%m%d")

echo "=====================================================" >> /home/wwwsync/log_sync/"$NOW.sync.record"
echo "$(date +"%Y%m%d%H%M")" >> /home/wwwsync/log_sync/"$NOW.sync.record"

# sync to remote
rsync -avzh --delete /home/wwwsync/output/ hpc@140.122.63.103:/home/hpc/input/  >> /home/wwwsync/log_sync/"$NOW.sync.record"

# sync from remote
rsync -avzh --delete hpc@140.122.63.103:/home/hpc/output/ /home/wwwsync/input/  >> /home/wwwsync/log_sync/"$NOW.sync.record"
