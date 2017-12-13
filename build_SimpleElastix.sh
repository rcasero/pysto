#!/bin/bash

# Syntax:
#
#     ./build_SimpleElastix.sh pv
#
#         pv: The version of python we want to build the wrappers for,
#         e.g. 2.7, 3.6...
#
# Dependencies: conda needs to be installed so that we can work with local environments.
#
# This script downloads the SimpleElastix code to
#
#     ~/Software/SimpleElastix
#
# and creates a SimpleElastix_pv local environment to build
# it. Afterwards, the user or another script can install SimpleElastix
# for python in another local environment doing e.g.
#
#     ./build_SimpleElastix.sh 3.6
#     cd ~/Software/SimpleElastix/build_3.6/SimpleITK-build/Wrapping/Python/Packaging
#     python setup.py install


#################################################################################################
# syntax

# check number of input parameters
if [ "$#" -ne 1 ]; then
    tput setaf 1
    echo "Error: Syntax: ./build_SimpleElastix.sh PYTHON_VERSION"
    tput sgr0
    exit 1
fi

# assing inputs to easier variable names
PYTHON_VERSION=$1

tput setaf 1; echo "** Building SimpleElastix for python version: ${PYTHON_VERSION}"; tput sgr0

#################################################################################################
# auxiliary functions

# create conda local environment foo_2.7 with python 2.7 if it doesn't exist
#
#     create_conda_local_environment foo 2.7
#
# creates conda local environment foo_3.6 with python 3.6 if it doesn't exist
#
#     create_conda_local_environment foo 3.6 
create_conda_local_environment() {
    NAME=$1
    PYTHON_VERSION=$2

    if [ -z "$(conda info --envs | sed '/^#/ d' | cut -f1 -d ' ' | grep -w ${NAME}_${PYTHON_VERSION})" ]; then
	tput setaf 1; echo "** Create conda local environment: ${NAME}_${PYTHON_VERSION}"; tput sgr0
	conda create -y --name ${NAME}_${PYTHON_VERSION} python=${PYTHON_VERSION} || exit 1
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

sudo apt-get install -y cmake

#################################################################################################
# check for conda package manager

if hash conda 2>/dev/null
then
    :
else
    tput setaf 1; echo "** Conda not found"; tput sgr0
    exit 1
fi

#################################################################################################
# build SimpleElastix

# the SimpleElastix's SuperBuild uses virtualenv. For the local
# environments we use conda environments
conda install -y virtualenv

# create a local environment for SimpleElastix for current python version
create_conda_local_environment SimpleElastix ${PYTHON_VERSION}

# prepare to install SimpleElastix
tput setaf 1; echo "** Clone or update SimpleElastix code"; tput sgr0
cd ~/Software
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
mkdir -p build_${PYTHON_VERSION}

# build for python 3.6
source activate SimpleElastix_${PYTHON_VERSION} || exit 1
cd ~/Software/SimpleElastix/build_${PYTHON_VERSION}

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
