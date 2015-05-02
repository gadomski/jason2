# jason2

A python package for downloading and working with [jason2 altimitry data](http://www.nasa.gov/mission_pages/ostm/main/).


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


## Usage

**jason2** provides a command-line script with the same name that contains a few subcommands.
Run `jason2 --help` for information.


## License

This code is available under the MIT license, see LICENSE.txt.
