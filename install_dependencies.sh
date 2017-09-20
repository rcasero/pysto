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

# conda local environment
if [ -z "$(conda info --envs | sed '/^#/ d' | cut -f1 -d ' ' | grep -w pysto)" ]; then
    tput setaf 1; echo "** Create conda local environment: pysto"; tput sgr0
    conda create -y --name pysto python=3
else
    tput setaf 1; echo "** Conda local environment already exists (...skipping): pysto"; tput sgr0
fi

# switch to pysto local environment
tput setaf 1; echo "** Switching to local environment: pysto"; tput sgr0
source activate pysto

# install pysto code and dependencies
tput setaf 1; echo "** Install pysto code and dependencies in local environment"; tput sgr0
pip install .

# install development tools
tput setaf 1; echo "** Install development tools in local environment"; tput sgr0
conda install -y spyder pytest
