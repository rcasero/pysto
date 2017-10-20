# install_dependencies.sh
#
#    Summary:
#    ====================================================================
#
#    Project pysto's script to create local environments for python
#    2.7 ("pysto_2.7") and 3.6 ("pysto_3.6"), and install Ubuntu and
#    python dependencies.
#
#    An important dependency is SimpleElastix. As SimpleElastix is not
#    required for all modules, and it has no pip/conda package,
#    instead we build and install it with this script.
#
#    SimpleElastix/SimpleITK:
#    ====================================================================
#
#    Some parts of pysto require SimpleITK. This can be installed
#    either with
#
#         conda install -c simpleitk simpleitk
#
#    or
#
#         pip install simpleitk
#
#    However, we are working in another project were we use image
#    registration with SimpleElastix. SimpleElastix is an externsion
#    of SimpleITK that has no pip/conda package, and needs to be built
#    by hand.
#
#    Thus, in this script we download, build and install
#    SimpleElastix.
#
#    We do it in separate local environments, so that other projects
#    external to pysto can install SimpleElastix without having to
#    rebuild it, just by running
#
#        source activate my_other_project
#        cd ~/Downloads/SimpleElastix/build_2.7/SimpleITK-build/Wrapping/Python/Packaging
#        python setup.py install
#
#    or
#
#        source activate my_other_project
#        cd ~/Downloads/SimpleElastix/build_3.6/SimpleITK-build/Wrapping/Python/Packaging
#        python setup.py install
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

#    Copyright © 2017  Ramón Casero <rcasero@gmail.com>
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
# auxiliary functions

# # creates conda local environment foo_2.7 with python 2.7 if it doesn't exist
# create_conda_local_environment foo 2.7 
# # creates conda local environment foo_3.6 with python 3.6 if it doesn't exist
# create_conda_local_environment foo 3.6 
create_conda_local_environment() {
    NAME=$1
    PYTHON_VERSION=$2

    if [ -z "$(conda info --envs | sed '/^#/ d' | cut -f1 -d ' ' | grep -w ${NAME}_${PYTHON_VERSION})" ]; then
	tput setaf 1; echo "** Create conda local environment: ${NAME}_${PYTHON_VERSION}"; tput sgr0
	conda create -y --name ${NAME}_${PYTHON_VERSION} python=${PYTHON_VERSION}
    else
	tput setaf 1; echo "** Conda local environment already exists (...skipping): ${NAME}_${PYTHON_VERSION}"; tput sgr0
    fi
}

# get paths to python executable, include directory and library
get_python_executable() {
    PYTHON_EXECUTABLE=`which python`
    if [[ ! -e "$PYTHON_EXECUTABLE" ]]
    then
	tput setaf 1
	>&2 echo "Error: Python executable not found: \"$PYTHON_EXECUTABLE\""
	tput sgr0
	#exit 1
    fi
    echo $PYTHON_EXECUTABLE
}
# location of Python.h in the conda environment
get_python_include_dir() {
    PYTHON_INCLUDE_DIR=`find ${CONDA_PREFIX}/include/ -name Python.h | xargs dirname`
    if [[ ! -d "$PYTHON_INCLUDE_DIR" ]]
    then
	tput setaf 1
	>&2 echo "Error: Python include dir not found: \"$PYTHON_INCLUDE_DIR\""
	tput sgr0
	#exit 1
    fi
    echo $PYTHON_INCLUDE_DIR
}
get_python_library() {
    PYTHON_LIBRARY=`python -c 'from distutils import sysconfig; \
import os; \
print(os.path.join(sysconfig.get_config_var("LIBDIR"), sysconfig.get_config_var("LDLIBRARY")))'`
    if [[ ! -e "$PYTHON_LIBRARY" ]]
    then
	tput setaf 1
	>&2 echo "Error: Python library not found: $PYTHON_LIBRARY"
	tput sgr0
	#exit 1
    fi
    echo $PYTHON_LIBRARY
}

#################################################################################################
# basic packages

# ubuntu packages
sudo apt-get install -y jq curl automake

# conda package manager
if hash conda 2>/dev/null; then
    tput setaf 1; echo "** Conda 3 package manager already installed"; tput sgr0
else
    tput setaf 1; echo "** Installing conda 3 package manager"; tput sgr0
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
# pysto local environment: for python 2.7
create_conda_local_environment pysto 2.7

