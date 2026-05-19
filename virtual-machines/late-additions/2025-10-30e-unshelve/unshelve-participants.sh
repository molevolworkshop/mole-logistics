#!/bin/bash

# Unshelves participants VMs (this causes them to begin burning SUs at a rate of 2/hour)

# Comment out this line and the next to run this script
print("aborting because this script has already been run")
exit(0)

source ../../CLI-credentials/app-cred-CLI-MOLE-2026-credentials-openrc.sh
source ../participant-vm-ids.sh # creates the variable VMIDS (array of all VM IDs)

for vm in ${VMIDS[@]} ; do
	echo Unshelving $vm
    openstack server unlock $vm 
    openstack server unshelve $vm
    openstack server lock $vm 
done


