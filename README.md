# pysto

Some image processing python functions.

From "pisto manchego", a messy Spanish dish made of tomatoes, onions, courgettes, green and red peppers and olive oil.

# Install

1. Install python environment

        sudo apt-get install python3 python3-dev pip3 spyder3

1. Clone the project

        git clone https://github.com/rcasero/pysto.git

1. Install the pysto package for your local user

        cd pysto
        pip3 install . --user
        
# Uninstall

1. Uninstall the package

       cd pysto
       sudo pip3 uninstall pysto
       
# Use

1. In your python file, import the module you want to use (currently, only `imgproc` available), possibly giving it a shorthand

       import pysto.imgproc as pysimg
       
1. Then, you can call the function

       im_matched = pysimg.matchHist(imref, im, maskref=maskref, mask=mask)
