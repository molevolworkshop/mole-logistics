#!/bin/bash


# Comment out this line and the next to run this script
print("aborting because this script has already been run")
exit(0)

source ../all-vm-ips.sh     # creates the variable VMIPS (array of all VM IP addresses)

for ip in ${VMIPS[@]}
do
    echo $ip
    scp paup moleuser@$ip:/tmp
    ssh -t moleuser@$ip "bash -c 'cd /tmp; chmod +x paup; sudo mv paup /usr/local/bin'"
done

