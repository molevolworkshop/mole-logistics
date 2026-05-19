# Setting up virtual machines

_Note that many of the files here were originally in prep folder in https://github.com/molevolworkshop/molevolworkshop.github.io. In May 2026, we created the mole-logistics and moved prep files here._

The whole process to set up virtual machines is described in `jetstream2026.md`, but the overall process is:
- We need allocation in ACCESS (https://access-ci.org/)
    - Note current allocation expires on July 20, 2026 and we need to request an extension (only PIs can do this: Tracy Heath and Jeremy Brown)
    - New allocation proposal can be submitted after that with new PIs
    - Every new project manager should apply for ACCESS account (co-directors and TAs)
- We use Jetstream2 Exosphere (https://jetstream2.exosphere.app/exosphere/) to create the virtual machines
    - To create the VMs, we need the public ssh keys of co-directors and TAs. Information on how to get these keys is in `ssh.md`
- After virtual machines are created, we need command line credentials to manage them. We need "ACCESS CILogon" through Openstack

# Late additions

Originally in `late-additions.zip` file at https://github.com/molevolworkshop/moledata, now we have scripts here to manage the VMs (except for shell scripts that list all the IP addresses for security purposes).

The structure of the folder for anyone that will run scripts on VMs should be:
```
virtual-machines/
    CLI-credentials/ ## gitignored; see "CLI credentials" section in jetstream2026.md
    late-additions/
        [all scripts in github]
        all-vm-ids.sh		
        all-vm-ips.sh
        faculty-vm-ids.sh
        faculty-vm-ips.sh	
        participant-vm-ids.sh			
        participant-vm-ips.sh
```
where the *-ids.sh and *-ips.sh scripts are gitignored because they contain the VMs IDs and IP addresses, but they can be shared offline.