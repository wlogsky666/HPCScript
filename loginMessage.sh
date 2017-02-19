#!/bin/sh

echo '###########################################################################'
echo '##                                                                       ##'
echo '##                          HPC Cluseter of NTNU                         ##'
echo '##                                                                       ##'
echo '###########################################################################'

#nodes info

echo ''
echo 'Information of computing nodes:'
echo ''

##Queue info

echo '==========================================================================='
echo 'Information of Queues:'
echo ''

echo 'q24cores   :'
echo 'q48cores   :'
echo 'q96cores   :'
echo 'q192cores  :'
echo 'q384cores  :'
echo 'bigmem128  :'
echo 'bigmem1024 :'
echo 'gpu        :'
echo 'test		 :'
echo ''

##Note

echo '==========================================================================='
echo 'Notice:'
echo ''

echo '1. Please use queueing system to submit your jobs.'
echo '2. Please use /lustre/lwork/YOUR_ACCOUNT as your working directory.'
echo '3. Please put your tmp files in /tmp instead of global space.'
echo '4. Please check your job status frequently.'
echo '5. Please clean your tmp files after job finished.'
