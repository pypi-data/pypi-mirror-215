#------------------------------------------------------------------------
#
# This is a python install script written for qwiic python package.
#
# Written by  SparkFun Electronics, May 2019
#
# This python library supports the SparkFun Electroncis qwiic
# ecosystem, providing an plaform indepenant interface to the
# I2C bus.
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
#==================================================================================
# Copyright (c) 2019 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#==================================================================================

from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from os import path
import os
import io

here = path.abspath(path.dirname(__file__))

# get the log description
with io.open(path.join(here, "DESCRIPTION.rst"), encoding="utf-8") as f:
    long_description = f.read()

# Build up our list of dependant modules.
#
setup_requires = ['pyserial==3.4']

# Use the dir names of the submodules in the ./qwiic/drives directory
#for daDriver in sub_mods:
#    setup_requires.append('%s' % (daDriver.replace('_','-')))

setup(
    name='pyLauda',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # http://packaging.python.org/en/latest/tutorial.html#version
    version='1.0.3',

    description='German Aerospace Center',
    long_description=long_description,

    # The project's main homepage.
    url='http://gitsrv.intra.dlr.de/nieh_ko/PyLauda',

    # Author details
    author='German Aerospace Center',
    author_email='konstantin.niehaus@dlr.de',

    install_requires=setup_requires,
    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Hardware",
        "Topic :: System :: Hardware :: Hardware Drivers",
        "Topic :: Scientific/Engineering",
    ],

    # What does your project relate to?
    keywords='driver, rs232, rs485, temperature control',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['pyLauda'],
    package_data={ "pyLauda" : ['']},

)
