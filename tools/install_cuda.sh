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
#    Note: If you have a previously installed CUDA Toolkit from the
#      Nvidia website, and try to install the other, you'll get the
#      error
#
#      Unpacking cuda-repo-ubuntu1604-9-1-local (9.1.85-1) ...
#      dpkg: error processing archive cuda-repo-ubuntu1604-9-1-local_9.1.85-1_amd64.deb (--install):
#      trying to overwrite '/etc/apt/sources.list.d/cuda-9-1-local.list', which is also in package cuda-repo-ubuntu1704-9-1-local 9.1.85-1
#      dpkg-deb: error: subprocess paste was killed by signal (Broken pipe)
#
#      First, you need to manually uninstall the previous version:
#
#      sudo apt remove -y --purge conda
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

exit 0
