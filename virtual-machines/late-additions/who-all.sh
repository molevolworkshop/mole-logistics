#!/bin/bash

# Running this script shows who is currently logged into each VM
# It can be used to check whether anyone will be affected by
# another operation.

source ./all-vm-ips.sh

for ip in ${VMIPS[@]}
do
    ssh -t moleuser@$ip "bash -c 'who'"
done

