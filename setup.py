# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='pysto',
    version='1.1.3',
    download_url = 'https://github.com/rcasero/pysto/archive/1.1.3.tar.gz',
    packages=find_packages(),
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*',
    install_requires=[
        'matplotlib>=2.0',
        'numpy>=1.13',
        'opencv-python>=3.3.0',
    ],
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': ['spyder', 'twine', 'wheel', 'setuptools'],
        'test': ['pytest'],
    },
    description='Miscellaneous image processing functions',
    url='https://github.com/rcasero/pysto',
    author='Ramón Casero',
    author_email='rcasero@gmail.com',
    license='GPL v3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
    ],
    keywords=['image processing', 'bioinformatics'],
)
