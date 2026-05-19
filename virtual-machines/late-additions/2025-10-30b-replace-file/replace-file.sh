#!/bin/bash

# Example showing how to replace an executable file on each VM
# First, it copies (using scp) the file junk.sh to the /tmp directory on a VM
# Second, it makes the file executable and then moves it from /tmp to /usr/local/bin

# Comment out this line and the next to run this script
print("aborting because this script has already been run")
exit(0)

source ../all-vm-ips.sh     # creates the variable VMIPS (array of all VM IP addresses)

for ip in ${VMIPS[@]}
do
    echo $ip
    scp junk.sh moleuser@$ip:/tmp
    ssh -t moleuser@$ip "bash -c 'cd /tmp; chmod +x junk.sh; sudo mv junk.sh /usr/local/bin'"
done

