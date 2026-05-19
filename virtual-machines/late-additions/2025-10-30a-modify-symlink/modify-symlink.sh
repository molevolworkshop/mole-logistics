#!/bin/bash

# Running this script fixes the ~/moledata symbolic link on each test VM
#   Incorrect: /usr/local/share/mole
#   Correct:   /usr/local/share/examples/mole

# Comment out this line and the next to run this script
print("aborting because this script has already been run")
exit(0)

source ../all-vm-ips.sh     # creates the variable VMIPS (array of all VM IP addresses)
                
for ip in ${VMIPS[@]}
do
    ssh -t moleuser@$ip "bash -c 'rm moledata; ln -s /usr/local/share/examples/mole moledata'"
done
