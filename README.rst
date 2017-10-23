Summary
=======

``pysto`` are a few miscellaneous processing python functions.

The name is a play of words on "pisto", a Manchego dish made of
tomatoes, onions, courgettes, green and red peppers and olive oil.

User instructions
=================

Installing pysto with pip
-------------------------

1. Simply run from your local environment or whole system

   pip install pysto

Installing pysto from the cloned github repository
--------------------------------------------------

1. Clone the pysto repository

   git clone https://github.com/rcasero/pysto.git

2. Activate the local environment of the other project, or you can also
   work without a local environment. For example, to activate a local
   conda environment called "myproject"

   source activate myproject

3. Install pysto from the pysto root directory (note that if you are
   installing it system-wide, you may need to run the command as root)

   cd pysto pip install .

Uninstalling pysto
------------------

1. Uninstall the package

   pip uninstall pysto

Developer instructions
======================

Install pysto project for development
-------------------------------------

1. Clone the pysto repository

   git clone https://github.com/rcasero/pysto.git

2. Run ``install_dependencies.sh`` so it creates local environments for
   python 2.7 and 3.6, and installs python dependencies and development
   tools

   cd pysto ./install\_dependencies.sh

Developing source code for pysto
--------------------------------

1. Activate one of the pysto local environments

   source activate pysto\_3.6

2. If you are making changes to the code, you want your python
   environment to import the code you are working with in
   ``~/Software/pysto``, not the package installed in your local conda
   environment. Thus, add the project's source directory to
   ``PYTHONPATH``

   export PYTHONPATH=~/Software/pysto:$PYTHONPATH

3. Launch the development IDE, e.g.

   spyder&

4. In your code, import the pysto modules/functions in the usual way,
   e.g.

   | import pysto.imgproc as pymg
   | [...] imf = pymg.imfuse(im1, im2)

5. While developing, you can run all tests (both for python 2.7 and 3.6)
   from the command line with

   make test

6. You need to have a local file ``~/.pypirc`` (replace
   ``<the password>`` by the password). This will be used by ``twine``
   to release packages to PyPI

   [distutils] index-servers = pypi pypitest

   [pypi] username=rcasero password=

   [pypitest] repository = https://test.pypi.org/legacy/
   username=rcasero password=

7. Protect the file so that it can be read only by you

   chmod 600 ~/.pypirc

Uninstalling pysto
------------------

1. Uninstall the package

   pip uninstall pysto

Releasing a new version of pysto to PyPI
----------------------------------------

We provide a ``Makefile`` to simplify testing and releasing.

1. Run tests to make sure nothing obvious got broken

   make test

2. Commit and push all the code that should go in the release to github.

3. Update ``setup.py`` with release version, any new dependencies, the
   new download URL, changes to the description...

   from setuptools import setup, find\_packages

   setup( name='pysto', version='1.0.0', download\_url =
   'https://github.com/rcasero/pysto/archive/1.0.0.tar.gz',
   packages=find\_packages(), python\_requires='>=3.6',
   install\_requires=['matplotlib>=2.0','numpy>=1.13','opencv-python>=3.3.0'],
   description='Miscellanea image processing functions',
   url='https://github.com/rcasero/pysto', author='Ramón Casero',
   author\_email='rcasero@gmail.com', license='GPL v3', )

4. Update ``ChangeLog.md`` with the main changes to this release. For
   example,

   ## v1.0.0 ### Added

   -  imgproc.matchHist(): "Modify image intensities to match the
      histogram of a reference image" by
      `rcasero <https://github.com/rcasero>`__
   -  imgproc.imfuse(): "Composite of two images" by
      `rcasero <https://github.com/rcasero>`__
   -  testdata/\*.png: Stereo cloud images with ROI masks
      (left\_mask.png, left.png, right\_mask.png, right.png) by
      `rcasero <https://github.com/rcasero>`__

5. Tag the release in github, create the package/wheel and upload to the
   test PyPI server

   make test-package

6. You should be able to see your package in

   https://test.pypi.org/project/pysto/

7. If everything goes well, upload to PyPI Live

   make package

8. You should be able to see your package in

   https://pypi.org/project/pysto/