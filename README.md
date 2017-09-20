# Summary

`pysto` are a few miscellaneous processing python functions.

The name is a play of words on "pisto", a Manchego dish made of tomatoes, onions, courgettes, green and red peppers and olive oil.

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

1. Create local environment called `pysto`, and install in it the
pysto modules, python dependencies and development tools

        cd pysto
	./install_dependencies.sh

1. Activate `pysto` local environment

        source activate pysto

1. Run project tests

        pytest tests/

## Developing source code for pysto

1. If you are making changes to the code, you probably don't want to
have to reinstall the modules to check every change. Instead, add the
project source directory to the `PYTHONPATH`

       export PYTHONPATH=~/Software/pysto:$PYTHONPATH

1. Launch the development IDE, e.g.

       spyder&

1. In your code, import the pysto modules/functions as e.g.

       import pysto.imgproc as pymg        
       [...]
       imf = pymg.imfuse(im1, im2)
        
## Uninstalling pysto

1. Uninstall the package

       pip uninstall pysto

## Uploading a new release of pysto to PyPI

(Some instructions derived from Peter Downs' ["How to submit a package
to PyPI"](http://peterdowns.com/posts/first-time-with-pypi.html).)

1. Run tests to make sure nothing obvious got broken

       pytest tests/

1. Update `setup.py` with release version, any new dependencies, the
new download URL, etc.. For example,

       from setuptools import setup, find_packages
       
       setup(
           name='pysto',
           version='1.0.0',
           packages=find_packages(),
       
           python_requires='>=3.6',
           install_requires=['matplotlib>=2.0','numpy>=1.13','opencv-python>=3.3.0'],
           
           description='Miscellanea image processing functions',
           url='https://github.com/rcasero/pysto',
           download_url = 'https://github.com/rcasero/pysto/archive/1.0.0.tar.gz',
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

1. You need to have a local file `~/.pypirc` (replace `<the password>` by the password)

       [distutils]
       index-servers =
         pypi
         pypitest
       
       [pypi]
       username=rcasero
       password=<the password>
       
       [pypitest]
       username=rcasero
       password=<the password>

1. Protect the file so that it can be read only by you

       chmod 600 ~/.pypirc

1. Create a source distribution and a wheel (built package)

       python setup.py sdist bdist_wheel

1. Upload your package to PyPI Test

       twine upload --repository testpypi dist/*

1. You should be able to see your package in

       https://test.pypi.org/project/pysto/

1. If everything goes well, upload to PyPI Live

       twine upload --repository pypi dist/*

1. You should be able to see your package in

       https://pypi.python.org/pypi
