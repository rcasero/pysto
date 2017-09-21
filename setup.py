# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='pysto',
    version='1.1.1',
    packages=find_packages(),

    python_requires='>=3.6',
    install_requires=['matplotlib>=2.0','numpy>=1.13','opencv-python>=3.3.0'],
    
    description='Miscellaneous image processing functions',
    url='https://github.com/rcasero/pysto',
    download_url = 'https://github.com/rcasero/pysto/archive/1.1.1.tar.gz',
    author='Ramón Casero',
    author_email='rcasero@gmail.com',
    license='GPL v3',
)
