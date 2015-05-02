"""Downloading and analyzing jason2 altimitry data.

http://www.nasa.gov/mission_pages/ostm/main/#.VT5JxK1Viko
"""

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md")) as f:
    long_description = f.read()


setup(
    name="jason2",
    version="0.0.1",
    description="Download and analyze jason2 altimitry data",
    long_description=long_description,
    url="https://github.com/gadomski/jason2",
    author="Pete Gadomski",
    author_email="pete.gadomski@gmail.com",
    license="MIT",

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
    ],

    keywords="jason2 altimitry",
    packages=find_packages(),
    install_requires=["matplotlib", "netCDF4", "numpy"],

    entry_points={
        "console_scripts": [
            "jason2=jason2.cli:main",
        ],
    },
)
