# Summary

`pysto` are a few miscellaneous processing python functions.

The name is a play of words on "pisto", a Manchego dish made of
tomatoes, onions, courgettes, green and red peppers and olive oil.

# User instructions

## Installing pysto with pip

1. Simply run from your local environment or whole system

        pip install pysto

## Installing pysto from the cloned github repository

1. Clone the pysto repository

        git clone https://github.com/rcasero/pysto.git

1. Activate the local environment of the other project, or you can
also work without a local environment. For example, to activate a
local conda environment called "myproject"

        source activate myproject

1. Install pysto from the pysto root directory (note that if you are
installing it system-wide, you may need to run the command as root)

        cd pysto
        pip install .

## Uninstalling pysto

1. Uninstall the package

        pip uninstall pysto

# Developer instructions

## Install pysto project for development

1. Clone the pysto repository

        git clone https://github.com/rcasero/pysto.git

1. Run `install_dependencies.sh` to install development tools, create
local environments for python 2.7 and 3.6, and install python
dependencies. `pysto` depends on SimpleITK, and there are two options:

    1. Install the official SimpleITK package

            cd pysto
            ./install_dependencies.sh

    1. Build and install SimpleElastix, which is an extension of SimpleITK

            cd pysto
            ./install_dependencies.sh SimpleElastix

## Developing source code for pysto

1. Activate one of the pysto local environments

        source activate pysto_3.6

1. If you are making changes to the code, you want your python
environment to import the code you are working with in
`~/Software/pysto`, not the package installed in your local conda
environment. Thus, add the project's source directory to `PYTHONPATH`

        export PYTHONPATH=~/Software/pysto:$PYTHONPATH

1. Launch the development IDE, e.g.

        spyder&

1. In your code, import the pysto modules/functions in the usual way, e.g.

        import pysto.imgproc as pymg        
        [...]
        imf = pymg.imfuse(im1, im2)
        
1. While developing, you can run all tests (both for python 2.7 and
3.6) from the command line with

        make test

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

## Uninstalling pysto

1. Uninstall the package

        pip uninstall pysto

## Making a new release (to GitHub and PyPI)

We provide a `Makefile` to simplify testing and releasing.

1. Run all tests for python 2.7 and 3.6 to make sure nothing obvious got broken

        make test

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
