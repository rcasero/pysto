# Summary

`pysto` are a few miscellaneous processing python functions.

The name is a play of words on "pisto", a Manchego dish made of
tomatoes, onions, courgettes, green and red peppers and olive oil.

# User instructions

## Installing pysto as a user

1. Install the latest pysto PyPI package

        pip install pysto

## Uninstalling pysto

1. Uninstall the package

        pip uninstall pysto

1. If you get the error `pip error: Cannot locate installed-files.txt`, remove pysto manually. For example, if you are in a conda environment

        rm -rf ${CONDA_PREFIX}/lib/python3.6/site-packages/pysto*

# Developer instructions

We provide scripts `install_dependencies.sh` and `build_SimpleElastix.sh` to help install necessary software, and a `Makefile` to simplify testing and releasing.

## Installing pysto as a developer

1. If you want to develop code for pysto, instead of installing the PyPI package, you want to clone the github repository

        git clone https://github.com/rcasero/pysto.git

1. Install the development dependencies (this creates local conda environments `pysto_2.7` and `pysto_3.6`, for python 2.7 and 3.6, respectively and installs several Ubuntu and python packages). There are two options, depending on what SimpleITK you want:
   1. If you are happy with the official SimpleITK package, just run (this is very fast)

           cd pysto
           ./install_dependencies.sh

   1. If you prefer [SimpleElastix](https://simpleelastix.github.io/) (an extension of [SimpleITK](http://www.simpleitk.org/) with [elastix registration software](http://elastix.isi.uu.nl/))

           cd pysto
           ./install_dependencies.sh SimpleElastix

1. Install the pysto code to one or both of the local environments

        conda activate pysto_2.7
        pip install --upgrade .
        
        conda activate pysto_3.6
        pip install --upgrade .

1. You need to have a local file `~/.pypirc` (replace `<the password>`
by the password). This will be used by `twine` to release packages to PyPI

        [distutils]
        index-servers =
          pypi
          pypitest
        
        [pypi]
        username=rcasero
        password=<the password>
        
        [pypitest]
        repository = https://test.pypi.org/legacy/
        username=rcasero
        password=<the password>

1. Protect the file so that it can be read only by you

        chmod 600 ~/.pypirc

## Uninstalling pysto as a developer

1. Delete the conda local environments (this will delete all the python packages inside the environments)

        source deactivate
        conda remove --name pysto_2.7 --all
        conda remove --name pysto_3.6 --all

## Developing source code for pysto

1. Activate one of the pysto local environments

        cd ~/Software/pysto
        source activate pysto_3.6

1. Launch the development IDE, e.g.

        spyder&

1. In your code, import the pysto modules/functions in the usual way, e.g.

        import pysto.imgproc as pym
        import pysto.imgprocITK as pymITK
        [...]
        imf = pym.imfuse(im1, im2)
        pymITK.imshow(im3)
        
1. While developing, you can run all tests (both for python 2.7 and
3.6) from the command line with

        make test

## Making a new release (to GitHub and PyPI)

1. We assume that you have made some changes to the code, and commit/pushed them to the GitHub repository.

1. Update `version` and `download_url` in `setup.py` with new release number. If something else has changed in the project, update other relevant fields in `setup.py`.

        setup(
            ...
            version='1.0.0',
            download_url='https://github.com/rcasero/pysto/archive/1.0.0.tar.gz',
            ...
        )

1. Update `ChangeLog.md` with the main changes to this release, in markdown format.

1. Commit and push all changes to the repository.

1. Make a test package. (This will also tag the release in github, create the test package/wheel and upload to the test PyPI server), that you can see in https://test.pypi.org/project/pysto/

        make test-package

1. If everything has gone well, make the release package, that you can see in https://pypi.org/project/pysto/

        make package

1. Go to [pysto GitHub release tags](https://github.com/rcasero/pysto/tags), click on "Edit release notes" and copy and paste the new entry from the `ChangeLog.md`
