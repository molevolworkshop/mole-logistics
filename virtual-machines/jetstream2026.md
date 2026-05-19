---
layout: page
title: Jetstream2 Setup Notes (2026)
permalink: /jetstream2026/
---
{% comment %}
https://www.webfx.com/tools/emoji-cheat-sheet/
{% endcomment %}

## Jetstream2 notes (2026 Workshop)

These are notes on setting up Jetstream2 virtual machines for the 2026 MOLE workshop. If you are a participant, these notes are not intended for you, but you are of course welcome to read them. They are intended for the current directors and head TA of the workshop, who must get the Jetstream virtual machines up and running before the workshop begins. 

[Paul Lewis](mailto:paul.lewis@uconn.edu) created this document 16-Oct-2026.

This document supersedes the original [Jetstream Setup Notes](/jetstream-setup/) and the later [Jetstream2 Setup Notes 2022](/jetstream2022/), [Jetstream2 Setup Notes 2023](/jetstream2023/), [Jetstream2 Setup Notes 2023](/jetstream2024/), and [Jetstream2 Setup Notes 2024](/jetstream2025/).

## Introduction

Starting in 2022, the Workshop began using a "cluster in the cloud" for its computing needs.

The cluster we will be using is from the [Jetstream2](https://jetstream-cloud.org) project at Indiana University. Jetstream was NSF's first science and engineering research cloud, completed in early 2016 at a cost of $6.6M. Jetstream is one source of computing infrastructure provided under the umbrella of [Xsede](https://www.xsede.org), the Extreme Science and Engineering Discovery Environment, an NSF-sponsored program that provided cloud computing for researchers in academia. 

### History 

Peter Beerli and I applied to Xsede for an educational **allocation** to provide enough computing resources for the Workshop in 2020. [Here](/assets/pdf/jetstream-proposal.pdf) is our proposal. We were awarded 207360.0 SUs (Service Units), which would allow 120 4-core virtual machines to run continuously for 18 days (120*4*24*18 = 207360 core*hours). The Workshop was sidelined due to the COVID pandemic in 2020 and again in 2021.

[Jetstream2](https://jetstream-cloud.org) was just coming online in the spring of 2022 and, while we could have continued to use Jetstream through the 2022 workshop, we were encouraged to go ahead and switch over to Jetstream2, which had the benefit of being better prepared for the 2023 Workshop when Jetstream2 would be the only version available.

Between the 2022 and 2023 Workshops, Xsede was replaced by [Access](https://access-ci.org). The Workshop directors (Peter Beerli, Laura Kubatko) and I submitted an [Explore ACCESS proposal](/assets/pdf/2022-11-24-ACCESS-proposal.pdf) in November 2022 asking for 68,080 SUs for the 2023 Workshop. We were actually granted 100,000 SUs.

For the 2024 workshop, we were granted an extension because we had used less than half of the SUs allocated for the 2023 workshop.

I began building the 2025 master virtual machine instance on May 9, 2025. At that time there were 173,891 SUs remaining in the DEB190022 allocation. On the last day of the workshop (June 1, 2025), there were 133,868 SUs remaining, and there were 127,412 on June 3 when I finished deleting all the virtual machines. Thus, the workshop burned 46,479 SUs in total in 2025.

At the end of July, 2025, Jeremy Brown submitted an extension request that was granted 31-July-2025. The new end date is Project: 2026-07-30. Technically, the extension was granted to Tracy Heath, who is still PI, because apparently changes to PI and Co-PI cannot be made for a continuing allocation. As of 16-Oct-2025, there were 127,053 SUs remaining in DEB190022. I met with Claudia and Jeremy to begin the process of setting up the MOLE-BASE-2026 virtual machine.

On May 10, 2026, one week before the 2026 workshop began, there were 125,024 SUs remaining in allocation DEB190022, with 7 VMs plus MOLE-2026-base burning a total of 8*2=15 SUs/hour.

### High-level Overview

The basic procedure for setting up computing for next year (2027) is as follows:

* The current allocation expires July 20, 2026, so it is important to request an extension on the ACCESS web site well before that date.

* Anyone new to the project (e.g. new allocation manager) should apply for an ACCESS account at [https://access-ci.org/](https://access-ci.org/).

* ACCESS provides an _allocation_ of computing resources that can be "spent" at any number of participating computing centers. Our course has always used the JetStream2 resource at Indiana University in Bloomington, IN. This is an extremely well-run center, and I heartily recommend staying with them for future workshops if at all possible.

* You will use Jetstream2's Exosphere web interface [https://jetstream2.exosphere.app/exosphere/](https://jetstream2.exosphere.app/exosphere/) to create the master virtual machine (VM) that provides the image cloned to create the faculty, TA, and participant VMs. This year this master VM is named _MOLE-2026-base_.

* Most of this document is concerned with setting up the master VM after it is created. I go through this process every year rather than just cloning last year's image because operating systems and software change somewhat over the year and I like to have everything up-to-date. It will take a couple of hours to set up the master but only seconds to clone all the VMs using a snapshot image of the master VM. It behooves you to communicate with faculty and TAs early in the year to try to get all the updated software and tutorial data installed before cloning.

* After you get all the VMs up and running, you should _shelve_ and _lock_ all of them until just before the course begins. If you follow the instructions below, you will create 2-core VMs that burn 2 SUs (Service Units) from your allocation each hour they are unshelved. While they are shelved, they burn 0 SUs, so it is _very_ important to keep them shelved unless you are actually using them. Note that _shelving_ is one of several states that sound similar, but shelving is the only one that does not burn SUs. Once the workshop begins, I let all the VMs run continuously for the entire workshop. It would be relatively simple to shelve them each evening at 10pm and unshelve them all again in the morning, but I fear that some students will want to run tutorials late at night and would be frustrated to find their VM shelved.

* After the VMs are up and running, I seldom use the Exosphere web interface. Instead, I use command line tools (the CLI interface) that allow me to run scripts that loop over all the VMs. This allows you to, for example, quickly and easily replace a file on all VMs. Once the master VM has been cloned, this is the only way to make a change to all the clones apart from deleting them all and re-cloning, which would take much more time and effort. The command line tools require you to have created a file that is a sort of private key that has the allocation information baked in (see section [Obtaining CLI credentials](#obtaining-cli-credentials) below. Your script must `source` that file to be allowed to do anything with the VMs. Obtaining the credentials file requires you to login to a third web site (the other two being [ACCESS](https://access-ci.org/) and JetStream2's [Exosphere](https://jetstream2.exosphere.app/exosphere/)) called [Horizon](https://js2.jetstream-cloud.org/). This is probably the only thing you will need to do on the horizon web interface.

* IP addresses are a restricted resource. You should create all the VMs without asking for IP addresses. Once they are created, you can request the same number of floating IP addresses and (with the command line tools) assign a floating IP to each VM.

* The TAs and course directors must be able to easily login to any VM without needing a password. This makes it easy to (for example) reset a participant's password if they have forgotten it. To do this, you will use the cloud-init script supplied when creating VMs from the master image to add SSH public keys for each person who needs easy access. We also use the cloud-init script to set up the `moleuser` user and create several aliases that make some software easy to start. There is a second user baked into each VM (`exouser`), and one SSH public key will be specified when creating the VMs to allow that one person to always be able to login as exouser. This is a good backup in case something about the moleuser account gets trashed. (Because they have sudo privileges on their own VM, some students do some pretty crazy things sometimes, such as (real example) changing the ownership of every file and directory to "everyone" because the person liked the warning colors that were then used to show that files and directories were totally unprotected.)

### Helful links

These have proven to be useful resources to have handy.

* [Jetstream2 status](https://jetstream.status.io/)
* [Jetstream2 home page](https://jetstream-cloud.org)
* [Jetstream2 documentation](https://docs.jetstream-cloud.org)
* [Exosphere](https://jetstream2.exosphere.app/)
* [Exosphere documentation](https://docs.jetstream-cloud.org/ui/exo/exo/)
* [Horizon home page](https://js2.jetstream-cloud.org/)
* [OpenStack command list](https://docs.openstack.org/python-openstackclient/yoga/cli/command-objects/server.html)
* [Jetstream2 API tutorial](https://github.com/jlf599/JetstreamAPITutorial)
* [Cloud-init examples](https://cloudinit.readthedocs.io/en/latest/reference/examples.html)

## Creating and setting up the MOLE master virtual machine

The master virtual machine will be referred to throughout this document as `MOLE-2026-base`.

### Most important!

Be sure to **shelve** instance if not planning to work with it for several hours. Shelving is the only option that does not burn SUs. Despite their names seeming to mean the same thing, **suspending** burns SUs at 75% of the normal rate and **stopping** burns SUs at 50% the normal rate. See [Instance management actions](https://iujetstream.atlassian.net/wiki/spaces/JWT/pages/537460754/Instance+management+actions) for more info.

### Notation and conventions

I will use the dollar sign (`$`) at the beginning of a line of code to show that the command is being entered as the normal user. I will use the hash symbol (`#`) at the beginning of a line of code to show that the command is being entered as the super user. That said, superuser commands will almost always be entered using the `sudo` command. If a line of code does not begin with either `#` or `$`, then it represents output of the command.

### Logging into Exosphere

[Exosphere](https://jetstream2.exosphere.app/) is a graphical user interface for managing your allocation. I was able to login using my ACCESS credentials and add our allocation to the Jetstream2 platform.

### SSH stuff

Using the red **Create** button in the upper right corner of Exosphere, I chose _SSH Public Key_ to upload my ssh public key. I named it `cormy` and pasted in the contents of the public key file _~/.ssh/id_rsa.pub_ on my local laptop.

**Ideally, the computer you use to set up everything should be the one you plan to have with you at Woods Hole.**

Once you have created an instance to login to (see next section below), you can create an entry in your (local laptop's) _~/.ssh/config_ file to make it easy to login.
~~~~~~
Host molevm
    HostName 149.165.156.59
    User plewis
    IdentityFile /Users/plewis/.ssh/id_rsa
~~~~~~    
        
Now you will be able to ssh an instance you create using the _molevm_ host set up in _.ssh/config_ file:

    ssh molevm

### Creating the instance to be used as the base image

To create a new instance, click the red **Create** button in the upper right corner of Exosphere. 

I used the **Ubuntu 24.04 (latest)** image source and specified **MOLE-2026-base** as the name. I chose **m3.small** as the flavor, **20 GB** root disk size (default for selected flavor), **1** for number of instances, **no** for enable web desktop, **cormy** for SSH public key, and **Show** for Advanced Options. (Note that you should specify your own SSH public key, **not cormy**).

**About disk size:** The VMs we are using have 18.33GB of disk space of which about 16GB is taken up by the operating system and the software and data files we install. Thus, participants will have only about 2 GB to play with. Participants will thus need to off-load important files to their laptops to maintain some working disk space. Why are we so limited? The main reason is that, to get a larger disk, we would need to go to 8-core VMs, which burn 8 SU (service units) per hour rather than the 2 SUs/hour burn rate of the current 2-core VMs. Given that we have a limited number of SUs given to us by ACCESS, it is better to be frugal with disk space than risk running out of SUs before the workshop ends.

Advanced Options:

| Name                                     | Value                  | Default? |
| ---------------------------------------- | ---------------------- | -------- |
| Install operating system updates?        | Yes                    | Yes      |
| Deploy Guacamole for easy remote access? | Yes                    | Yes      |
| Network                                  | auto_allocated_network | Yes      |
| Public IP Address                        | Automatic              | Yes      |
| Boot Script (see below)                  | used default           | Yes      |

Press the **Create** button to create the instance. The Exosphere GUI will say "Building" in lemon yellow for about 5 minutes, then "running Setup" for another minute, then "Ready" in green. Clicking on "Instances" will take you to a screen that shows the **MOLE-2026-base** instance and its **IP address** (149.165.150.186).

You can now log into the instance as **exouser**.

    $ ssh exouser@149.165.150.186
    
### Default boot script

For reference, here is the default boot script used to create MOLE-2026-base. Note: when creating MOLE-2026-base, do not change the default boot script! We will add some things to the default boot script when cloning MOLE-2026-base to create participant and faculty VMs, but **the master VM should be set up using the default boot script**.

~~~~~~
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Type: multipart/mixed; boundary="=================exosphere-user-data===="
Number-Attachments: 4

--=================exosphere-user-data====
Content-Transfer-Encoding: 7bit
Content-Type: text/cloud-boothook
Content-Disposition: attachment; filename="00-exosphere-boothook.sh"

#!/bin/bash

# Ensure this hook only runs on the first boot.
if cloud-init-per instance exosphere-setup-starting /bin/false; then
  exit 0
fi

echo on > /proc/sys/kernel/printk_devkmsg || true  # Disable console rate limiting for distros that use kmsg
sleep 1  # Ensures that console log output from any previous command completes before the following command begins
echo '{"status":"starting", "epoch": '$(date '+%s')'000}' | tee --append /dev/console > /dev/kmsg || true
chmod 640 /var/log/cloud-init-output.log


--=================exosphere-user-data====
Content-Transfer-Encoding: 7bit
Content-Type: text/x-shellscript
Content-Disposition: attachment; filename="00-exosphere-setup-running.sh"

#!/bin/bash

sleep 1  # Ensures that console log output from any previous command completes before the following command begins
echo '{"status":"running", "epoch": '$(date '+%s')'000}' | tee --append /dev/console > /dev/kmsg || true


--=================exosphere-user-data====
Content-Transfer-Encoding: 7bit
Content-Type: text/x-shellscript
Content-Disposition: attachment; filename="90-exosphere-ansible-setup.sh"

#!/bin/bash
set +e

retry() {
  local max_attempt=3
  local attempt=0
  while [ $attempt -lt $max_attempt ]; do
    if "$@"; then
      return 0
    fi
    echo "Command failed: $@"
    attempt=$((attempt + 1))
    if [ $attempt -lt $max_attempt ]; then
      sleep 5
    fi
  done
  echo "All retries of command failed: $@"
  return 1
}

(which apt-get && retry apt-get install -y python3-venv) # Install python3-venv on Debian-based platforms
(which yum     && retry yum install -y python3)      # Install python3 on RHEL-based platforms
python3 -m venv /opt/ansible-venv
. /opt/ansible-venv/bin/activate
retry pip install --upgrade pip
retry pip install ansible-core passlib
retry git clone \
  --depth=1 \
  --branch="{instance-config-mgt-repo-checkout}" \
  "{instance-config-mgt-repo-url}" \
  /opt/instance-config-mgt
ansible-playbook \
  -i /opt/instance-config-mgt/ansible/hosts \
  -e "{ansible-extra-vars}" \
  /opt/instance-config-mgt/ansible/playbook.yml
ANSIBLE_RETURN_CODE=$?
if [ $ANSIBLE_RETURN_CODE -eq 0 ]; then STATUS="complete"; else STATUS="error"; fi
sleep 1  # Ensures that console log output from any previous commands complete before the following command begins
echo '{"status":"'$STATUS'", "epoch": '$(date '+%s')'000}' | tee --append /dev/console > /dev/kmsg || true


--=================exosphere-user-data====
Content-Transfer-Encoding: 7bit
Content-Type: text/cloud-config
Content-Disposition: attachment; filename="exosphere.yml"

#cloud-config

users:
  - default
  - name: exouser
    shell: /bin/bash
    groups: sudo, admin
    sudo: ['ALL=(ALL) NOPASSWD:ALL']{ssh-authorized-keys}
ssh_pwauth: true
package_update: true
package_upgrade: {install-os-updates}
packages:
  - git


--=================exosphere-user-data====--
~~~~~~

### Setting up the new instance

The newly created MOLE-2026-base needs to be provisioned with the software and data files used during the workshop.

First create a _TARs_ folder in which to store downloaded tar files and a _clones_ folder for git working directories.

    cd
    mkdir TARs
    mkdir clones
    
If disk space gets tight, you can delete these directories.

### Finding basic information

I like to record some basic information (just for the record), such as the date that the master instance was created and information about the processor. 

Get current date:

    $ TZ="EST5EDT" date
    Fri May  9 06:47:59 EDT 2026
    
Get OS release:

    $ cat /etc/os-release
    PRETTY_NAME="Ubuntu 24.04.2 LTS"
    NAME="Ubuntu"
    VERSION_ID="24.04"
    VERSION="24.04.2 LTS (Noble Numbat)"
    VERSION_CODENAME=noble
    ID=ubuntu
    ID_LIKE=debian
    HOME_URL="https://www.ubuntu.com/"
    SUPPORT_URL="https://help.ubuntu.com/"
    BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
    PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
    UBUNTU_CODENAME=noble
    LOGO=ubuntu-logo

Find processor info:

    $ more /proc/cpuinfo
    processor	: 0
    vendor_id	: AuthenticAMD
    cpu family	: 25
    model		: 1
    model name	: AMD EPYC-Milan Processor
    stepping	: 1
    microcode	: 0x1000065
    cpu MHz		: 1996.249
    cache size	: 512 KB
    physical id	: 0
    siblings	: 1
    core id		: 0
    cpu cores	: 1
    apicid		: 0
    initial apicid	: 0
    fpu		: yes
    fpu_exception	: yes
    cpuid level	: 13
    wp		: yes
    flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 syscall nx mmxext fxsr_opt pdpe1gb rdtscp lm rep_good nopl xtopology cpuid extd_apic
    id tsc_known_freq pni pclmulqdq ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand hypervisor lahf_lm cmp_legacy svm cr8_legacy abm sse4a misalignsse 3d
    nowprefetch osvw topoext perfctr_core ssbd ibrs ibpb stibp vmmcall fsgsbase tsc_adjust bmi1 avx2 smep bmi2 invpcid rdseed adx smap clflushopt clwb sha_ni xsaveopt xsavec xgetbv1 xsaves clzero xsaveerp
    tr wbnoinvd arat npt lbrv nrip_save tsc_scale vmcb_clean flushbyasid pausefilter pfthreshold v_vmsave_vmload vgif umip pku ospke vaes vpclmulqdq rdpid arch_capabilities
    bugs		: sysret_ss_attrs spectre_v1 spectre_v2 spec_store_bypass srso ibpb_no_ret
    bogomips	: 3992.49
    TLB size	: 1024 4K pages
    clflush size	: 64
    cache_alignment	: 64
    address sizes	: 40 bits physical, 48 bits virtual
    power management:
    
    processor	: 1
    vendor_id	: AuthenticAMD
    cpu family	: 25
    model		: 1
    model name	: AMD EPYC-Milan Processor
    stepping	: 1
    microcode	: 0x1000065
    cpu MHz		: 1996.249
    cache size	: 512 KB
    physical id	: 1
    siblings	: 1
    core id		: 0
    cpu cores	: 1
    apicid		: 1
    initial apicid	: 1
    fpu		: yes
    fpu_exception	: yes
    cpuid level	: 13
    wp		: yes
    flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 syscall nx mmxext fxsr_opt pdpe1gb rdtscp lm rep_good nopl xtopology cpuid extd_apic
    id tsc_known_freq pni pclmulqdq ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand hypervisor lahf_lm cmp_legacy svm cr8_legacy abm sse4a misalignsse 3d
    nowprefetch osvw topoext perfctr_core ssbd ibrs ibpb stibp vmmcall fsgsbase tsc_adjust bmi1 avx2 smep bmi2 invpcid rdseed adx smap clflushopt clwb sha_ni xsaveopt xsavec xgetbv1 xsaves clzero xsaveerp
    tr wbnoinvd arat npt lbrv nrip_save tsc_scale vmcb_clean flushbyasid pausefilter pfthreshold v_vmsave_vmload vgif umip pku ospke vaes vpclmulqdq rdpid arch_capabilities
    bugs		: sysret_ss_attrs spectre_v1 spectre_v2 spec_store_bypass srso ibpb_no_ret
    bogomips	: 3992.49
    TLB size	: 1024 4K pages
    clflush size	: 64
    cache_alignment	: 64
    address sizes	: 40 bits physical, 48 bits virtual
    power management:
    
Find 32 vs 64 bit and processor architecture:

    $ uname -m
    x86_64    
    
Find installed packages (this list is too long to include here, but it is useful to know how to find what's installed):

    $ sudo dpkg -l
    
To remove a package (note: I didn't use this feature, but thought it good to keep the instructions):

    $ sudo dpkg -r packagename # remove package itself
    $ sudo dpkg -P packagename # purge files associated with package

### Update operating system before doing any work  

    $ sudo apt-add-repository universe
    $ sudo apt update
    $ sudo apt upgrade -y

Last updated 2025-10-16.

### Install apt-file

This allows us to find out what files are installed by a package using "apt-file list packagename"

    $ sudo apt install -y apt-file

This may pop up a graphical interface: use tab and arrow keys to navigate. May need to reboot, which can be done from the Exosphere interface.

Last updated 2025-10-16.

### Install net-tools

Provides ifconfig command.

    $ sudo apt install net-tools

Last updated 2025-10-16.

### Install whois

This enables use of the mkpasswd command used to create the hashed password used in the cloud-init script.

    $ sudo apt install -y whois

Last updated 2025-10-16.

### Install mlocate

Note: this didn't work!
{:.pozor}

This provides the locate command, useful for finding where libraries and other system files are installed.

    $ sudo apt install -y mlocate

Last updated 2025-10-16.

### Install unzip

Not really necessary, already installed.

    $ sudo apt install -y unzip

Last updated 2025-10-16.

### Install [R](https://www.r-project.org)

R is needed in order to precompile PhyloPlots.

    $ sudo apt-get install -y r-base

Last updated 2025-10-16.

### Install zlib

Needed for migrate-n. Not really necessary, already installed.

    $ sudo apt install -y zlib1g-dev

Last updated 2025-10-16.

### Install openmpi

Needed for migrate-n-mpi. 

    $ sudo apt-get install -y openmpi-bin 
    $ sudo apt-get install -y libopenmpi-dev
    $ sudo apt-get install -y openmpi-common

Last updated 2025-10-16.

### Install [migrate-n](https://peterbeerli.com/migrate-html5/index.html)

Migrate has its own lab in the workshop. Version 5.0.6 installed.

    $ cd
    $ curl -LO https://peterbeerli.com/migrate-html5/download_version4/migrate-newest.src.tar.gz
    $ tar xvf migrate-newest.src.tar.gz 
    $ mv migrate-newest.src.tar.gz TARs
    $ cd migrate-5.0.6/src
    $ ./configure
    $ make
    $ sudo make install
    $ make clean
    $ make mpis
    $ sudo make installmpi

Installed as _/usr/local/bin/migrate-n_ and _/usr/local/bin/migrate-n-mpi_:

    $ ls /usr/local/bin
    migrate-n  migrate-n-mpi

Last updated 2025-10-16.

### Install [Julia](https://julialang.org)

Julia is needed for Claudia's PhyloNetworks tutorial.

From [Julia downloads](https://julialang.org/downloads/) web site, select the Generic Linux and x86 64-bit (glibc) version.

    $ cd
    $ curl -LO https://julialang-s3.julialang.org/bin/linux/x64/1.12/julia-1.12.0-linux-x86_64.tar.gz
    $ tar zxvf julia-1.12.0-linux-x86_64.tar.gz
    $ mv julia-1.12.0-linux-x86_64.tar.gz TARs
    $ sudo mv julia-1.12.0 /opt/
    $ cd /usr/local/bin
    $ sudo ln -s /opt/julia-1.12.0/bin/julia julia

This places the julia directory in _/opt_ and creates a symbolic link to the executable in _/usr/local/bin_.

Last updated 2025-10-16.

### Install Julia packages needed by the [PhyloNetworks tutorial](https://github.com/crsl4/PhyloNetworks.jl/wiki)

This follows the [instructions](https://github.com/crsl4/PhyloNetworks.jl/wiki) on the PhyloNetworks site. Also see [instructions in this post](https://stackoverflow.com/questions/32338701/install-just-one-package-globally-on-julia) and [this post](https://stackoverflow.com/questions/61273734/setting-up-a-centralized-julia-library-repository) on installing Julia packages globally. In particular, defining the JULIA_DEPOT_PATH environmental variable specifies the location where Julia packages will be installed.

    $ cd
    $ export JULIA_DEPOT_PATH=/opt/julia-1.12.0/usr/share/julia/site
    $ julia
    julia> using Pkg                # to use functions that manage packages
    julia> Pkg.add("PhyloNetworks") # to download/install PhyloNetworks
    julia> Pkg.add("PhyloPlots")    # to download/install PhyloPlots
    julia> Pkg.add("SNaQ")          # to download/install SNaQ
    julia> Pkg.add("RCall")         # package to call R from within julia
    julia> Pkg.add("CSV")           # to read from / write to text files, e.g. csv files
    julia> Pkg.add("DataFrames")    # to create & manipulate data frames
    julia> Pkg.add("StatsModels")   # for regression formulas
    julia> using PhyloNetworks      # check whether it loads
    julia> using PhyloPlots         # check whether it loads
    julia> Pkg.status()             # useful for seeing what packages are installed
        [336ed68f] CSV v0.10.15
        [a93c6f00] DataFrames v1.7.0
        [33ad39ac] PhyloNetworks v1.0.0
        [c0d5b6db] PhyloPlots v2.0.1
        [6f49c342] RCall v0.14.8
        [3eaba693] StatsModels v0.7.4
    julia> pathof(PhyloNetworks)    # useful for seeing where the package was installed
        "/opt/julia-1.12.0/usr/share/julia/site/packages/PhyloNetworks/7zhDI/src/PhyloNetworks.j"    

Use Ctrl-d to quit julia.

Last updated 2025-10-16.

### Install [Boost C++](https://www.boost.org)

Needed in order to build RevBayes and BUCKy.

    $ cd
    $ sudo apt install -y libboost-all-dev

Last updated 2025-10-16.

### Install [RevBayes](https://revbayes.github.io/download)

Downloaded v1.3.0 Linux executable from the [RevBayes Releases web page](https://github.com/revbayes/revbayes/releases) and installed as follows:

    $ cd
    $ curl -LO https://github.com/revbayes/revbayes/releases/download/v1.3.1/revbayes-v1.3.1-linux64.tar.gz
    $ tar zxvf revbayes-v1.3.1-linux64.tar.gz
    $ cd revbayes-v1.3.1/bin
    $ sudo mv rb /usr/local/bin

Last updated 2025-10-16.

### Install [MrBayes](https://nbisweden.github.io/MrBayes/)

MrBayes is used in the SNaQ tutorial. These instructions install the binary in _/usr/local/bin_. 

Note: do not run autoconf as this will create errors in the configure script!

    $ cd
    $ curl -LO https://github.com/NBISweden/MrBayes/archive/v3.2.7a.tar.gz
    $ tar zxvf v3.2.7a.tar.gz
    $ mv v3.2.7a.tar.gz TARs
    $ cd MrBayes-3.2.7a/ 
    $ ./configure
    $ make
    $ sudo make install

Installed as _/usr/local/bin/mb_. 
Last updated 2025-10-16.

### Install [BUCKy](http://pages.stat.wisc.edu/~ane/bucky/index.html)

BUCKy is used in the SNaQ tutorial. These instructions install the binary in _/usr/local/bin_.

    $ cd
    $ curl -LO http://www.stat.wisc.edu/~ane/bucky/v1.4/bucky-1.4.4.tgz
    $ tar zxvf bucky-1.4.4.tgz
    $ mv bucky-1.4.4.tgz TARs
    $ cd bucky-1.4.4/src

Note: in order to get BUCKy to compile, I had to qualify `unordered_map` as `boost::unordered_map` in two lines (line 163 and 357) in _TGM.h_ because an `unordered_map` template is defined in both _./boost/unordered/unordered_map_fwd.hpp_ and _/usr/include/c++/11/bits/unordered_map.h_. Once you have edited _TGM.h_, you can issue the commands below to build and install.

    $ make
    $ sudo mv bucky /usr/local/bin
    $ sudo mv mbsum /usr/local/bin

Last updated 2025-10-16.

### Install [RAxML](https://github.com/stamatak/standard-RAxML)

RAxML is used in both Claudia's SNaQ and Emily Jane's gene tree updating tutorials. These instructions install the binary in _/usr/local/bin_. Note: it is easier to just use "sudo apt-get install raxml" to do this install, but I didn't realize this at the time.

    $ cd ~/clones
    $ git clone https://github.com/stamatak/standard-RAxML.git
    $ cd standard-RAxML
    $ make -f Makefile.AVX.PTHREADS.gcc
    $ sudo mv raxmlHPC-PTHREADS-AVX /usr/local/bin/raxmlHPC
    $ rm *.o  # no make clean available

Installed as _/usr/local/bin/raxmlHPC_.
Last updated 2025-10-16.

### Install [Java](https://www.java.com/en/)

The Java Runtime Environment is needed for ASTRAL and jModelTest.

    $ cd
    $ sudo apt install default-jre  # not really necessary, already installed

Last updated 2025-10-16.

### Install [ASTRAL](https://github.com/smirarab/ASTRAL)

ASTRAL is used in the SNaQ tutorial. These instructions install the binary in _/opt/astral_. Note that the _/opt/astral/astral.5.7.3.jar_ jar file and the _/opt/astral/lib_ directory need to be owned by an ordinary user, otherwise the jar must be executed as root.

    $ cd
    $ curl -LO https://github.com/smirarab/ASTRAL/archive/refs/tags/v5.7.1.tar.gz
    $ tar zxvf v5.7.1.tar.gz
    $ mv v5.7.1.tar.gz TARs
    $ sudo mkdir /opt/astral
    $ cd ASTRAL-5.7.1
    $ unzip Astral.5.7.1.zip
    $ cd Astral
    $ sudo cp astral.5.7.1.jar /opt/astral
    $ sudo cp -r lib /opt/astral

You should now be able to start ASTRAL as follows:

    $ sudo java -jar /opt/astral/astral.5.7.1.jar
    
An alias will be created by the [cloud init script](#boot-script-used) to make this easier. You do not need to set this up now; the following line is just informational.

    alias astral="java -jar /opt/astral/astral.5.7.1.jar"
    
The [cloud init script](#boot-script-used) will also change ownership to moleuser (also informational, no need to do anything now):

    sudo chown moleuser.moleuser /opt/astral/astral.5.7.1.jar
    sudo chown moleuser.moleuser /opt/astral/lib -R
    
Last updated 2025-10-16.

### Create MOLE directory

This directory will be used to store example data needed by students for tutorials.

    $ cd
    $ sudo mkdir /usr/local/share/examples/mole

Last updated 2025-10-16.

### Install data for [PhyloNetworks](http://crsl4.github.io/PhyloNetworks.jl/latest/) tutorial

    $ cd ~/clones
    $ git clone https://github.com/JuliaPhylo/PhyloUtilities.git
    $ cd PhyloUtilities
    $ sudo mkdir /usr/local/share/examples/mole/phylo-networks
    $ sudo cp -R data_results /usr/local/share/examples/mole/phylo-networks
    $ sudo cp -R scripts /usr/local/share/examples/mole/phylo-networks

Modify line 46 of /usr/local/share/examples/mole/phylo-networks/scripts/raxml.pl to say:

    my $raxml = '/usr/local/bin/raxmlHPC'; # executable

Modify line 47 of /usr/local/share/examples/mole/phylo-networks/scripts/raxml.pl to say:

    my $astral = '/opt/astral/astral.5.7.1.jar'; # adapt to your system

Last updated 2025-10-16.

### Download and install various datasets used in tutorials

The repository [github.com/molevolworkshop/moledata](https://github.com/molevolworkshop/moledata) stores many data sets used in the workshop.

Note: if any of these tutorials are changed during the workshop, be sure to package up the new version and replace the version in the moledata git repository.

    $ cd ~/clones
    $ git clone https://github.com/molevolworkshop/moledata.git
    $ cd moledata
    $ sudo unzip MSAlab.zip -d /usr/local/share/examples/mole           # alignment tutorial
    $ sudo unzip migrate_tutorial.zip -d /usr/local/share/examples/mole   # migrate tutorial
    $ sudo unzip modsel_sim_tutorial.zip -d /usr/local/share/examples/mole # Model Selection/Simulation tutorial
    $ sudo unzip svdquartets_tutorial.zip -d /usr/local/share/examples/mole # SVDQuartets tutorial
    $ sudo unzip PamlLab.zip -d /usr/local/share/examples/mole # PAML lab
    $ sudo unzip iqtreelab.zip -d /usr/local/share/examples/mole # IQ-TREE lab
    $ sudo unzip revbayes.zip -d /usr/local/share/examples/mole # RevBayes tutorial
    $ sudo unzip machinelearning.zip -d /usr/local/share/examples/mole # machine learning tutorial

Last updated 2026-05-10 (replaced machinelearning.zip with new files).

### Install data files for the phylogenomics lab

These files are used in the McTavish tree updating and tree comparison labs. These labs depend on opentree and RAxML. Note that the git repository cloned here may not actually be needed: the tutorial will be accessed by participants via the [Phylogenomics tutorial web site](https://github.com/snacktavish/Mole2023), which has participants clone from the same git repostory. The setup below just provides a backup of these files on the virtual machines themselves.

    cd ~/clones
    git clone  https://github.com/snacktavish/TreeUpdatingComparison.git
    sudo cp -R TreeUpdatingComparison /usr/local/share/examples/mole/

Last updated 2025-10-16.

### Set permissions and remove mac-specific dir

    cd /usr/local/share/examples/mole
    sudo rm -rf __MACOSX
    sudo chmod 755 modsel_sim_tutorial

Last updated 2025-05-09.

### Install [MAFFT](https://mafft.cbrc.jp/alignment/software/)

    cd
    curl -LO https://mafft.cbrc.jp/alignment/software/mafft-7.525-with-extensions-src.tgz    
    tar zxvf mafft-7.525-with-extensions-src.tgz
    mv mafft-7.525-with-extensions-src.tgz TARs
    cd mafft-7.525-with-extensions/core
    make
    sudo make install

Installed into _/usr/local/bin/_. 
Last updated 2025-10-16.

### Install [MUSCLE](https://www.drive5.com/muscle/)

MUSCLE is used in the alignment lab as well as the McTavish gene tree updating lab. 

    sudo apt install -y muscle

Last updated 2025-10-16.

### Install seqtk

seqtk is used in the McTavish gene tree updating lab.

    sudo apt install -y seqtk 

Last updated 2025-10-16.

### Install samtools

samtools is used in the McTavish gene tree updating lab.

    sudo apt install -y samtools 

Last updated 2025-10-16.

### Install bcftools

bcftools is used in the McTavish gene tree updating lab.

    sudo apt install -y bcftools

Last updated 2025-10-16.

### Install fastx

The fastx toolkit is used in McTavish gene tree updating lab. fastx toolkit and bwa-mem are not available through apt.

{% comment %}
Note: I couldn't access the hannonlab web site so this year I retrieved the _fastx_toolkit_0.0.13_binaries_Linux_2.6_amd64.tar.bz2_ file from MOLE-2024-base.

Here is what I did last year (hopefully hannonlab web site will be back up next time):
{% endcomment %}

    cd
    curl -LO http://hannonlab.cshl.edu/fastx_toolkit/fastx_toolkit_0.0.13_binaries_Linux_2.6_amd64.tar.bz2
    tar -xjf fastx_toolkit_0.0.13_binaries_Linux_2.6_amd64.tar.bz2
    mv fastx_toolkit_0.0.13_binaries_Linux_2.6_amd64.tar.bz2 TARs
    sudo mv bin/* /usr/local/bin/
    rm -rf bin

{% comment %}
There is a github version, but it looks like it has been modifed by people who are not the original authors and may behave differently: [lianos github repository](https://github.com/lianos/fastx-toolkit). Here is what they say in their _README.md_ file

    Tweaks to the FASTX-Toolkit.
    
    One (useful) tweak is the (default) disabling of quality-score checks
    in parsing/manipulating/writing fastq files. The default fastx behavior
    can be turned back on by adding the `-S` switch to the command.

    FASTX-Toolkit version 0.13 and libgtextutils version 0.6 were used as the base.
{% endcomment %}

Installed the following executables (version 0.0.13) in _/usr/local/bin_:

    fasta_clipping_histogram.pl
    fasta_formatter
    fasta_nucleotide_changer
    fastq_masker
    fastq_quality_boxplot_graph.sh
    fastq_quality_converter
    fastq_quality_filter
    fastq_quality_trimmer
    fastq_to_fasta
    fastx_artifacts_filter
    fastx_barcode_splitter.pl
    fastx_clipper
    fastx_collapser
    fastx_nucleotide_distribution_graph.sh
    fastx_nucleotide_distribution_line_graph.sh
    fastx_quality_stats
    fastx_renamer
    fastx_reverse_complement
    fastx_trimmer
    fastx_uncollapser

Last updated 2025-10-16.

### Install bwa-mem2

bwa-mem2 is used in McTavish gene tree updating lab.

    cd ~/clones
    git clone --recursive https://github.com/bwa-mem2/bwa-mem2
    cd bwa-mem2
    make
    sudo mv ./bwa-mem2* /usr/local/bin/
    rm ./src/*.o

This installs the following binaries in _/usr/local/bin/_:

    bwa-mem2
    bwa-mem2.avx
    bwa-mem2.avx2
    bwa-mem2.avx512bw
    bwa-mem2.sse41
    bwa-mem2.sse42

Last updated 2025-10-16.

### Install [TREE-QMC](https://github.com/molloy-lab/TREE-QMC)

    git clone https://github.com/molloy-lab/TREE-QMC
    cd TREE-QMC/external/MQLib
    make
    cd ../../ && mkdir -p build && cd build
    g++ -std=c++11 -O2 \
        -I ../external/MQLib/include \
        -I ../external/toms743 \
        -o tree-qmc \
        ../src/*.cpp \
        ../external/toms743/toms743.cpp \
        ../external/MQLib/bin/MQLib.a \
        -lm \
        -DVERSION=\"$(cat ../version.txt)\"
    sudo mv tree-qmc /usr/local/bin

### Install [maxcut](https://sagi-snir.wixsite.com/snir-lab/maxcut)

Note: this was installed but has now been superceded by TREE-QMC

Sagi Snir's maxcut is used in the SNaQ tutorial. These instructions install the binary in _/usr/local/bin_.
The software (v. 2.1) is no longer available from [here](http://research.haifa.ac.il/~ssagi/software/QMCN.tar.gz). Sagi suggested we use version 3.0 from [this dryad repository](https://datadryad.org/stash/dataset/doi:10.5061/dryad.r9k57). While that may work, the SNaQ tutorial has not been tested with this version of MaxCut, so this year we are using an archived copy of the `QMCN.tar.gz` file that I scp'd onto the virtual machine.

    # caution! QMCN.tar.gz does not create its own directory, so create a directory for it before unpacking
    cd
    mkdir QMCN
    cp ./TARs/QMCN.tar.gz QMCN
    cd QMCN
    tar zxvf QMCN.tar.gz
    mv QMCN.tar.gz ../TARs
    sudo cp find-cut-Linux-64 /usr/local/bin 

Installed as _/usr/local/bin/find-cut-Linux-64_. 
Last updated 2025-10-16.

### Install [IQ-TREE](http://www.iqtree.org)

Used for the IQ-TREE tutorial.

    cd
    # Install 64-bit Linux Intel version 2.3.2
    curl -LO https://github.com/iqtree/iqtree3/releases/download/v3.0.1/iqtree-3.0.1-Linux-intel.tar.gz
    tar zxvf iqtree-3.0.1-Linux-intel.tar.gz
    mv iqtree-3.0.1-Linux-intel.tar.gz TARs
    sudo mv iqtree-3.0.1-Linux-intel/bin/iqtree3 /usr/local/bin

Last updated 2025-10-16.

{% comment %}
### Install [libpython2.7.so.1.0 shared library](https://askubuntu.com/questions/1213461/cant-locate-libpython2-7-so-1-0)

The file _libpython2.7.so.1.0_ is required for PAUP*. 

    sudo apt install -y libpython2.7

Note: had to postpone install because of the following message:
"E: Unable to locate package libpython2.7
E: Couldn't find any package by glob 'libpython2.7'"

Last updated 2025-05-09.
{% endcomment %}

### Install [jModelTest](https://github.com/ddarriba/jmodeltest2/)

Used in the PAUP tutorial.

    cd
    curl -LO https://github.com/ddarriba/jmodeltest2/files/157117/jmodeltest-2.1.10.tar.gz
    tar zxvf jmodeltest-2.1.10.tar.gz
    mv jmodeltest-2.1.10.tar.gz TARs
    sudo cp -r jmodeltest-2.1.10 /opt

You should now be able to start jModelTest as follows, 
    
    sudo java -jar /opt/jmodeltest-2.1.10/jModelTest.jar    
    
but it will spit out the error message:    

    ERROR: You are trying to run a GUI interface in a headless server.

An alias will be created by the [cloud init script](#boot-script-used) to make this easier.
    alias jmodeltest="java -jar /opt/jmodeltest-2.1.10/jModelTest.jar"
The [cloud init script](#boot-script-used) will also change ownership
    sudo chown -R moleuser.moleuser /opt/jmodeltest-2.1.10
Last updated 2025-10-16.

### Install [PAUP*](http://phylosolutions.com/paup-test/)

    cd
    curl -LO https://phylosolutions.com/paup-test/paup4a169_ubuntu64.gz
    cp paup4a169_ubuntu64.gz TARs
    gunzip paup4a169_ubuntu64.gz
    sudo mv paup4a169_ubuntu64 /usr/local/bin/paup
    sudo chmod +x /usr/local/bin/paup

Installed as _/usr/local/bin/paup_. 
Last updated 2025-10-16.

### Install [PAML](http://abacus.gene.ucl.ac.uk/software/paml.html)

    cd
    curl -LO https://github.com/abacus-gene/paml/releases/download/v4.10.9/paml-4.10.9-linux-x86_64.tar.gz
    tar zxvf paml-4.10.9-linux-x86_64.tar.gz
    mv paml-4.10.9-linux-x86_64.tar.gz TARs
    cd paml-4.10.9-linux-x86_64/src
    make -f Makefile
    sudo mv baseml basemlg chi2 codeml evolver infinitesites mcmctree pamp yn00 /usr/local/bin

Installed baseml, basemlg, chi2, codeml, evolver, infinitesites, mcmctree, pamp, and yn00in _/usr/local/bin_. 
Last updated 2025-10-16.

{% comment %}
No longer using these sections because the python environment is created on the attached volume instead and used for both the machine learning and opentree labs.

### Create pyenv python virtual environment

Python modules used in the McTavish tree comparison tutorial are installed into a virtual environment named pyenv. This may not be used because the tutorial specifies for the students to install python modules themselves (which will be installed in _~/.local_), but it is installed if we end up needing it.

    sudo chown -R exouser:exouser /usr/local/share/examples/mole/TreeUpdatingComparison
    cd /usr/local/share/examples/mole/TreeUpdatingComparison
    python3 -m venv pyenv

Last updated 2025-10-30.

### Install DendroPy ([DendroPy](https://dendropy.org/downloading.html))

DendroPy is used in the McTavish gene tree updating lab.

    # activate the python environment pyenv
    cd
    source /usr/local/share/examples/mole/TreeUpdatingComparison/pyenv/bin/activate
    python3 -m pip install git+https://github.com/jeetsukumaran/DendroPy.git
    python3 -m pip list
    deactivate

Last updated 2025-10-30.

### Install opentree

opentree is used in the McTavish gene tree updating lab.

    # activate the python environment pyenv
    cd
    source /usr/local/share/examples/mole/TreeUpdatingComparison/pyenv/bin/activate
    python3 -m pip install opentree
    python3 -m pip list
    deactivate

Last updated 2025-10-30.
{% endcomment %}

### Creating a shared read-only volume for the python virtual environment

The python virtual environment used in the machine learning tutorial is large (1.8GB) and thus locating it on each VM uses up most of the remaining disk space on the VM. It is thus necessary to create a **volume** to hold just the python virtual environment that is used for both the machine learning and opentree labs. This volume is attached to MOLE-2026-base and shared with all other VMs via NFS.

#### Creating and populating a volume

In Exosphere, choose **Create > Volume** using the red **Create** button at the top right. Attach the volume to MOLE-2026-base using the **Attach Volume** button under the Volumes panel when viewing the details of the MOLE-2026-base instance. Mount the volume at _/media/volume/MOLE-data-2026_.

Assuming you are logged into MOLE-2026-base as exouser, create a python virtual environment as follows:

    module list                                                               # ensure anaconda is not loaded
    cd /media/volume/MOLE-data-2026
    python3 -m venv pyenv                                                     # create python virtual environment
    source ./pyenv/bin/activate                                               # activate the python virtual environment
    python3 -m pip install msprime==1.3.3                                     # for machine learning lab
    python3 -m pip install matplotlib==3.9.2                                  # for machine learning lab
    python3 -m pip install numpy==2.0.2                                       # for machine learning lab
    python3 -m pip install scikit-learn==1.7.2                                # for machine learning lab
    #python3 -m pip install scipy==1.17.1 # not really needed; already installed by scikit-learn
    python3 -m pip install tensorflow==2.18.0                                 # for machine learning lab
    python3 -m pip install keras==3.14.0  # not really needed; already installed by tensorflow
    python3 -m pip install ipykernel                                          # for machine learning lab
    python3 -m pip install opentree                                           # for opentree lab
    python3 -m pip install git+https://github.com/jeetsukumaran/DendroPy.git  # for opentree lab
    deactivate

While pyenv is activated, calling

    python3 -m pip freeze > mlmodules.txt
    
will save the versions of all modules currently loaded to a file. If you need to recreate the environment later, you can install all of these at once using (again, while pyenv is activated)

    python3 -m pip install -r mlmodules.txt
    
You can use 

    python3 -m pip list
    
to list modules installed in the virtual environment.

While still logged into MOLE-2026-base, create the directory _/var/pyenv_. This directory will serve as the mount point for each cloned VM.

    mkdir /var/pyenv

Last updated 2026-05-11.

#### Setting up the NFS server on MOLE-2026-base

Install nfs-kernel-server and nfs-common on MOLE-2026-base:

    sudo apt install -y nfs-kernel-server   # needed for running the NFS server on MOLE-2026-base
    sudo apt install -y nfs-common          # needed for running NFS clients on the VMs cloned from MOLE-2026-base
    
**Note:** I received error messages related to nvidia libraries when trying to install nsf-common. Because we are not using GPUs, I solved the problem by simply removing nvidia

    sudo rm /var/crash/nvidia-linux-grid-535.0.crash # to remove the crash report that causes problems
    sudo apt remove --purge nvidia-*                 # to remove nvidia
    sudo apt autoremove                              # removes files no longer referenced by any installed package
    
See the section [Setting up the NFS clients on each VM](#setting-up-the-nfs-clients-on-each-VM) below for how to establish NFS connections between the server running on MOLE-2026-base and each VM.
    
See [this explanation](https://bluexp.netapp.com/blog/azure-anf-blg-linux-nfs-server-how-to-set-up-server-and-client#H_H9) for basic NFS setup and [this one](https://www.digitalocean.com/community/tutorials/understanding-ip-addresses-subnets-and-cidr-notation-for-networking) for an explanation of specifying IP ranges.

Last updated 2026-05-11.

{% comment %}
#### Setting up the NFS client

Assuming 149.165.172.151 is the ip address of MOLE-2026-base:
~~~~~~
sudo mkdir /var/pyenv
sudo chown moleuser:moleuser /var/pyenv
sudo mount -t nfs 149.165.150.186:/media/volume/MOLE-data-2026/pyenv /var/pyenv
# use the following command to unmount
# sudo umount /var/pyenv  # can also use -f (force) and/or -l (lazy) switches
~~~~~~

(Not sure the following is necessary or desirable or even correct!) The above mount command sets up NFS sharing temporarily. To automate this so that the share is mounted on startup:
~~~~~~
sudo vi /etc/fstab
# Insert line similar to the following
# 149.165.150.186:/media/volume/MOLE-data-2026/pyenv /var/pyenv nfs defaults 0 0
sudo mount /var/pyenv
sudo mount 149.165.150.186:/media/volume/MOLE-data-2026/pyenv
~~~~~~
{% endcomment %}

## Locking an instance

It is wise to lock the _MOLE-2026-base_ instance as soon as you are finished setting it up. To do this, choose **Lock** from the **Actions** menu when you are viewing the details of the _MOLE-2026-base_ instance. Locking prevents you from doing something stupid, like deleting this virtual machine accidentally. It is easy to unlock it any time you need to, but it is much harder to recreate it after accidentally deleting it! I tend to keep all instances locked unless I find there is some action that requires unlocking.

## Create MOLE 2026 snapshots

Once the **MOLE-2026-base** VM is set up and running, you can create a **snapshot** image using the Actions menu. I named the first of these snapshot images **MOLE-2026-snapshot-2025-10-30** (where the 2025-10-30 part is the date) and make additional snapshots (deleting the really old ones) as changes are made to MOLE-2026-base.

Note that MOLE-2026-snapshot-2025-10-30 will show `0 B` initially when viewed in the Images list. Not to worry; the size will be updated when the image is fully created.

## Creating instances based on MOLE-2026-snapshot-2025-10-30

To create new instances, click the red **Create** button in the upper right corner of Exosphere, then choose **Instance** and then, in the **Choose an Instance Source** section, click the **By Image** tab and hit the **Create Instance** button beside MOLE-2026-snapshot-2025-10-30 (**or the most recent snapshot**).

Choose a base name (e.g. "amphioxus"), **m3.small** as the flavor, **20 GB** root disk size (default for selected flavor), **62** for number of instances (this is 47 for participants, 4 for TAs, 1 for Course assistant, 2 for Co-directors, and 8 that can be shared amongst faculty), **no** for enable web desktop, and **Show** for Advanced Options.

Advanced Options:

| Name                                     | Value                  | Default? |
| ---------------------------------------- | ---------------------- | -------- |
| Install operating system updates?        | Yes                    | Yes      |
| Deploy Guacamole for easy remote access? | Yes                    | Yes      |
| Network                                  | auto_allocated_network | Yes      |
| Public IP Address                        | Automatic              | Yes      |
| Boot Script                              | see below              | No       |

**Important** Be sure to change `<passwd>` to a real password in the boot script (see below) before pressing the **Create** button to create the instances. 
{:.pozor}

The Exosphere GUI will say "Building" in orange, then "running Setup", then "Ready" in green. Clicking on "Instances" will take you to a screen that shows each instance created and its IP address.

You (or a student) can now log into an instance as **moleuser** with a command like this:

    ssh moleuser@149.165.159.178
    
### Boot script used

This is the default cloud-config boot script with some modifications for MOLE. 

* One modification is the addition of the user "moleuser". Note that SSH public keys for the co-directors as well as the TAs are automatically saved to the _~moleuser/.ssh/authorized_keys_ directory on each instance, making it easy for the TAs to log in to any instance, even if the student has changed the moleuser password (the moleuser password will be given to students in the first lab). 

* Another modification is the addition of 14 lines in the `runcmd` section. These lines do the following:

 1. makes moleuser the owner of everything inside _/var/pyenv_ 
 2. makes moleuser the owner of everything inside _/usr/local/share/examples/mole_ 
 3. makes moleuser the owner of everything inside _/opt/astral_ (needed for ASTRAL to be started without using sudo) 
 4. makes moleuser the owner of everything inside _/opt/jmodeltest-2.1.10_ (needed for jModelTest to be started without using `sudo`) 
 5. makes moleuser the owner of everything inside _/opt/julia-1.12.0_  
 6. creates an alias named _astral_ (makes it easier to start ASTRAL)
 7. creates an alias named _jmodeltest_ (makes it easier to start jModelTest)
 8. creates an alias named _phyml_ (which points to the phyml executable inside jModelTest)
 9. adds a line exporting the environmental variable JULIA_DEPOT_PATH to moleuser's _.bash_profile_ file (this allows Julia to find the packages needed for the PhyloNetworks tutorial)
10. creates a symlink named _iqtree-beta_ in _/usr/local/bin_ that points to _/usr/local/bin/iqtree3_ (in case the IQTREE tutorial still uses iqtree-beta rather than iqtree3)
11. creates a symlink named _raxml_ in _/usr/local/bin_ that points to _/usr/local/bin/raxmlHPC_ (the PAUP* tutorial specifies raxml rather than raxmlHPC)
12. creates a symlink named _raxmlHPC-PTHREADS-AVX_ in _/usr/local/bin_ that points to _/usr/local/bin/raxmlHPC_ (the SNaQ tutorial uses raxmlHPC-PTHREADS-AVX at some point)
13. makes moleuser the owner of its own _.bash_profile_ file (created as a result of the alias definitions above)
14. creates a symbolic link named _moledata_ (makes it easier to find example datasets)

~~~~~~
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Type: multipart/mixed; boundary="=================exosphere-user-data===="
Number-Attachments: 4

--=================exosphere-user-data====
Content-Transfer-Encoding: 7bit
Content-Type: text/cloud-boothook
Content-Disposition: attachment; filename="00-exosphere-boothook.sh"

#!/bin/bash

# Ensure this hook only runs on the first boot.
if cloud-init-per instance exosphere-setup-starting /bin/false; then
  exit 0
fi

echo on > /proc/sys/kernel/printk_devkmsg || true  # Disable console rate limiting for distros that use kmsg
sleep 1  # Ensures that console log output from any previous command completes before the following command begins
echo '{"status":"starting", "epoch": '$(date '+%s')'000}' | tee --append /dev/console > /dev/kmsg || true
chmod 640 /var/log/cloud-init-output.log


--=================exosphere-user-data====
Content-Transfer-Encoding: 7bit
Content-Type: text/x-shellscript
Content-Disposition: attachment; filename="00-exosphere-setup-running.sh"

#!/bin/bash

sleep 1  # Ensures that console log output from any previous command completes before the following command begins
echo '{"status":"running", "epoch": '$(date '+%s')'000}' | tee --append /dev/console > /dev/kmsg || true


--=================exosphere-user-data====
Content-Transfer-Encoding: 7bit
Content-Type: text/x-shellscript
Content-Disposition: attachment; filename="90-exosphere-ansible-setup.sh"

#!/bin/bash
set +e

retry() {
  local max_attempt=3
  local attempt=0
  while [ $attempt -lt $max_attempt ]; do
    if "$@"; then
      return 0
    fi
    echo "Command failed: $@"
    attempt=$((attempt + 1))
    if [ $attempt -lt $max_attempt ]; then
      sleep 5
    fi
  done
  echo "All retries of command failed: $@"
  return 1
}

(which apt-get && retry apt-get install -y python3-venv) # Install python3-venv on Debian-based platforms
(which yum     && retry yum install -y python3)      # Install python3 on RHEL-based platforms
python3 -m venv /opt/ansible-venv
. /opt/ansible-venv/bin/activate
retry pip install --upgrade pip
retry pip install ansible-core passlib
retry git clone \
  --depth=1 \
  --branch="{instance-config-mgt-repo-checkout}" \
  "{instance-config-mgt-repo-url}" \
  /opt/instance-config-mgt
ansible-playbook \
  -i /opt/instance-config-mgt/ansible/hosts \
  -e "{ansible-extra-vars}" \
  /opt/instance-config-mgt/ansible/playbook.yml
ANSIBLE_RETURN_CODE=$?
if [ $ANSIBLE_RETURN_CODE -eq 0 ]; then STATUS="complete"; else STATUS="error"; fi
sleep 1  # Ensures that console log output from any previous commands complete before the following command begins
echo '{"status":"'$STATUS'", "epoch": '$(date '+%s')'000}' | tee --append /dev/console > /dev/kmsg || true


--=================exosphere-user-data====
Content-Transfer-Encoding: 7bit
Content-Type: text/cloud-config
Content-Disposition: attachment; filename="exosphere.yml"

#cloud-config

users:
  - default
  - name: moleuser          # MOLE-specific: adds a user moleuser common to all
    passwd: <replace me with hashed password generated using "mkpasswd --method=SHA-512 --rounds=4096">
    expiredate: '2027-12-31'
    lock_passwd: false
    shell: /bin/bash 
    groups: sudo, admin    
    sudo: ALL=(ALL) NOPASSWD:ALL
    ssh_authorized_keys:    # moleuser has public keys for directors and TAs allowing easy login
        - ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKh6TEdeul5a+Q239SNR1gSQVq/WjsxDARMmTQIUTOmf plewis@cormoran.local
        - ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHaGHTJV5ixEfHmvGAsGWEuChd3odBmT+2mvn/gjkhqo jjustis@MSI
        - ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGN3kowum4t/7rwKk1oPcSuYBH68ojiRG8eMSVpMpPaU analisamilkey@MacBook-Air-5.lan
        - ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIC7lsWtZyDLX6fKOVCsuC/B1RNS9a/c6xAxUxOuFp66F thao@ARSIAAME5TQNGU1
        - ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMj4eIHXmM7xrRPF4ong/gA5nE+UrmncLLEQkcnmEsIo jembrown@bioscis-MacBook-Pro-2.local
        - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC70XJydvXPPFEui0f5XHGjTkVutUEABHXWQtNPfkgkl9r5nPShPooydGSTWci+84QLUI53OBretQ1dlrkrZvBqeT6YPwO33T7c2aQTmBpcWG4rhtieyvjfxVCXgOaJVaLqLE8k/0T34B/Ks1rTaaVJ0a8vMm4AuSkDFopKGoR9EZRJLCY5CUeJZA1byVWcQkLvrHekP0AcWlWqyT54UGhd1rWE2yijLHZIq1rhI5C8JMKU5m/q6BFHZj6TqaoAY63AiBT2l1vCG6CTz6pu5bS2edKCozoQ0JTlnodabwYQRHzsbQg6PPJ8OK1Qvezl2KeKa73jpRot+h6djD1iXfvoHOaQ2PndICWGpVm6gnLsFnjMtWN/aAdjHhp/A6veDbwo5gOw96j2LjCw+jwB80UsfMkRVqbc4pndzSKR0e+qOFOfxshr8n5JT9YJJ3uznjl58Lv487SJ4fCdeAVBSif49rRK5cToa0x3oKt50g2xvxmn2Z4mOwquUqo5UEoIttc= marmoset@Lenny
        - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDndxbOPDEMbBLJIIxOgKYGrd1FN3swhRJ+mYXj9/dE5IrB98YKWWT4+mS43mmWwlFDljRzIe9VlkwWvl2sYECefpBuNimkFwz+0V3E+FINSjSEBAgumaVhygr9L/3S6YnH4zpqWMyYPk4QOhvTYLIAC4vsLRaKHOTMRYj6JmWQi3DeX5I/utYHdOOMoGPZ1cTfFTyPbdFhPta09Umf1AfS93o73G7BanHdGSQBQajlcZlwT7ePEP/S80X5Bg/sTnli+pMojUXhdVXIQOi0nRnqxC4zqEV3zthCAqsKjvy0+GL7M3tybDIEyGnQtPCPD43RTNVgVGPrn4k1LmZtWlpoKsjXyBoO9rbZXZjWaSu7cIFm9Wcc7BXbLHiSjWFitl3S8C7Z0+iQAU0CT8ifRxGntAyYPNL+xKNHyuIwwVDaC8Z8toAkFO1RB1w6UgJmDgLhbi+saEo98HKFchDi8qED7JanXsW0ewnoguZUQLFuWMRbe7Be6lKGaea8wBhW0c8= useradmin@Users-MBP-2.lan
        - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDV/XPzswM4seTioKLp01l4yzoaxRgK1Hx0yQQpr/HlokC0hSCuACQSaA6ULMqgsoAd4S1EhI9rujdpf8N7yKKsNIrwpGSX9UL5bUsCE8xh5n500iu2YUTkBuWDgZvGPqKWwMu9L9v5AxH/bk2l4EqfbPUyzgcQRX6w5OJoz7pYvEBD8BGc5y/V3VfW3BaQARdXQqvc6Eqg5wEewsLjBrkNwc0nVQHTxIuz3MP1eRybbsB44N6JuqyVlogdy8DzSI96Za/yVPCeVcGfl44N9rOa8+/7t2AsE+ycGuTM3tOeWJBUE5FOzFbEpk3SppcwKkOwTt+nnLMcCRpovHJOmSSHdptq7HJptm49FDChX/AYQy91EObHLqOkbciueHlTRNYjeye2+rnYS83kNi3f0iYr01HeUtK85GcvCGxbEpinPEVbSUFDI9inbkYVvSkL6T5JK9NWXgDpqFvGU1fESMaaZCtXDgDuFZI0T83k/tsRLvD8woxqCSsZPIvbz/UPUwM= tracyh@Indigo.local
        - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCqJeFU3sEcA72fyYD2LCzDsfHqPmZonnATiXDKYeutIzQ+iVREIG3EMUNjeps8JS9oWw11ojXLFDZCHdg/z87qBZn7ilGgXZ6/PRhGaDx3kjPr5Mek10bV3BwB0O9Gws9rmepD/akuXY7wTS5M++YqCkwU1Ia9oAEW4QWDuc1Bdj3L1DqSYbI+xg38EA5TpRL2N968OPuu1xhGT9cPkRgOQAcTbFyknoeEXKwSUKamii8q8Lv+Zi9nA1nRYa0xZdJSGZNxso41FJkEmNfF6o/IKMtAJ0DHcg1B3aJpS8o2+cgyR+L0NqVHrJeBIagm4n3H8xP40pUCj5PyphdZam5L jpbielawski@Josephs-MacBook-Air.local
        - ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA1D6eflrh3q3daop2orqL0pXrAqOUt8AaYWaC/d+iZQutHiroByNjpSETkmEd1yw8NpF6gVkh8oNqvTH1ERlJtX1BETipUvJAlvV67ZwWDSoYVqM+RwFiUT4cIC2No0V3ETI9pd4D0Dnq/9l4V9pYaunnbvIaAUsQiDRPMcRq+aOZRB/fH9nTQ5jfWKWEAu2m77T6esXe0bFX6cMhoZdk4HQSc+Wdsfn5TZEoi7+0YVK7973ZmIHYRRl9a/80NtIIHQVOOjPve3mUxv5/dlFBvPVLVHe91XqD4DnXnjXytBgNpqjPHNY28yy/UZ7Ba8XXIxGzWEDy3p1+dJzXni/hOQ== DavidSwofford
        - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDFYUmO7HPYTDvNCjAZIkXfR/P9cCm6QzQqRRLRFH7XI8ZF6w3+jhuT3bXDvHqYCP4W0s67UfWU1C92qtMWpzVzHw2XWi67agSNNU/PgywlCoQqoybf1s5SDfgPGJ54env9Y09KtHZF64n4WI/Sja5+FSeF7Cd4xt8SkJcRIPV+EHluE08imnFvNkW1REG32x1xDJq7euezwIHUhG9Be7nXN0VQlX0UH4D6KIDg7+autni/yZzKrfX0w7vFsAja8flWUj02mTGtZU428kHThjvzH6fJ7IonM+gSN+s+MW+1xkWSQp6N4OzM79aZS5xuzup29/8vkWcO03kg8Vigctvx ejmctavish@gmail.com
  - name: exouser
    shell: /bin/bash
    groups: sudo, admin
    sudo: ['ALL=(ALL) NOPASSWD:ALL']{ssh-authorized-keys}
ssh_pwauth: true
package_update: true
package_upgrade: {install-os-updates}
packages:
  - git
runcmd:
  - chown -R moleuser:moleuser /var/pyenv                                                                     # MOLE
  - chown -R moleuser:moleuser /usr/local/share/examples/mole                                                 # MOLE
  - chown -R moleuser:moleuser /opt/astral                                                                    # MOLE
  - chown -R moleuser:moleuser /opt/jmodeltest-2.1.10                                                         # MOLE
  - chown -R moleuser:moleuser /opt/julia-1.12.0                                                              # MOLE
  - echo 'alias astral="java -jar /opt/astral/astral.5.7.1.jar"' >> /home/moleuser/.bash_profile              # MOLE
  - echo 'alias jmodeltest="java -jar /opt/jmodeltest-2.1.10/jModelTest.jar"' >> /home/moleuser/.bash_profile # MOLE
  - echo 'alias phyml="/opt/jmodeltest-2.1.10/exe/phyml/PhyML_3.0_linux64"' >> /home/moleuser/.bash_profile   # MOLE
  - echo 'export JULIA_DEPOT_PATH=/opt/julia-1.12.0/usr/share/julia/site' >> /home/moleuser/.bash_profile     # MOLE
  - sudo ln -s /usr/local/bin/iqtree3 /usr/local/bin/iqtree-beta                                              # MOLE
  - sudo ln -s /usr/local/bin/raxmlHPC /usr/local/bin/raxml                                                   # MOLE
  - sudo ln -s /usr/local/bin/raxmlHPC /usr/local/bin/raxmlHPC-PTHREADS-AVX                                   # MOLE
  - sudo chown -R moleuser.moleuser /home/moleuser/.bash_profile                                              # MOLE
  - ln -s /usr/local/share/examples/mole /home/moleuser/moledata                                              # MOLE

--=================exosphere-user-data====--
~~~~~~

### Setting up the NFS clients on each VM

You will need to mount the _/media/volume/MOLE-data-2026/pyenv_ directory on MOLE-2026-base onto the _/var/pyenv_ directory on each VM instance. This involves (each of these items has its own subsection below):
* adding a line to _/etc/exports_ on MOLE-2026-base for each VM instance (allowing that VM instance to access the share);
* restart the server on MOLE-2026-base
* add each VM to the known_hosts file on your local laptop to avoid getting asked it is OK to connect for each
* mount the folder `/var/pyenv` on each VM instance

#### Editing _/etc/exports_

Edit the exports file:

    sudo vi /etc/exports
    
Add virtual machine ip addresses to the exports file (the IP numbers shown here are those for the 7 chelydra testing VMs):
    
    /media/volume/sdb/mole 149.165.147.173(ro,sync,no_subtree_check)
    /media/volume/sdb/mole 149.165.147.87(ro,sync,no_subtree_check)
    /media/volume/sdb/mole 149.165.147.77(ro,sync,no_subtree_check)
    /media/volume/sdb/mole 149.165.169.167(ro,sync,no_subtree_check)
    /media/volume/sdb/mole 149.165.147.128(ro,sync,no_subtree_check)
    /media/volume/sdb/mole 149.165.173.221(ro,sync,no_subtree_check)
    /media/volume/sdb/mole 149.165.147.176(ro,sync,no_subtree_check)

Close the file when finished.

#### Restarting the NFS server

On MOLE-2026-base:

    sudo exportfs -a                            # causes /etc/exports file to be processed
    sudo systemctl restart nfs-kernel-server    # retarts the server

#### Adding host keys to your local _~/.ssh/known_hosts_ file

On your local laptop, issue a line like this for each participant/faculty/TA VM:

    ssh-keyscan 149.165.172.121 >> ~/.ssh/known_hosts
    
I would create a bash script to do this (be sure IPADDRESSES holds all the VM IP addresses before running):

    #!/bin/bash
    
    IPADDRESSES=(149.165.147.173 149.165.147.87 149.165.147.77 149.165.169.167 149.165.147.128 149.165.173.221 149.165.147.176)
    
    for ip in ${IPADDRESSES[@]}
    do
        ssh-keyscan $ip >> ~/.ssh/known_hosts
    done

    # Remove duplicate entries from known_hosts file
    sort -u ~/.ssh/known_hosts -o ~/.ssh/known_hosts
    
#### Mounting _/media/volume/MOLE-data-2026/pyenv_ at _/var/pyenv_ on each VM

You can use a script such as the following to mount the _/media/volume/MOLE-data-2026/pyenv_ folder on MOLE-2026-base on all VMs at once (assuming MOLE-2026-base is exporting to all of them):

    #!/bin/bash
    
    MOLEBASE="149.165.150.186"
    IPADDRESSES=(149.165.147.173 149.165.147.87 149.165.147.77 149.165.169.167 149.165.147.128 149.165.173.221 149.165.147.176)
    
    for ip in ${IPADDRESSES[@]}
    do
        ssh -t moleuser@$ip "bash -c 'sudo mount -t nfs $MOLEBASE:/media/volume/MOLE-data-2026/pyenv /var/pyenv'"
    done

For this to work:
* every VM should have a _/var/pyenv_ folder that is owned by moleuser (this should have been done when the VM was created)
* the array IPADDRESSES in this script should contain all the virtual machine IP addresses
* ensure MOLEBASE is set to the correct IP address of the MOLE-2026-base machine

{% comment %}
## Cleaning up VMs from 2024

I used the script _delete-2024-VMs.sh_ the _late-additions/2025-05-10-delete-2024-VMs_ folder to delete the VMs that were shelved at the end of the 2024 workshop. See the section [Late additions](#late-additions) below for details on how the _late-additions_ folder.
{% endcomment %}

## Command line client

### Obtaining CLI credentials

**Note:** every year I create new credentials because the old ones have expired (see expiration date in table below).

**Note:** There is now a "Download Credentials for web shell access" section of the Exosphere web site. This may allow you to avoid logging into Horizon (as described below), but I haven't tried it.

These instructions copied from the illustrated and more complete instructions at the [Setting up application credentials and openrc.sh for the Jetstream2 CLI](https://docs.jetstream-cloud.org/ui/cli/openrc/) page.

* Login to [Horizon](https://js2.jetstream-cloud.org/) using Xsede credentials, ensuring that "ACCESS CILogon" is displayed
* Be sure it says ACCESS * DEB190022 at the top dropdown box
* Choose **Identity**, then **Application Credentials** from the left sidebar menu
* Click **Create Application Credential** towards the top right
* Filled out form using entries below (but preferably make up your own name), then pressed the **Create Application Credential** button

| Field                    | Value                                                            |
| ------------------------ | ---------------------------------------------------------------- |
| Name                     | CLI-MOLE-2026-credentials                                        |
| Description              | 2026 Woods Hole Molecular Evolution Workshop at MBL              |
| Secret                   | not shown here, stored in my password manager                    |
| Expiration Date          | 07/30/2026                                                       |
| Expiration Time          | left blank                                                       |
| Roles                    | left blank  (defaults to "reader, load-balancer_member, member") |
| Access Rules             | left blank                                                       |
| Unrestricted (dangerous) | left unchecked                                                   |

Copied the password generated by my password manager into the Secret field. Note that using a password manager (e.g. 1Password) is not necessary; I used it because it makes it easy to generate a secure password.

**Important!** A dialog box will appear with three buttons at the bottom: **Download openrc file**, **Download clouds.yaml**, and **Close**. 

**Do not press the "Close" button until you have safely downloaded _both_ the _openrc_ and _clouds.yaml_ files to your local hard drive.** 
{:.pozor}

If you fail, you will have to delete the credentials you just created and start again (the consequences of failing to save both files at this stage are minor, but annoying).

The file _clouds.yaml_ was downloaded by pressing the **Download clouds.yaml** button. I placed it here on my local laptop:

    ~/.config/openstack/clouds.yaml

The file _app-cred-CLI-MOLE-2026-credentials-openrc.sh_ was downloaded by pressing the **Download openrc file** button and saved on my local hard drive. This is the file can be sourced to provide these environmental variables needed for authentication:

    OS_AUTH_TYPE
    OS_AUTH_URL
    OS_IDENTITY_API_VERSION
    OS_REGION_NAME
    OS_INTERFACE
    OS_APPLICATION_CREDENTIAL_ID
    OS_APPLICATION_CREDENTIAL_SECRET

### Using CLI

Most of these instructions come from the [Jetstream2 API tutorial](https://github.com/jlf599/JetstreamAPITutorial).

You will need to install the openstack client on your local laptop (see [installing openstack](https://pypi.org/project/python-openstackclient/)). If you are sure that you only have one version of python3 installed on your laptop, you can safely use this method (but see below for an alternative that might be safer):

    pip3 install python-openstackclient
    
I actually prefer the following method because it explicitly uses the default python3 installed on my system (this way I know that python-openstackclient is installed in the version of python3 that I actually use):

    python3 -m pip install python-openstackclient
    
You will need to source your openrc file (see last section):

    . app-cred-POL-CLI-MOLE-credential-openrc.sh
    
To show a list of flavors:

    openstack flavor list
    
To show a list of images:

    openstack image list

To show details for one particular image:

    openstack image show MOLE-2026-snapshot-2025-10-30 --fit-width

To show a list of instances:

    openstack server list
    
To show details for one particular instance, provide the ID:

    openstack server show a6e3ec6f-3e1a-42ed-a45a-3375af4146a5 --fit-width

To create and launch an instance (see [Launch and Access Your Instance](https://docs.jetstream-cloud.org/ui/cli/launch/)):

    (normally done using exosphere interface)

{% comment %}    
openstack server create <my-server-name> \
--flavor FLAVOR \
--image IMAGE-NAME \
--key-name <my-keypair-name> \
--security-group <my-security-group-name> \
--wait
{% endcomment %}    
        
To shelve or unshelve an instance (see [Instance Management Actions in the CLI](https://docs.jetstream-cloud.org/ui/cli/manage/)), get ID using `openstack server list` and then issue a command like this:

    openstack server unshelve ea2f87ea-3cce-4987-a489-e0b9850f743c
      
To delete an instance (see [Deleting items in the CLI](https://docs.jetstream-cloud.org/ui/cli/deleting/)):

    openstack server delete ea2f87ea-3cce-4987-a489-e0b9850f743c
    
{% comment %}
    1  cd .ssh
    2  ls
    3  cat - >> authorized_keys
    4  ls -la
    5  cd .ssh
    6  ls
    7  cat - > authorized_keys
    8  vi authorized_keys
    9  cat - > authorized_keys
   10  ls
   11  cat authorized_keys
   12  vi authorized_keys
   13  cd
   14  mkdir TARs
   15  mkdir clones
   16  ls
   17  TZ="EST5EDT" date
   18  more /proc/cpuinfo
   19  uname -m x86_64
   20  sudo dpkg -l
   21  !
   22  sudo apt-add-repository universe
   23  sudo apt update
   24  sudo apt upgrade -y
   25  sudo apt install -y apt-file
   26  sudo apt install -y python2
   27  ls
   28  uname -m x86_64
   29  uname --help
   30  sudo apt install -y apt-file
   31  sudo apt install -y python2
   32  sudo apt install -y python-is-python3
   33  sudo apt install -y whois
   34  whois
   35  whoami
   36  sudo apt install -y mlocate
   37  sudo apt install -y unzip
   38  sudo apt-get install -y r-base
   39  sudo apt install -y zlib1g-dev
   40  sudo apt-get install -y openmpi-bin
   41  sudo apt-get install -y libopenmpi-dev
   42  sudo apt-get install -y openmpi-common
   43  curl -LO https://peterbeerli.com/migrate-html5/download_version4/migrate-newest.src.tar.gz
   44  ls
   45  tar zxvf migrate-newest.src.tar.gz
   46  ls
   47  curl -LO https://peterbeerli.com/migrate/download_version4/migrate-5.0.6.src.tar.gz
   48  ls
   49  tar zxvf migrate-5.0.6.src.tar.gz
   50  ls
   51  rm migrate-newest.src.tar.gz
   52  tar zxvf migrate-5.0.6.src.tar.gz
   53  file migrate-5.0.6.src.tar.gz
   54  tar xvf migrate-5.0.6.src.tar.gz
   55  ls
   56  mv migrate-5.0.6.src.tar.gz TARs/
   57  ls
   58  cd migrate-5.0.6/
   59  ls
   60  cd src
   61  ./configure
   62  make
   63  sudo make install
   64  make clean
   65  make mpis
   66  sudo make installmpi
   67  ls -la /usr/local/bin/
   68  cd
   69  curl -LO https://julialang-s3.julialang.org/bin/linux/x64/1.8/julia-1.8.5-linux-x86_64.tar.gz
   70  tar zxvf julia-1.8.5-linux-x86_64.tar.gz
   71  mv julia-1.8.5-linux-x86_64.tar.gz TARs
   72  sudo mv julia-1.8.5 /opt/
   73  cd /usr/local/bin
   74  sudo ln -s /opt/julia-1.8.5/bin/julia julia
   75  cd
   76  ls
   77  cd ~/usr/local/bin
   78  cd /usr/local/bin/
   79  ls
   80  rm julia
   81  sudo rm julia
   82  cd /opt
   83  ls
   84  sudo rm -rf julia-1.8.5/
   85  cd
   86  curl -fsSL https://install.julialang.org | sh
   87  vi .bashrc
   88  vi .profile
   89  curl -LO https://julialang-s3.julialang.org/bin/linux/x64/1.10/julia-1.10.2-linux-x86_64.tar.gz
   90  ls
   91  tar zxvf julia-1.10.2-linux-x86_64.tar.gz
   92  mv julia-1.10.2-linux-x86_64.tar.gz TARs/
   93  sudo mv julia-1.10.2 /opt/
   94  cd /usr/local/bin
   95  sudo ln -s /opt/julia-1.10.2/bin/julia julia
   96  julia
   97  cd
   98  export JULIA_DEPOT_PATH=/opt/julia-1.10.2/usr/share/julia/site
   99  julia
  100  cd ~/clones/
  101  git clone https://github.com/revbayes/revbayes.git
  102  cd revbayes/projects/cmake/
  103  ./build.sh
  104  cd
  105  sudo apt install -y libboost-all-dev
  106  cd clones/
  107  cd revbayes/projects/cmake/
  108  ./build.sh
  109  sudo mv rb /usr/local/bin
  110  curl -LO https://github.com/NBISweden/MrBayes/archive/v3.2.7a.tar.gz
  111  tar zxvf v3.2.7a.tar.gz
  112  mv v3.2.7a.tar.gz TARs
  113  cd MrBayes-3.2.7a/
  114  ./configure
  115  make
  116  sudo make install
  117  cd
  118  curl -LO http://dstats.net/download/http://www.stat.wisc.edu/~ane/bucky/v1.4/bucky-1.4.4.tgz
  119  tar zxvf bucky-1.4.4.tgz
  120  mv bucky-1.4.4.tgz TARs/
  121  cd bucky-1.4.4/src/
  122  make
  123  ls
  124  make
  125  sudo mv bucky /usr/local/bin/
  126  sudo mv mbsum /usr/local/bin/
  127  cd
  128  cd clones/
  129  git clone https://github.com/stamatak/standard-RAxML.git
  130  cd standard-RAxML/
  131  make -f Makefile.AVX.PTHREADS.gcc
  132  sudo mv raxmlHPC-PTHREADS-AVX /usr/local/bin/raxmlHPC
  133  rm *.o
  134  cd
  135  sudo apt install default-jre
  136  curl -LO https://github.com/smirarab/ASTRAL/archive/refs/tags/v5.7.1.tar.gz
  137  tar zxvf v5.7.1.tar.gz
  138  mv v5.7.1.tar.gz TARs
  139  sudo mkdir /opt/astral
  140  cd ASTRAL-5.7.1
  141  unzip Astral.5.7.1.zip
  142  cd Astral/
  143  sudo cp astral.5.7.1.jar /opt/astral
  144  sudo cp -r lib /opt/astral
  145  sudo java -jar /opt/astral/astral.5.7.1.jar
  146  cd
  147  sudo mkdir /usr/local/share/mole
  148  cd clones/
  149  git clone https://github.com/crsl4/PhyloNetworks.jl.wiki.git
  150  cd PhyloNetworks.jl.wiki/
  151  sudo mkdir /usr/local/share/mole/phylo-networks
  152  sudo cp -R data_results /usr/local/share/mole/phylo-networks
  153  cd /usr/local/share/mole/phylo-networks/data_results/scripts/
  154  ls
  155  nano raxml.pl
  156  sudo nano raxml.pl
  157  nano raxml.pl
  158  cd ~/clones/
  159  git clone https://github.com/molevolworkshop/moledata.git
  160  cd moledata/
  161  sudo unzip MSAlab.zip -d /usr/local/share/mole
  162  sudo unzip migrate_tutorial.zip -d /usr/local/share/mole
  163  sudo unzip modsel_sim_tutorial.zip -d /usr/local/share/mole
  164  sudo unzip svdquartets_tutorial.zip -d /usr/local/share/mole
  165  sudo unzip PamlLab.zip -d /usr/local/share/mole
  166  sudo unzip iqtreelab.zip -d /usr/local/share/mole
  167  sudo unzip revbayes.zip -d /usr/local/share/mole
  168  cd ..
  169  git clone  https://github.com/snacktavish/Mole2023.git
  170  sudo cp -R Mole2023 /usr/local/share/mole/
  171  cd /usr/local/share/mole
  172  sudo rm -rf __MACOSX
  173  sudo chmod 755 modsel_sim_tutorial
  174  cd
  175  curl -LO https://mafft.cbrc.jp/alignment/software/mafft-7.505-with-extensions-src.tgz
  176  tar zxvf mafft-7.505-with-extensions-src.tgz
  177  mv mafft-7.505-with-extensions-src.tgz TARs
  178  cd mafft-7.505-with-extensions/core
  179  make
  180  sudo make install
  181  sudo apt install -y muscle
  182  sudo apt install -y seqtk
  183  sudo apt install -y samtools
  184  sudo apt install -y bcftools
  185  cd
  186  curl -LO http://hannonlab.cshl.edu/fastx_toolkit/fastx_toolkit_0.0.13_binaries_Linux_2.6_amd64.tar.bz2
  187  tar -xjf fastx_toolkit_0.0.13_binaries_Linux_2.6_amd64.tar.bz2
  188  mv fastx_toolkit_0.0.13_binaries_Linux_2.6_amd64.tar.bz2 TARs
  189  sudo mv bin/* /usr/local/bin/
  190  pwd
  191  ls
  192  cd bin/
  193  ls
  194  cd ..
  195  rm -rf bin
  196  ls /usr/local/bin
  197  cd clones/
  198  git clone --recursive https://github.com/bwa-mem2/bwa-mem2
  199  cd bwa-mem2/
  200  make
  201  sudo mv ./bwa-mem2* /usr/local/bin/
  202  rm ./src/*.o
  203  ls /usr/local/bin/
  204  cd
  205  curl -LO https://github.com/Cibiv/IQ-TREE/releases/download/v1.6.12/iqtree-1.6.12-Linux.tar.gz
  206  tar zxvf iqtree-1.6.12-Linux.tar.gz
  207  mv iqtree-1.6.12-Linux.tar.gz TARs
  208  sudo mv iqtree-1.6.12-Linux/bin/iqtree /usr/local/bin
  209  curl -LO https://github.com/iqtree/iqtree2/releases/download/v2.2.0/iqtree-2.2.0-Linux.tar.gz
  210  tar zxvf iqtree-2.2.0-Linux.tar.gz
  211  mv iqtree-2.2.0-Linux.tar.gz TARs
  212  sudo mv iqtree-2.2.0-Linux/bin/iqtree2 /usr/local/bin
  213  ls /usr/local/bin
  214  sudo apt install -y libpython2.7
  215  cd
  216  curl -LO https://github.com/ddarriba/jmodeltest2/files/157117/jmodeltest-2.1.10.tar.gz
  217  tar zxvf jmodeltest-2.1.10.tar.gz
  218  mv jmodeltest-2.1.10.tar.gz TARs
  219  cp -r jmodeltest-2.1.10 /opt
  220  sudo cp-r jmodeltest-2.1.10 /opt
  221  sudo cp -r jmodeltest-2.1.10 /opt
  222  sudo java -jar /opt/jmodeltest-2.1.10/jModelTest.jar
  223  ls
  224  mkdir QMCN
  225  cp wQMC.tar.gz QMCN/
  226  cd QMCN/
  227  ls
  228  tar zxvf wQMC.tar.gz
  229  rm wQMC.tar.gz
  230  ls
  231  cd
  232  ls
  233  cp wQMC.tar.gz TARs/
  234  cd QMCN/
  235  sudo cp find-cut-Linux-64 /usr/local/bin
  236  ls
  237  sudo cp max-cut-tree /usr/local/bin/
  238  max-cut-tree
  239  sudo max-cut-tree
  240  ls /usr/local/bin/
  241  cd /usr/local/bin
  242  ls -la
  243  sudo chmod +x max-cut-tree
  244  max-cut-tree
  245  pwd
  246  ./max-cut-tree
  247  ls
  248  ./max-cut-tree
  249  cd
  250  curl -LO http://phylosolutions.com/paup-test/paup4a168_ubuntu64.gz
  251  cp paup4a168_ubuntu64.gz TARs
  252  gunzip paup4a168_ubuntu64.gz
  253  sudo mv paup4a168_ubuntu64 /usr/local/bin/paup
  254  sudo chmod +x /usr/local/bin/paup
  255  curl -LO https://github.com/abacus-gene/paml/releases/download/4.10.7/paml-4.10.7-linux-X86_64.tgz
  256  ls
  257  tar zxvf paml-4.10.7-linux-X86_64.tgz
  258  ls
  259  cd paml-4.10.7/
  260  ls
  261  cd src
  262  make -f Makefile
  263  ls
  264  nano Makefile
  265  make -f Makefile
  266  sudo mv baseml basemlg chi2 codeml evolver infinitesites mcmctree pamp yn00 /usr/local/bin
  267  cd
  268  ls
  269  mv paml-4.10.7-linux-X86_64.tgz TARs/
  270  ls
  271  mv wQMC.tar.gz TARs/
  272  ls
  273  cd /usr/local/share/mole/
  274  ls
  277  sudo chown -R exouser.exouser /usr/local/share/mole/TreeUpdatingComparison
  278  cd TreeUpdatingComparison
  279  python -m venv pyenv
  280  source /usr/local/share/mole/TreeUpdatingComparison/pyenv/bin/activate
  281  python -m pip install git+https://github.com/jeetsukumaran/DendroPy.git
  282  python -m pip list
  283  deactivate
  284  source /usr/local/share/mole/TreeUpdatingComparison/pyenv/bin/activate
  285  python -m pip install opentree
  286  python -m pip list
  287  deactivate
  288  cd
  289  curl -LO https://molevolworkshop.github.io/faculty/smith/tutorial/Machine_Learning_for_Population_Genetics.ipynb
  290  curl -LO https://molevolworkshop.github.io/faculty/smith/tutorial/Models-01.png
  291  sudo mkdir -p /usr/local/share/mole/machinelearning
  292  sudo mv Machine_Learning_for_Population_Genetics.ipynb /usr/local/share/mole/machinelearning
  293  sudo chown -R exouser.exouser /usr/local/share/examples/mole/machinelearning
  294  cd /usr/local/share/
  295  ls
  296  cd examples/
  297  ls
  298  cd ..
  299  cd mole/
  300  ls
  301  cd ..
  302  ls
  303  sudo mv mole/ examples/
  304  ls
  305  cd examples/
  306  ls
  307  ls -la
  308  cd mrbayes/
  309  ls
  310  vi .bashrc
  311  man history
  312  history
  313  ls
  314  cd /usr/local/share/examples/
  315  ls
  316  cd mole
  317  ls
  318  cd ..
  319  ls
  320  ls -la
  321  cd mrbayes/
  322  ls
  323  cd ..
  324  ls
  325  cd examples/
  326  ls
  327  cd mole
  328  ls
  329  cd phylo-networks/
  330  ls
  331  cd data_results/
  332  ls
  333  cd ..
  334  ls
  335  cd ..
  336  ls
  337  cd ..
  338  ls
  339  pwd
  340  sudo mv mrbayes mole
  341  cd mole
  342  ls
  343  ifconfig
  344  ls
  345  cd /usr/local/share/
  346  ls
  347  cd examples/
  348  ls
  349  cd mole/
  350  ls
  351  cd TreeUpdatingComparison/
  352  ls
  353  cd ..
  354  ls
  355  cd
  356  ls
  357  curl -LO https://molevolworkshop.github.io/faculty/smith/tutorial/Machine_Learning_for_Population_Genetics.ipynb
  358  ls
  359  ls -la Models-01.png
  360  mkdir temp
  361  mv Models-01.png temp
  362  curl -LO https://molevolworkshop.github.io/faculty/smith/tutorial/Models-01.png
  363  ls
  364  diff Models-01.png temp/Models-01.png
  365  rm -rf temp
  366  ls
  367  sudo mkdir -p /usr/local/share/examples/mole/machinelearning
  368  sudo mv Machine_Learning_for_Population_Genetics.ipynb /usr/local/share/examples/mole/machinelearning/
  369  sudo chown -R exouser.exouser /usr/local/share/examples/mole/machinelearning
  370  module list
  371  cd /usr/local/share/examples/mole/machinelearning/
  372  python -m venv mlenv
  373  source ./mlenv/bin/activate
  374  python -m pip install msprime==1.2.0
  375  python -m pip install numpy==1.23.5
  376  python -m pip install scipy==1.9.3
  377  python -m pip install scikit-learn==1.2.0
  378  python -m pip install tensorflow==2.10.0
  379  python -m pip install keras==2.10.0
  380  python -m pip install ipykernel
  381  deactivate
  382  mkdir -p /usr/local/share/examples/mole/machinelearning/jupyter/molekernel
  383  cd /usr/local/share/examples/mole/machinelearning/jupyter/molekernel/
  384  module load anaconda
  385  jupyter kernelspec list
  386  cp -r /software/u22/anaconda/python3.9/share/jupyter/kernels/python3
  387  cp -r /software/u22/anaconda/python3.9/share/jupyter/kernels/python3/* .
  388  nano kernel.json
  389  cd /usr/local/share/examples/mole/machinelearning/
  390  cat - > doof.sh << EOF
  391  nano doof.sh
  392  sudo apt install -y nfs-kernel-server
  393  sudo vi /etc/exports
  394  sudo systemctl restart nfs-kernel-server
  395  cd /media/volume
  396  cd /media/volume/moledata
  397  ls
  398  sudo systemctl restart nfs-kernel-server
  399  cat /etc/exports
  400  ls -la /media/volume/sdb/mole
  401  cd /media/volume/
  402  ls
  403  cd moledata/
  404  ls
  405  sudo nano /etc/exports
  406  sudo systemctl restart nfs-kernel-server
  407  history
{% endcomment %}

## Late additions

There are always modifications that need to be made to all VMs after they have been created. For each of these tasks, I use the same basic procedure. 

Before going further, I recommend that you download the [_late-additions.zip_ file](https://github.com/molevolworkshop/moledata/blob/main/late-additions.zip) from the [moledata repository](https://github.com/molevolworkshop/moledata). This zip file, when unpacked, contains example scripts and a _README.md_ file that explains how to use them. Much of the information in the _README.md_ file is duplicated below.

Note that, in each of the scripts described below, there are these lines:

        # Comment out this line and the next to run this script
        print("aborting because this script has already been run")
        exit(0)

I put these lines in as a safety check. They allow me to keep a script I've already run for future reference while preventing me from accidentally running the script again.

I created a folder named _/Users/plewis/Documents/woodshole/wh2026/computing2026_ on my local laptop with this structure:

    computing2026
        CLI-credentials
            app-cred-CLI-MOLE-2026-credentials-openrc.sh
            clouds.yaml
        late-additions
            all-vm-ids.sh
            all-vm-ips.sh
            listIPs.sh
            listVMs.sh
            .
            .
            .

The file _listIPs.sh_ can be used to get a list of the IP addresses for each VM:

    #!/bin/bash
    source ../CLI-credentials/app-cred-CLI-MOLE-2026-credentials-openrc.sh
    openstack floating ip list
    
The file listVMs.sh_ can be used to get a list of the IDs for each VM (some openstack operations require IDs, not IPs):

    #!/bin/bash
    source ../CLI-credentials/app-cred-CLI-MOLE-2026-credentials-openrc.sh
    openstack server list
    
I find it easiest to put all the VM IPs and IDs in separate bash scripts that can be sourced when needed. Here is what _all-vm-ips.sh_ looks like (only including the IP addresses for the 7 test VMs; at showtime, this file should contain IP addresses for all VMs except MOLE-2026-base):

    #!/bin/bash
    export VMIPS=(\
        149.165.147.173 \  # chelydra 1 (josh)
        149.165.147.87  \  # chelydra 2 (analisa)
        149.165.147.77  \  # chelydra 3 (solomon)
        149.165.169.167 \  # chelydra 4 (thao)
        149.165.147.128 \  # chelydra 5 (jeremy)
        149.165.173.221 \  # chelydra 6 (claudia)
        149.165.147.176 \  # chelydra 7 (paul)
        )

Here is what _all-vm-ids.sh_ looks like (only including the IDs for the 7 test VMs; at showtime, this file should contain IDs for all VMs except MOLE-2026-base):

    #!/bin/bash
    export VMIDS=(\
        2629d400-53d0-4df5-b449-73fc4445fcc0 \  # chelydra 1 (josh)
        b7d97b60-8647-4611-8416-09080d08f0ce \  # chelydra 2 (analisa)
        bb9c189c-b6d9-430a-9781-c1389c4f6ef7 \  # chelydra 3 (solomon)
        63883810-052d-4b5c-a83d-7c44d0d83036 \  # chelydra 4 (thao)
        2bb7a176-4fbd-496a-a390-5e5bf5714a60 \  # chelydra 5 (jeremy)
        39291f2f-987f-4485-a621-7a845894bd67 \  # chelydra 6 (claudia)
        27f59a98-4264-45ac-88ee-79cb308559e2 \  # chelydra 7 (paul)
        )

Here are a few common use cases. Note that I incorporate the date into the folder names. This allows me to later remember the order in which late additions were made, but it is not essential. If several late additions are carried out on one day, I add letters to the end of the date.

### Modify a symbolic link on a selection of VMs

I illustrate with an actual case. I had to modify a symbolic link on the 6 test VMs in the early testing stage in late April, 2024.

* Create a folder named _2025-10-30-modify-symlink_ under your _late-additions_ folder on your laptop
* Create a bash script named _modify-symlink.sh_ in _late-additions/2025-10-30-modify-symlink_ with these contents:

        #!/bin/bash

        # Comment out this line and the next to run this script
        print("aborting because this script has already been run")
        exit(0)
        
        source ../all-vm-ips.sh     # provides the environmental variable VMIPS
                
        for ip in ${VMIPS[@]}
        do
            ssh -t moleuser@$ip "bash -c 'rm moledata; ln -s /usr/local/share/examples/mole moledata'"
        done

* Comment out the two "sanity check" lines and run the script (assuming you are in _late-additions/2025-10-30-modify-symlink_)

        . modify-symlink.sh

You should see IP addresses listed as the script finishes each one.

As soon as you have run the script, uncomment the two sanity check lines so that it cannot be accidentally run again.

### Replace a file on a selection of VMs

* Create a folder named _2025-10-30-replace-file_ under your _late-additions_ folder on your laptop
* Create a bash script named _replace-file.sh_ in _late-additions/2025-10-30-replace-file_ with these contents:

        #!/bin/bash
        
        # Comment out this line and the next to run this script
        print("aborting because this script has already been run")
        exit(0)
        
        source ../all-vm-ips.sh
        
        for ip in ${VMIPS[@]}
        do
            echo $ip
            scp junk.sh moleuser@$ip:/tmp
            ssh -t moleuser@$ip "bash -c 'cd /tmp; chmod +x junk.sh; sudo mv junk.sh /usr/local/bin'"
        done

* Comment out the two "sanity check" lines and run the script (assuming you are in _late-additions/2025-10-30-replace-file_ folder)

        . replace-file.sh_

As soon as you have run the script, uncomment the two sanity check lines so that it cannot be accidentally run again.

### Shelve a selection of VMs

* Create a folder named _2025-10-30-shelve_ under your _late-additions_ folder on your laptop
* Create a bash script named _shelve.sh_ in _late-additions/2025-10-30-shelve_ with these contents:

        #!/bin/bash
        
        # Comment out this line and the next to run this script
        print("aborting because this script has already been run")
        exit(0)
        
        source ../../CLI-credentials/app-cred-POL-CLI-MOLE-2025-credentials-openrc.sh
        source ../all-vm-ids.sh
        
        for id in ${VMIDS[@]} ; do
            echo Shelving $id
            openstack server shelve $id
        done

* Comment out the two "sanity check" lines and run the script (assuming you are in _late-additions/2025-10-30-shelve_ folder)

        . shelve.sh

The only new thing here is the `source` command loading the variables in my CLI-credentials file. This is necessary before using any openstack commands in your script. An additional `source` command is used to load all the VM IDs that will be visited in the for loop.

Note that you could use a similar script to unshelve all VMs.

As soon as you have run the script, uncomment the two sanity check lines so that it cannot be accidentally run again.

### Lock a selection of VMs

* Create a folder named _2025-10-30-lock_ under your _late-additions_ folder on your laptop
* Create a bash script named _lock.sh_ in _late-additions/2025-10-30-lock_ with these contents:

        #!/bin/bash
        
        # Comment out this line and the next to run this script
        print("aborting because this script has already been run")
        exit(0)
        
        source ../../CLI-credentials/app-cred-CLI-MOLE-2026-credentials-openrc.sh
        source ../all-vm-ids.sh
        
        for vm in ${VMIDS[@]} ; do
            echo Locking $vm
            openstack server lock $vm
        done

* Comment out the two "sanity check" lines and run the script (assuming you are in _late-additions/2025-10-30-lock_ folder)

        . lock.sh

The first `source` command loads the variables in my CLI-credentials file. This is necessary before using any openstack commands in your script. The second `source` command is used to load all the VM IDs that will be visited in the for loop.

Note that you could use a similar script to unlock all VMs.

As soon as you have run the script, uncomment the two sanity check lines so that it cannot be accidentally run again.
