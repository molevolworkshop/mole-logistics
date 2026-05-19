#!/bin/bash

# Running this script shows who is currently logged into each faculty VM
# It can be used to check whether anyone will be affected by
# another operation.

source ./faculty-vm-ips.sh

for ip in ${FACVMIPS[@]}
do
    ssh -t exouser@$ip "bash -c 'who'"
done


