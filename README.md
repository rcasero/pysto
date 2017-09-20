# pysto

Some image processing python functions.

The name is a play of words on "pisto", a Manchego dish made of tomatoes, onions, courgettes, green and red peppers and olive oil.

# Install pysto project for development

1. Clone the project

        git clone https://github.com/rcasero/pysto.git

1. Create local environment called `pysto`, and install in it the
pysto modules, python dependencies and development tools

        cd pysto
	./install_dependencies.sh

1. Activate `pysto` local environment

        source activate pysto

1. Run project tests

        pytest tests/

# Installing pysto for other projects

1. Activate the local environment of the other project, or you can also work without a local environment.

1. Install pysto from the pysto root directory (note that if you are
installing it system-wide, you may need to run the command as root)

        cd ~/Software/pysto
	pip install .

# Developing source code for pysto

1. If you are making changes to the code, you probably don't want to have to reinstall the modules to check every change. Instead, add the project source directory to the `PYTHONPATH`

	export PYTHONPATH=~/Software/pysto:$PYTHONPATH

1. Launch the development IDE, e.g.

	spyder&

1. In your code, import the pysto modules/functions as e.g.

	import pysto.imgproc as pymg
        [...]
	imf = pymg.imfuse(im1, im2)
        
# Uninstall

1. Uninstall the package

       pip uninstall pysto
