#!/bin/bash

# Replace the machine learning files with those 
# supplied by Megan Smith on May 4, 2026.

# This section prevents this script from being run accidentally
# Comment out this line and the next to run this script
print("aborting because this script has already been run")
exit(0)

source ../all-vm-ips.sh     # creates the variable VMIPS (array of all VM IP addresses)

for ip in ${VMIPS[@]}
do
    # Show the ip address of the VM
    printf "\nVisiting $ip\n"
    
    # Copy files to /tmp on remote VM
    scp files/Machine_Learning_for_Population_Genetics_V2.py moleuser@$ip:/tmp
    scp files/simulated_responses.npy                        moleuser@$ip:/tmp
    scp files/simulated_sfs.npy                              moleuser@$ip:/tmp
    
    # Remove current contents of /usr/local/share/examples/mole/machinelearning
    # and replace with the three new files 
    # The ssh -t option forces pseudo-terminal emulation
    # the bash -c option specifies that commands are coming and disables interactive communication
    ssh -t moleuser@$ip "bash -c 'cd /tmp; \
        sudo rm -f /usr/local/share/examples/mole/machinelearning/*; \
        sudo mv Machine_Learning_for_Population_Genetics_V2.py /usr/local/share/examples/mole/machinelearning; \
        sudo mv simulated_responses.npy                        /usr/local/share/examples/mole/machinelearning; \
        sudo mv simulated_sfs.npy                              /usr/local/share/examples/mole/machinelearning' \
    "
done

