from setuptools import setup, find_packages
from pathlib import Path

VERSION = '0.0.5' 
DESCRIPTION = 'Python Package for playing with Simple Vectors passing through a point'

this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / "README.md").read_text()
# Setting up
setup(
        name="SimpleVectors", 
        version=VERSION,
        author="Jonathan Ghodke",
        author_email="Jonathanghodke@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
	long_description_content_type='text/markdown',
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