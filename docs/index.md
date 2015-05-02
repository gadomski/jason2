# jason2

**jason2** is a python package for working with [jason2](http://www.nasa.gov/mission_pages/ostm/main/) altimetry data.
It provides a python API and a command line tool.


## Installation

**jason2** depends on [hdf5](http://www.hdfgroup.org/HDF5) and [netcdf](http://www.unidata.ucar.edu/software/netcdf).
If you are on OSX, install both with [homebrew](http://brew.sh):

```bash
brew install hdf5 netcdf
```

Then install **jason2** with pip:

```bash
pip install git+https://github.com/gadomski/jason2.git@master
```


## Command Line

The **jason2** python package provides a command line tool, called `jason2`, for working with jason-2 data.

### Configuration File

Before using the command line tool you need to set up a jason2 project configuration file.
This file will tell **jason2** which data products, passes, and cycles you are interested in.
By default, **jason2** expects this file to be named `jason2.cfg` in your current working directory; you can specify another path using the `--config` command line option.

```cfg
[project]
data_directory: jason2-data
products: gdr_d, sgdr_d
passes: 195
email: me@example.com
```

Use the following keys to configure your jason-2 project:

- `data_directory`: Top-level path for all downloaded jason-2 data products. If this directory does not exist, `jason2` will create it for you.
- `products`: Comma-separated list of jason-2 data products to download. Use `jason2 list-products` to see a list of all supported products.
- `passes`: Comma-separated list of all passes to download. Other software sometimes uses "tracks" instead of "passes".
- `start_cycle`: Integer indicating the first cycle to download. If not provided, cycle downloads will start at zero.
- `end_cycle`: Integer indicating the last cycle to download. If not provided, all cycles up to the most recent will be downloaded.
- `email`: An email address that will be provided to the FTP server for download tracking.


### Commands

Below is a summary of some of the commands available via the command line tool.
For a complete list and information on command line options, use `jason2 --help` or `jason2 [subcommand] --help`.

* `jason2 fetch` - Download jason2 data via FTP


## API

No API documentation is available at this time, please read the source to get a sense of what is going on.