# switch to pysto local environment
tput setaf 1; echo "** Switching to local environment: pysto_2.7"; tput sgr0
source activate pysto_2.7

# install pysto code and dependencies
tput setaf 1; echo "** Install pysto code and dependencies in local environment"; tput sgr0
pip install --upgrade .

# install development tools
tput setaf 1; echo "** Install development tools in local environment"; tput sgr0
conda install -y spyder pytest
pip install twine wheel setuptools --upgrade

#################################################################################################
# pysto local environment: for python 3.6
create_conda_local_environment pysto 3.6

# switch to pysto local environment
tput setaf 1; echo "** Switching to local environment: pysto_3.6"; tput sgr0
source activate pysto_3.6

# install pysto code and dependencies
tput setaf 1; echo "** Install pysto code and dependencies in local environment"; tput sgr0
pip install --upgrade .

# install development tools
tput setaf 1; echo "** Install development tools in local environment"; tput sgr0
conda install -y spyder pytest
pip install twine wheel setuptools --upgrade

########################################################################
# build SimpleElastix and install python wrappers

# another type of local environment used by SimpleElastix's SuperBuild
conda install -y virtualenv

# TODO: we build SimpleElastix in separate 2.7 and 3.6 environments,
# as currently we are not sure how to make the produced SimpleITK
# shared object link to the local libraries in each separate local
# environment
create_conda_local_environment SimpleElastix 2.7
create_conda_local_environment SimpleElastix 3.6

# prepare to install SimpleElastix
tput setaf 1; echo "** Clone or update SimpleElastix code"; tput sgr0
cd ~/Downloads
if [ -d SimpleElastix ]
then
   cd SimpleElastix
   git pull
else
   git clone https://github.com/SuperElastix/SimpleElastix
   cd SimpleElastix
fi

# we are going to build for each python version in a separate
# directory. When you try to reuse the same directory, the build
# restarts anyway
mkdir -p build_2.7
mkdir -p build_3.6

# build for python 2.7
source activate SimpleElastix_2.7 || exit 1
cd ~/Downloads/SimpleElastix/build_2.7

SITK_OPTS="\
-DWRAP_PYTHON:BOOL=ON \
-DPYTHON_EXECUTABLE:FILEPATH=$(get_python_executable) \
-DPYTHON_INCLUDE_DIR:PATH=$(get_python_include_dir) \
-DPYTHON_LIBRARY:FILEPATH=$(get_python_library) \
-DWRAP_DEFAULT:BOOL=OFF \
-DBUILD_TESTING:BOOL=OFF \
-DBUILD_EXAMPLES:BOOL=OFF \
-DBUILD_SHARED_LIBS:BOOL=OFF \
-DITK_BUILD_TESTING:BOOL=OFF \
-DITK_BUILD_EXAMPLES:BOOL=OFF \
-DITK_BUILD_DOCUMENTATION:BOOL=OFF \
-DSimpleITK_OPENMP:BOOL=ON"
cmake $SITK_OPTS ../SuperBuild || exit 1
make -j4 || exit 1

# install python wrappers
cd SimpleITK-build/Wrapping/Python/Packaging || exit 1
python setup.py install || exit 1

# build for python 3.6
source activate SimpleElastix_3.6 || exit 1
cd ~/Downloads/SimpleElastix/build_3.6

SITK_OPTS="\
-DWRAP_PYTHON:BOOL=ON \
-DPYTHON_EXECUTABLE:FILEPATH=$(get_python_executable) \
-DPYTHON_INCLUDE_DIR:PATH=$(get_python_include_dir) \
-DPYTHON_LIBRARY:FILEPATH=$(get_python_library) \
-DWRAP_DEFAULT:BOOL=OFF \
-DBUILD_TESTING:BOOL=OFF \
-DBUILD_EXAMPLES:BOOL=OFF \
-DBUILD_SHARED_LIBS:BOOL=OFF \
-DITK_BUILD_TESTING:BOOL=OFF \
-DITK_BUILD_EXAMPLES:BOOL=OFF \
-DITK_BUILD_DOCUMENTATION:BOOL=OFF \
-DSimpleITK_OPENMP:BOOL=ON"
cmake $SITK_OPTS ../SuperBuild || exit 1
make -j4 || exit 1

# switch to pysto to install SimpleElastix there
source activate pysto_3.6

# install python wrappers
cd SimpleITK-build/Wrapping/Python/Packaging || exit 1
python setup.py install || exit 1



