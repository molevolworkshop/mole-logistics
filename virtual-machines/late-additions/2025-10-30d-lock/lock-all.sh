#!/bin/bash

# Locks all VMs (preventing them from accidentally being deleted)

# Comment out this line and the next to run this script
print("aborting because this script has already been run")
exit(0)

source ../../CLI-credentials/app-cred-CLI-MOLE-2026-credentials-openrc.sh
source ../all-vm-ids.sh # creates the variable VMIDS (array of all VM IDs)

for vm in ${VMIDS[@]} ; do
	echo Locking $vm
    openstack server lock $vm
done


 