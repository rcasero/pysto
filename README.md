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

## Releasing a new version of pysto to PyPI

We provide a `Makefile` to simplify testing and releasing.

1. Run tests to make sure nothing obvious got broken

        make test

1. Commit and push all the code that should go in the release to
github.

1. Update `setup.py` with release version, any new dependencies, the
new download URL, changes to the description...

        from setuptools import setup, find_packages
        
        setup(
            name='pysto',
            version='1.0.0',
            download_url = 'https://github.com/rcasero/pysto/archive/1.0.0.tar.gz',
            packages=find_packages(),
            python_requires='>=3.6',
            install_requires=['matplotlib>=2.0','numpy>=1.13','opencv-python>=3.3.0'],
            description='Miscellanea image processing functions',
            url='https://github.com/rcasero/pysto',
            author='Ramón Casero',
            author_email='rcasero@gmail.com',
            license='GPL v3',
        )

1. Update `ChangeLog.md` with the main changes to this release. For example,

        ## v1.0.0
        ### Added
        
        - imgproc.matchHist(): "Modify image intensities to match the
          histogram of a reference image" by
          [rcasero](https://github.com/rcasero)
        - imgproc.imfuse(): "Composite of two images" by
          [rcasero](https://github.com/rcasero)
        - testdata/*.png: Stereo cloud images with ROI masks (left_mask.png,
          left.png, right_mask.png, right.png) by
          [rcasero](https://github.com/rcasero)

1. Tag the release in github, create the package/wheel and upload to the test PyPI server

        make test-package

1. You should be able to see your package in

        https://test.pypi.org/project/pysto/

1. If everything goes well, upload to PyPI Live

        make package

1. You should be able to see your package in

        https://pypi.org/project/pysto/
