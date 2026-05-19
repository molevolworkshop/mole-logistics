#!/bin/bash

# Unlocks all VMs

# Comment out this line and the next to run this script
print("aborting because this script has already been run")
exit(0)

source ../../CLI-credentials/app-cred-CLI-MOLE-2026-credentials-openrc.sh
source ../participant-vm-ids.sh     # creates the variable VMIDS (array of all VM IDs)

for vm in ${VMIDS[@]} ; do
	echo Unlocking $vm
    openstack server unlock $vm
done


