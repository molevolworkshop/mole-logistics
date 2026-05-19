#!/bin/bash

# Shelves all VMs (this causes them to stop burning any SUs)

# Comment out this line and the next to run this script
print("aborting because this script has already been run")
exit(0)

source ../../CLI-credentials/app-cred-CLI-MOLE-2026-credentials-openrc.sh
source ../all-vm-ids.sh # creates the variable VMIDS (array of all VM IDs)

for id in ${VMIDS[@]} ; do
	echo Shelving $id
    openstack server unlock $id
    openstack server shelve $id
    openstack server lock $id
done


 