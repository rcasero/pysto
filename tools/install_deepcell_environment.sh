# file: install_deepcell_environment.sh
#
#    Summary:
#    ====================================================================
#
#    Install Ubuntu dependencies and create a DeepCell conda
#    environment to run DeepCell architectures using Keras 1/Theano.
#
#    DeepCell is a convolutional neural network proposed by David Van
#    Valen, Takamasa Kudo, Keara Lane, Derek Macklin, Nicolas Quach,
#    Mialy DeFelice, Inbal Maayan, Yu Tanouchi, Euan Ashley, and
#    Markus Covert, Deep learning automates the quantitative analysis
#    of individual cells in live-cell imaging experiments. PLoS Comput
#    Biol 12(11): e1005177. doi: 10.1371/journal.pcbi.1005177
#
#    The python code can be downloaded from
#
#    https://github.com/CovertLab/DeepCell/

#    Copyright © 2018  Ramón Casero <rcasero@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

#!/bin/bash

# exit immediately on errors that are not inside an if test, etc.
set -e

######################################################################

# install Miniconda 3
./install_miniconda.sh 3

# install CUDA toolkit for Ubuntu 17.04 directly from the Nvidia website
./install_cuda.sh nvidia_ubuntu_17.04

######################################################################

tput setaf 1; echo "** Build tools"; tput sgr0

# build tools
sudo apt install -y cmake

# for DeepCell
sudo apt install gcc-5 g++-5

# python IDE
sudo snap install pycharm-community --classic

# install Miniconda 3
./install_miniconda.sh 3

######################################################################

if [ -z "$(conda info --envs | sed '/^#/ d' | cut -f1 -d ' ' | grep -w DeepCell)" ]; then
    tput setaf 1; echo "** Create conda local environment: DeepCell"; tput sgr0
    conda create -y --name DeepCell python=2.7
else
    tput setaf 1; echo "** Conda local environment already exists (...skipping): DeepCell"; tput sgr0
fi

source activate DeepCell

# current latest version of pip (9.0.1) gives "Command 'lsb_release
# -a' returned non-zero exit status 1" error, so we need to downgrade
# to 8.1.2
conda install -y pip=8.1.2

# install Keras 1
conda install -y keras=1.1.1 theano=0.9.0
conda install -y cudnn=5.1 pygpu=0.6.9
conda install -y mkl-service

# install other python packages
conda install -y matplotlib pillow
conda install -y scikit-image scikit-learn h5py
conda install -y -c conda-forge tifffile mahotas
conda install -y nose pytest
pip install opencv-python pysto

# clear Theano cache. Previous runs of Keras may cause CUDA compilation/version compatibility problems
theano-cache purge
