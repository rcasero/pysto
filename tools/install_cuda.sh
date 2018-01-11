# file: install_cuda.sh
#
#    Summary:
#    ====================================================================
#
#    Install Nvidia CUDA Toolkit in Ubuntu.
#
#    Syntax:
#    ====================================================================
#
#    ./install_cuda.sh [ubuntu_packages | nvidia_ubuntu_16.04 | nvidia_ubuntu_17.04]
#
#    Options:
#
#      ubuntu_packages: (def) From Ubuntu official packages.
#
#      nvidia_ubuntu_16.04: From the Nvidia website, .deb packages for Ubuntu 16.04 (x86_64)
#
#      nvidia_ubuntu_17.04: From the Nvidia website, .deb packages for Ubuntu 17.04 (x86_64)
#
#    Note: If you choose an Nvidia website installation, and the cuda
#      package is already installed, installation is skipped. To
#      manually uninstall the previous version:
#
#      sudo apt remove -y --purge cuda
#      sudo apt autoremove -y --purge


#!/bin/bash

# exit immediately on errors that are not inside an if test, etc.
set -e

# assign default input argument
if [ "$#" -eq 0 ]
then
    # default input value
    CUDA_TYPE=ubuntu_packages
else
    # input value provided by user
    CUDA_TYPE="$1"
fi

######################################################################

tput setaf 1; echo "** Installing Nvidia CUDA Toolkit"; tput sgr0

## CUDA Toolkit installation. There are several options (uncomment the preferred one):

if [ "$CUDA_TYPE" ==  "ubuntu_packages" ]
then
    
    # Option 1. CUDA Toolkit from the Ubuntu distribution packages
    echo "** Remove Nvidia website packages, if present"
    set +e
    sudo apt remove -y --purge cuda
    sudo apt autoremove -y
    set -e
    echo "** Install current Ubuntu official packages"
    sudo apt install -y nvidia-cuda-dev nvidia-cuda-toolkit
    exit 0
    
elif [ "$CUDA_TYPE" ==  "nvidia_ubuntu_16.04" ]
then
    # Option 2. From Nvidia website:
    # CUDA Toolkit 9.1 for Ubuntu 16.04
    CUDA_VERSION=cuda-repo-ubuntu1604-9-1-local_9.1.85-1_amd64
elif [ "$CUDA_TYPE" ==  "nvidia_ubuntu_17.04" ]
then
    # Option 2. From Nvidia website:
    # CUDA Toolkit 9.1 for Ubuntu 17.04
    CUDA_VERSION=cuda-repo-ubuntu1704-9-1-local_9.1.85-1_amd64
else
    echo "Error: Option not recognised: $CUDA_TYPE"
    exit 1
fi

## Common code to NVIDA website CUDA Toolkit installation

echo
echo "** Remove Ubuntu official packages, if present"
set +e
sudo apt remove -y --purge nvidia-cuda-dev nvidia-cuda-toolkit
sudo apt autoremove -y
set -e

echo

echo "** Install Nvidia website packages"

# check whether package cuda is already installed
#
# The following line of code produces 0 if the package is not listed
# yet in APT or is not installed, and 1 if it's installed. E.g.,
# assuming that the cuda package is installed
#
#   $ dpkg-query -l cuda 2>/dev/null
#   Desired=Unknown/Install/Remove/Purge/Hold
#   | Status=Not/Inst/Conf-files/Unpacked/halF-conf/Half-inst/trig-aWait/Trig-pend
#   |/ Err?=(none)/Reinst-required (Status,Err: uppercase=bad)
#   ||/ Name                    Version          Architecture     Description
#   +++-=======================-================-================-====================================================
#   ii  cuda                    9.1.85-1         amd64            CUDA meta-package
#
#   $ dpkg-query -l cuda 2>/dev/null| tail -n 1
#   ii  cuda           9.1.85-1     amd64        CUDA meta-package
#
#   $ dpkg-query -l cuda 2>/dev/null| tail -n 1 | sed 's/  */ /g'
#   ii cuda 9.1.85-1 amd64 CUDA meta-package
#
#   $ dpkg-query -l cuda 2>/dev/null| tail -n 1 | sed 's/  */ /g' | cut -f 3 -d ' '
#   9.1.85-1
#
#   $ dpkg-query -l cuda 2>/dev/null| tail -n 1 | sed 's/  */ /g' | cut -f 3 -d ' ' | sed 's/[a-Z<>]//g'
#   9.1.85-1
#
#   $ dpkg-query -l cuda 2>/dev/null | tail -n 1 | sed 's/  */ /g' | cut -f 3 -d ' ' | sed 's/[a-Z<>]//g' | wc -w
#   1

CHECK=`dpkg-query -l cuda 2>/dev/null | tail -n 1 | sed 's/  */ /g' | cut -f 3 -d ' ' | sed 's/[a-Z<>]//g' | wc -w`

if [ $CHECK -eq 0 ]
then
    echo "** Installing cuda package"
    pushd ~/Downloads
    if [ ! -e "${CUDA_VERSION}.deb" ];
    then
	wget https://developer.nvidia.com/compute/cuda/9.1/Prod/local_installers/${CUDA_VERSION}
    fi
    sudo dpkg -i ${CUDA_VERSION}.deb
    sudo apt-key add /var/cuda-repo-9-1-local/7fa2af80.pub
    sudo apt-get update
    sudo apt-get install -y cuda
    popd
else
    echo "** cuda package already installed, skipping"
fi
