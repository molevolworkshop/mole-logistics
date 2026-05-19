#!/bin/bash

# This updates your local ~/.ssh/known-hosts file for all VMs listed in the VMIPS array

source ../all-vm-ips.sh # creates the variable VMIPS (array of all VM IP addresses)

for ip in ${VMIPS[@]}
do
    ssh-keyscan $ip >> ~/.ssh/known_hosts
done

# Keep only unique (-u) entries from known_hosts file and output (-o)
# the result to the known_hosts file (replacing the previous contents)
sort -u ~/.ssh/known_hosts -o ~/.ssh/known_hosts
