#!/bin/bash

MOLEBASE="149.165.150.186"
source ../all-vm-ips.sh     # creates the variable VMIPS (array of all VM IP addresses)

for ip in ${VMIPS[@]}
do
    ssh -t moleuser@$ip "bash -c 'sudo mount -t nfs $MOLEBASE:/media/volume/MOLE-data-2026/pyenv /var/pyenv'"
done