# file: install_pysto_environment.sh
#
#    Summary:
#    ====================================================================
#
#    Project pysto's script to create local environments for python
#    2.7 ("pysto_2.7") and 3.6 ("pysto_3.6"), and install Ubuntu and
#    python dependencies.
#
#    This is a script for developers only. Users will get the
#    simpleitk installed as a dependency when they run `pip install
#    pysto`.
#
#
#    Syntax:
#    ====================================================================
#
#    ./install_pysto_environment.sh
#    ./install_pysto_environment.sh SimpleITK
#
#         This installs developer programs, as well as package
#         dependencies. One of the dependencies is SimpleITK. With
#         either syntax above, we install the official SimpleITK
#         package.
#
#    ./install_pysto_environment.sh SimpleElastix
#
#         However, we may prefer installing SimpleElastix, an
#         extension of SimpleITK. In this latter case, there's no
#         pip/conda package, so we have to download and build the
#         SimpleElastix project. This process is delegated to script
#         build_SimpleElastix.sh.
#
#
#    Developer notes:
#    ====================================================================
#
#    Some design decisions:
#
#        1) We create and build conda environments SimpleElastix_2.7
#           and SimpleElastix_3.6 to build the project for python 2.7
#           and 3.6, respectively.
#
#           This way, we only need to build once and then can install
#           in any other local environment, whether pysto or an
#           external project.
#
#           TODO: Currently we build separatedly for 2.7 and 3.6, as
#           we haven't figured out how to reused the part of the build
#           that is independent from python.
#
#        2) We disable shared libraries in the SimpleITK build. This
#           way, _SimpleITK.cpython-*-x86_64-linux-gnu.so is not
#           linked to anything in the SimpleElastix_2.7 or
#           SimpleElastix_3.6 directories, and is more portable for
#           other local environments.
#
#        3) For the SimpleElastix build, we use the python binary,
#           include and library from the corresponding conda
#           SimpleElastix_* environments. This way, we know that they
#           will be the same that other conda local environments use.

#    Copyright © 2017-2018  Ramón Casero <rcasero@gmail.com>
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

#################################################################################################
# syntax

# check input parameters and assign default
if [ "$#" -eq 0 ]
then
    # default input value
    SIMPLEITK_PROJ=SimpleITK
elif [ "$#" -eq 1 ]
then
    SIMPLEITK_PROJ=$1
    if [[ $SIMPLEITK_PROJ != "SimpleITK" ]] && [[ $SIMPLEITK_PROJ != "SimpleElastix" ]]
    then
	/usr/bin/tput setaf 1
	echo "Error: Syntax: ./install_pysto_environment.sh [SimpleITK | SimpleElastix]"
	/usr/bin/tput sgr0
	exit 1
    fi
else
    /usr/bin/tput setaf 1
    echo "Error: Syntax: ./install_pysto_environment.sh [SimpleITK | SimpleElastix]"
    /usr/bin/tput sgr0
    exit 1
fi

#################################################################################################
# auxiliary functions

# # creates conda local environment foo_2.7 with python 2.7 if it doesn't exist
# create_conda_local_environment foo 2.7 
# # creates conda local environment foo_3.6 with python 3.6 if it doesn't exist
# create_conda_local_environment foo 3.6 
create_conda_local_environment() {
    NAME=$1
    PYTHON_VERSION=$2

    if [ -z "$(conda info --envs | sed '/^#/ d' | cut -f1 -d ' ' | grep -w ${NAME}_${PYTHON_VERSION})" ]; then
	/usr/bin/tput setaf 1; echo "** Create conda local environment: ${NAME}_${PYTHON_VERSION}"; /usr/bin/tput sgr0
	conda create -y --name ${NAME}_${PYTHON_VERSION} python=${PYTHON_VERSION}
    else
	/usr/bin/tput setaf 1; echo "** Conda local environment already exists (...skipping): ${NAME}_${PYTHON_VERSION}"; /usr/bin/tput sgr0
    fi
}

#################################################################################################
# basic packages

# ubuntu packages
sudo apt-get install -y jq curl automake python3-docutils pandoc

#################################################################################################
# install conda package manager

./install_miniconda.sh 3

#################################################################################################
# pysto local environment: for python 2.7
create_conda_local_environment pysto 2.7 || exit 1

# switch to pysto local environment
/usr/bin/tput setaf 1; echo "** Switching to local environment: pysto_2.7"; /usr/bin/tput sgr0
source activate pysto_2.7 || exit 1

# install pysto code and dependencies
/usr/bin/tput setaf 1; echo "** Install pysto code and dependencies in local environment"; /usr/bin/tput sgr0
pip install --upgrade . || exit 1

# install development tools
/usr/bin/tput setaf 1; echo "** Install development tools in local environment"; /usr/bin/tput sgr0
conda install -y spyder pytest pillow
pip install --upgrade twine wheel setuptools

#################################################################################################
# pysto local environment: for python 3.6

create_conda_local_environment pysto 3.6 || exit 1

# switch to pysto local environment
/usr/bin/tput setaf 1; echo "** Switching to local environment: pysto_3.6"; /usr/bin/tput sgr0
source activate pysto_3.6 || exit 1

# install pysto code and dependencies
/usr/bin/tput setaf 1; echo "** Install pysto code and dependencies in local environment"; /usr/bin/tput sgr0
pip install --upgrade . || exit 1

# install development tools
/usr/bin/tput setaf 1; echo "** Install development tools in local environment"; /usr/bin/tput sgr0
conda install -y spyder pytest pillow
pip install --upgrade twine wheel setuptools

#################################################################################################
# install SimpleITK or build and install SimpleElastix (which is SimpleITK extended with more functions)

# pysto requires

if [ "$SIMPLEITK_PROJ" == SimpleElastix ]
then

    # TODO: we build SimpleElastix in separate 2.7 and 3.6
    # environments. Ideally, we would like to do the following:
    #
    # 1. build without python wrappers (very slow)
    # 2. generate python wrappers for python 2.7 (fast)
    # 3. generate python wrappers for python 3.6 (fast)
    #
    # But currently, it seems that running cmake for 1 and then for 2 or 3
    # triggers a full rebuild
    
    ./build_SimpleElastix.sh 2.7 || exit 1
    ./build_SimpleElastix.sh 3.6 || exit 1

    # install SimpleElastix python wrappers
    source activate pysto_2.7 || exit 1
    cd ~/Downloads/SimpleElastix/build_2.7/SimpleITK-build/Wrapping/Python/Packaging || exit 1
    python setup.py --upgrade install || exit 1
    
    # install SimpleElastix python wrappers
    source activate pysto_3.6 || exit 1
    cd ~/Downloads/SimpleElastix/build_3.6/SimpleITK-build/Wrapping/Python/Packaging || exit 1
    python setup.py --upgrade install || exit 1

else

    source activate pysto_2.7 || exit 1
    pip install --upgrade simpleitk || exit 1
    
    source activate pysto_3.6 || exit 1
    pip install --upgrade simpleitk || exit 1
    
fi
