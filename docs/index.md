# jason2

**jason2** is a Python package for working with [jason2](http://www.nasa.gov/mission_pages/ostm/main/) altimetry data, including a command line tool for common use cases.
For installation instructions and system requirements, see [the project README](https://github.com/gadomski/jason2#readme).


## Structure

**jason2** organizes your work into a `Project`.
A `Project` has many attributes, including:

- a `data_directory`, which will hold all the raw jason-2 data files fetched from the remote server
- a list of `products`, which are specific product types (e.g. gdr, sgdr) that your project is interested in
- a list of `passes`, which are jason-2 passes (a.k.a. tracks) that your project is interested
- and more...

You can see the complete list of project parameters by running `jason2 --help` and looking at the available command line options.
Some of these parameters must be set by you, and others will be filled with sensible defaults.


## Configuration Files

While you could provide project parameters explicitly to each invocation of the command line tool, this quickly gets cumbersome.
To make things easier, project parameters can be stored in configuration files.
**jason2** looks for configuration files in two places:

- a file named `jason2.cfg` in the current working directory
- a file named `~/.jason2.cfg`

This allows you to specify common options (e.g. your email address for FTP fetching) in the user-wide `~/.jason2.cfg`, while specifying options specific to a given project (e.g. pass numbers) in a directory-specific file.

A configuration file looks like this:

```text
[project]
data-directory: build
email: me@example.com
products: gdr, sgdr
passes: 195, 197
end-cycle: 3
```

All options need to go in a `[project]` section.
Lists are specified in a comma-delimited fashion.
Omitted values (e.g. `start-cycle` in the example) are filled with sensible defaults.

Project parameters provided on the command line will override the values in the configuration files.


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

No API documentation is available at this time, please read the source to get a sense of what is going on.
