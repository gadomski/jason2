# jason2

**jason2** is a Python package for working with [jason2](http://www.nasa.gov/mission_pages/ostm/main/) altimetry data, including a command line tool for common use cases.
For installation instructions and system requirements, see [the project README](https://github.com/gadomski/jason2#readme).


## Structure

**jason2** organizes your work into a `Project`.
A `Project` has many attributes, including:

- a `data_directory`, which will hold all the raw jason-2 data files fetched from the remote server
- a list of `products`, which are specific product types (e.g. gdr, sgdr) that your project is interested in
- a list of `passes`, which are jason-2 passes (a.k.a. tracks) that your project is interested in
- and more...


## Configuration Files

**jason2** looks for project configuration files in a file named `jason2.cfg` in your current working directory.
You can specify another location for your configuration file with the `--config` command line option.

A configuration file looks like this:

```text
[project]
data_directory: build
email: me@example.com
products: gdr, sgdr

[pass-195]
min_latitude = 32.98
max_latitude = 33.23
min_longitude = 244.23
max_longitude = 244.63

[pass-197]
min_latitude = 32.98
max_latitude = 33.23
```

The list of products is specified in a comma-delimited fashion.
All latitudes and longitudes are provided in decimal degrees, and the longitude values are optional.


## Command Line Usage

Like many tools, `jason2` is organized into subtools; each subtool takes a specific action or actions, or provides certain output.
To see the top-level `jason2` help, including the list of subtools, run:

```bash
jason2 --help
```

For help on a specific subtool, run:

```bash
jason2 [subtool name] --help
```

e.g. for help with the `fetch` subtool:

```bash
jason2 fetch --help
```

To print some information about your current project configuration to stdout, run:

```bash
jason2 config
```

There are many more subtools available, use `jason2 --help` to find out more.


## API

No API documentation is available at this time, please read [the source](https://github.com/gadomski/jason2) to get a sense of what is going on.
