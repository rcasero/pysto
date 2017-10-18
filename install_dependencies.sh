# install_dependencies.sh
#
#    Script to create a local environment ("pysto") and install
#    dependencies for pysto.

#    Copyright (C) 2017  Ramón Casero <rcasero@gmail.com>
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

# ubuntu packages
sudo apt-get install -y jq curl

# conda package manager
if hash conda 2>/dev/null; then
    tput setaf 1; echo "** Conda package manager already installed"; tput sgr0
else
    tput setaf 1; echo "** Installing conda package manager"; tput sgr0
    # download installer
    if [ ! -e Miniconda3-latest-Linux-x86_64.sh ]
    then
	wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
    fi
    # install conda
    chmod u+x Miniconda3-latest-Linux-x86_64.sh
    sudo ./Miniconda3-latest-Linux-x86_64.sh -b -p /opt/miniconda3
    source ~/.bashrc
fi

#################################################################################################
# conda local environment: for python 2.7
if [ -z "$(conda info --envs | sed '/^#/ d' | cut -f1 -d ' ' | grep -w pysto_2.7)" ]; then
    tput setaf 1; echo "** Create conda local environment: pysto_2.7"; tput sgr0
    conda create -y --name pysto_2.7 python=2.7
else
    tput setaf 1; echo "** Conda local environment already exists (...skipping): pysto_2.7"; tput sgr0
fi

# switch to pysto local environment
tput setaf 1; echo "** Switching to local environment: pysto_2.7"; tput sgr0
source activate pysto_2.7

# install pysto code and dependencies
tput setaf 1; echo "** Install pysto code and dependencies in local environment"; tput sgr0
pip install .

# install development tools
tput setaf 1; echo "** Install development tools in local environment"; tput sgr0
conda install -y spyder pytest
pip install twine wheel setuptools --upgrade

#################################################################################################
# conda local environment: for python 3.6
if [ -z "$(conda info --envs | sed '/^#/ d' | cut -f1 -d ' ' | grep -w pysto_3.6)" ]; then
    tput setaf 1; echo "** Create conda local environment: pysto_3.6"; tput sgr0
    conda create -y --name pysto_3.6 python=3.6
else
    tput setaf 1; echo "** Conda local environment already exists (...skipping): pysto_3.6"; tput sgr0
fi

# switch to pysto local environment
tput setaf 1; echo "** Switching to local environment: pysto_3.6"; tput sgr0
source activate pysto_3.6

# install pysto code and dependencies
tput setaf 1; echo "** Install pysto code and dependencies in local environment"; tput sgr0
pip install .

# install development tools
tput setaf 1; echo "** Install development tools in local environment"; tput sgr0
conda install -y spyder pytest
pip install twine wheel setuptools --upgrade

########################################################################
# build SimpleElastix and install python wrappers

# another type of local environment used by SimpleElastix's SuperBuild
conda install -y virtualenv

# we build outside the local environment (this way, we have one build
# for all local environments)
source deactivate

# prepare to install SimpleElastix
pushd ~/Downloads
if [ -d SimpleElastix ]
then
   cd SimpleElastix
   git pull
else
   git clone https://github.com/SuperElastix/SimpleElastix
   cd SimpleElastix
fi
mkdir -p build
cd build

# build and install simpleElastix. No python wrapper.
# Skip tests, examples and documentation to speed things up
ITK_OPTS="\
-DPYTHON_EXECUTABLE:FILEPATH= \
-DPYTHON_INCLUDE_DIR:PATH= \
-DPYTHON_LIBRARY:FILEPATH= \
-DWRAP_DEFAULT:BOOL=OFF \
-DWRAP_PYTHON:BOOL=OFF \
-DBUILD_TESTING:BOOL=OFF \
-DBUILD_EXAMPLES:BOOL=OFF \
-DBUILD_SHARED_LIBS:BOOL=OFF \
-DITK_BUILD_TESTING:BOOL=OFF \
-DITK_BUILD_EXAMPLES:BOOL=OFF \
-DITK_BUILD_DOCUMENTATION:BOOL=OFF \
-DSimpleITK_OPENMP:BOOL=ON"
cmake $ITK_OPTS ../SuperBuild || exit 1
make -j4 || exit 1

#-DPYTHON_EXECUTABLE:FILEPATH=$PYTHON_EXECUTABLE \
#-DPYTHON_INCLUDE_DIR:PATH=$PYTHON_INCLUDE_DIR \
#-DPYTHON_LIBRARY:FILEPATH=$PYTHON_LIBRARY \


# we want to use python provided by anaconda, to avoid having
# unexpected versions detected in the system
PYTHON_EXECUTABLE=/opt/miniconda3/bin/python
PYTHON_INCLUDE_DIR=/opt/miniconda3/include/python3.6m
PYTHON_LIBRARY=/opt/miniconda3/lib/libpython3.6m.so
if [ ! -e $PYTHON_EXECUTABLE ]
then
    tput setaf 1
    >&2 echo "Error: Python executable not found: $PYTHON_EXECUTABLE"
    tput sgr0
    exit 1
fi
if [ ! -d $PYTHON_INCLUDE_DIR ]
then
    tput setaf 1
    >&2 echo "Error: Python include dir not found: $PYTHON_INCLUDE_DIR"
    tput sgr0
    exit 1
fi
if [ ! -e $PYTHON_LIBRARY ]
then
    tput setaf 1
    >&2 echo "Error: Python library not found: $PYTHON_LIBRARY"
    tput sgr0
    exit 1
fi

# we activate the local environment to install the python package
source activate histo2ct

# install python wrappers
cd SimpleITK-build/Wrapping/Python/Packaging || exit 1
python setup.py install || exit 1
