from setuptools import setup, find_packages

VERSION = '0.0.4' 
DESCRIPTION = 'Python Package for playing with Simple Vectors passing through a point'
LONG_DESCRIPTION = 'Very easy to use module which provides to play with vectors using their magnitude and direction (angle) w.r.t x-axis, also all the vectors which will be added are assumed to be passing through the same line'

# Setting up
setup(
        name="SimpleVectors", 
        version=VERSION,
        author="Jonathan Ghodke",
        author_email="Jonathanghodke@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['numpy', 'matplotlib'],
        keywords=['python', 'Vectors', 'vectors', 'simple vectors'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)