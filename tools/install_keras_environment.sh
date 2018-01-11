# file: install_keras_environment.sh
#
#    Summary:
#    ====================================================================
#
#    Install Ubuntu dependencies and create a conda environment for
#    the master version of Keras.
#
#    Syntax:
#    ====================================================================
#
#    ./install_keras_environment.sh [conda_env]
#
#    Options:
#
#    conda_env:
#       name of the conda environment to be created or added to (def. keras).

#!/bin/bash

# exit immediately on errors that are not inside an if test, etc.
set -e

# assign default input argument
if [ "$#" -eq 0 ]
then
    # default input value
    CONDA_ENV=keras
else
    # input value provided by user
    CONDA_ENV="$1"
fi

######################################################################

# install Miniconda 3
./install_miniconda.sh 3

# install CUDA toolkit for Ubuntu 17.04 directly from the Nvidia website
./install_cuda.sh nvidia_ubuntu_17.04

######################################################################

tput setaf 1; echo "** Build tools"; tput sgr0

# build tools
sudo apt install -y cmake

# python IDE
sudo snap install pycharm-community --classic

######################################################################
## python conda environment

# if the environment doesn't exist, we create a new one. If it does,
# we add the python packages to it

# check whether the environment already exists
if [ -z "$(conda info --envs | sed '/^#/ d' | cut -f1 -d ' ' | grep -w $CONDA_ENV)" ]; then
    tput setaf 1; echo "** Create conda local environment: $CONDA_ENV"; tput sgr0
    conda create -y --name $CONDA_ENV python=3.6
else
    tput setaf 1; echo "** Conda local environment already exists: $CONDA_ENV"; tput sgr0
fi

# switch to the local environment
source activate $CONDA_ENV

# install Tensorflow, Theano and keras latest version from source
pip install tensorflow-gpu pyyaml
pip install git+https://github.com/fchollet/keras.git --upgrade --no-deps
pip install git+https://github.com/Theano/Theano.git --upgrade --no-deps
pip install nose-parameterized
conda install -y scipy Cython cudnn=6 mkl-service
pip install pycuda scikit-cuda

# install libgpuarray from source, with python bindings
cd ~/Software
if [ -d libgpuarray ]; then # previous version present
    cd libgpuarray
    git pull
else # no previous version exists
    git clone https://github.com/Theano/libgpuarray.git
    cd libgpuarray
    mkdir Build
fi
cd Build
cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX:PATH=$CONDA_PREFIX
make
make install
cd ..
python setup.py -q build_ext -L $CONDA_PREFIX/lib -I $CONDA_PREFIX/include
python setup.py -q install --prefix=$CONDA_PREFIX

# clear Theano cache. Previous runs of Keras may cause CUDA compilation/version compatibility problems
theano-cache purge
