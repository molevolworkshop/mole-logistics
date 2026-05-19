# Late additions example scripts

Written 2026-05-12 by Paul O. Lewis

Note: to see this file properly formatted inside the Chrome browser, install the Markdown Preview Plus extension.

## Purpose

This directory contain example scripts that allow you to manage the virtual machines (VMs) used by the Woods Hole MBL Workshop in Molecular Evolution (MOLE). These scripts are useful once all the VMs have been cloned and are running. A typical use case is that a faculty member will decide that they need to replace a file on all VMs. These scripts make it pretty painless to carry out these kinds of operations, and often you can do such file replacements during a break or even while the participants are working on a different tutorial.

## Setup

The scripts that use openstack commands require that a sibling directory _CLI-credentials_ exists and contains a file named _-cred-CLI-MOLE-2026-credentials-openrc.sh_ that contains openstack credentials (see [instructions for obtaining credentials](https://molevolworkshop.github.io/jetstream2026/#obtaining-cli-credentials)). You also should have obtained a file names _clouds.yml_ that you have placed in your _~/.config/openstack_ directory.

## Usage

To use a script in this directory, simply source it into your current bash session. for example,

    . listIPs.sh
    
will use openstack to list all the IP addresses of all VMs.

The directories in which many of the scripts are stored have **dates incorporated into their names**. This is a convention, but not an essential one. I like to keep track of the order in which I applied late additions, and the date keeps their directories sorted. You can always run a script again (for example, the unlock, lock, unshelve, and shelve scripts); the **date in the directory name does not prevent you from running the script again**. 

For scripts that are potentially damaging if run more than once, I have inserted code at the top that must be commented out before the script can be executed. These lines are labeled and easy to find near the top of each script where such a sanity check matters. 

If you intend to change a script, I recommend duplicating the directory and changing the date to the current date in addition to changing the script. This preserves the history of changes in case that becomes important later.

## IPs and IDs

The files _all-vm-ips.sh_ and _faculty-vm-ips.sh_ contain the IP addresses of all VMs and just faculty/directors/TAs/course assistant VMs, respectively. This file should be updated if any VMs are deleted or created. These files are sourced in scripts that need to loop over an array of IP addresses.

The files _all-vm-ids.sh_ and _faculty-vm-ids.sh_ contain the openstack IDs of all VMs and just faculty/directors/TAs/course assistant VMs, respectively. This file should be updated if any VMs are deleted or created. These files are sourced in scripts that need to loop over an array of IDs.

You can get a list of all IP addresses using the script _listIPs.sh_. Likewise, you can get a list of all IDs using the script _listIDs.sh_.
