#!/bin/bash

# Renames "tmp 1 of 2"  through "tmp 2 of 2" 
#      to "apalone 1 of 14" through "apalone 2 of 14"

# Comment out this line and the next to run this script
print("aborting because this script has already been run")
exit(0)

source ../../CLI-credentials/app-cred-CLI-MOLE-2026-credentials-openrc.sh

openstack server set --name "apalone 1 of 14"   393b57a6-c718-4799-a2d9-2998a051ea78
openstack server set --name "apalone 2 of 14"   526b3826-8725-4178-84a5-697443237c1f
