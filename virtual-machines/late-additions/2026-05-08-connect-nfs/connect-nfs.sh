#!/bin/bash

# Connects NFS share on MOLE-2026-base to all VMs

# This section prevents this script from being run accidentally
# Comment out this line and the next to run this script
print("aborting because this script has already been run")
exit(0)

molebase="149.165.150.186"

source ../all-vm-ips.sh # creates the variable VMIPS (array of all VM IP addresses)
 
for ip in ${VMIPS[@]}
do
    ssh -t moleuser@$ip "bash -c '\
    printf \"\\nVisiting $ip\\n\"; \
    sudo umount /var/pyenv; \
    # this should not be necessary: sudo mkdir -p /var/pyenv; \
    sudo chown -R moleuser:moleuser /var/pyenv; \
    sudo mount -t nfs $molebase:/media/volume/MOLE-data-2026/pyenv /var/pyenv'"
done
