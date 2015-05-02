# jason2

A Python package for downloading and working with [jason2 altimitry data](http://www.nasa.gov/mission_pages/ostm/main/).
**jason2** includes a command line tool for common use cases.


## Installation

Install via `pip` from github:

```bash
pip install git+https://github.com/gadomski/jason2.git@master
```
**jason2** depends on [netCDF4](https://github.com/Unidata/netcdf4-python), which requires [hdf5](http://www.hdfgroup.org/HDF5) and [netcdf](http://www.unidata.ucar.edu/software/netcdf).
If you run OSX, both are available with [homebrew](http://brew.sh).

```bash
brew install hdf5 netcdf
```

**jason2** was developed on OSX, so it should work out of the box on most \*nix's.
Windows, your mileage my vary.

**jason2** was developed on Python 2.7.9.


## Documentation

Documentation is hosted at http://gadomski.github.io/jason2.
The plain text docs are available in this source tree at `docs/index.md`.


## License

This code is available under the MIT license, see LICENSE.txt.
