When trying to activate the environment with
. /var/pyenv/bin/activate
it doesn't work. In fact if we ls'd that directory we can see it is empty which is making me think the volume isn't mounted.

I think we need to modify this:
#!/bin/bash

MOLEBASE="149.165.150.186"
source ../all-vm-ips.sh     # creates the variable VMIPS (array of all VM IP addresses)

for ip in ${VMIPS[@]}
do
    ssh -t moleuser@$ip "bash -c 'sudo mount -t nfs $MOLEBASE:/media/volume/MOLE-data-2026/pyenv /var/pyenv'"
done
to loop over all IP addresses to mount