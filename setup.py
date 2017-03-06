from setuptools import setup, find_packages

setup(
    name='pysto',
    version='0.1',
    packages=find_packages(),

    python_requires='>=3.5',
    install_requires=['matplotlib>=1.5','numpy>=1.11','scipy>=0.17'],
    
    description='Pysto image processing functions',
    url='https://github.com/rcasero/pysto',
    author='Ramon Casero',
    author_email='rcasero@gmail.com',
    license='GPL v3',
)
