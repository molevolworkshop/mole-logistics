#!/bin/bash

# Shelves all VMs (this causes them to stop burning any SUs)

# Comment out this line and the next to run this script
#print("aborting because this script has already been run")
#exit(0)

source ../../CLI-credentials/app-cred-CLI-MOLE-2026-credentials-openrc.sh

# not sourcing faculty-vm-ids.sh because peter's vm has already been shelved and dave's vm needs to remain active
VMIDS=(
    # 393b57a6-c718-4799-a2d9-2998a051ea78  # apalone 1 of 14  peter beerli
    526b3826-8725-4178-84a5-697443237c1f  # apalone 2 of 14  joe bielawski
    8a4af20b-c726-425b-b3a5-c4bc06ac2d58  # apalone 3 of 14  belinda chang
    9cca6122-0a65-452d-b5a9-53668d0c1619  # apalone 4 of 14  scott edwards
    d61c67cf-79cc-4770-a1f8-6900670b06d7  # apalone 5 of 14  laura eme
    c5922800-90a1-4016-9ea1-b91713c3d1b7  # apalone 6 of 14  mandev gill
    896f0ca6-d705-46cd-a3ef-d0a1f68d9999  # apalone 7 of 14  tracy heath
    001404e7-2734-4cfe-a6ec-c370e9a2c980  # apalone 8 of 14  lacey knowles
    6417112e-3a71-4e07-8b55-43df3c24fd5d  # apalone 9 of 14  laura kubatko
    605389af-7753-44d4-82ad-b50af0465d06  # apalone 10 of 14 emily jane mctavish
    97a1ac84-8ef3-43c4-b39a-be7441b8f121  # apalone 11 of 14 corrie moreau
    23a1c38d-71e6-4674-bb6b-73d347e53d9f  # apalone 12 of 14 megan smith
    # 8d3ee0fe-bbb1-4850-8573-1b1a31a8088b  # apalone 13 of 14 david swofford
    23b4e1f1-e3da-4736-a78c-69ebdaac41f5  # apalone 14 of 14 rosana zenil-ferguson
    )

for id in ${VMIDS[@]} ; do
	echo Shelving $id
    openstack server unlock $id
    openstack server shelve $id
    openstack server lock $id
done


 