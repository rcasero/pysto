from setuptools import setup, find_packages

setup(
    name='pysto',
    version='0.1',
    packages=find_packages(),

    python_requires='>=3.6',
    install_requires=['matplotlib>=2.0','numpy>=1.13','opencv-python>=3.3.0'],
    
    description='Pysto image processing functions',
    url='https://github.com/rcasero/pysto',
    author='Ramon Casero',
    author_email='rcasero@gmail.com',
    license='GPL v3',
)
