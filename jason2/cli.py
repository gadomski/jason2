import argparse
import csv
import sys

import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import numpy

from jason2 import products
from jason2.project import Project
from jason2.utils import str_to_list


def fetch(project, args):
    project.fetch(args.skip_unzipping, args.overwrite)
    sys.exit(0)


def ice_heights(project, args):
    product = products[args.product]
    [datetimes, heights] = \
        project.get_ice_heights(product, args.min_latitude, args.max_latitude)
    writer = csv.writer(sys.stdout)
    writer.writerow(["Datetime", "Ice height"])
    for datetime, height in zip(datetimes, heights):
        writer.writerow([datetime, height])


def list_products(*_):
    for name, product in products.iteritems():
        namestr = "Name: " + name
        print
        print namestr
        print "-" * len(namestr)
        print " family = " + product.family
        print "   type = " + product.type_
        print "version = " + product.version
        print " zipped = " + str(product.zipped)
        print
    sys.exit(0)


def plot_waveforms(project, args):
    waveforms, latitudes = project.get_waveforms(args.cycle)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    (nrows, ncols) = waveforms.shape
    x = numpy.arange(ncols)
    X, Y = numpy.meshgrid(x, latitudes)
    ax.plot_surface(X, Y, waveforms, cmap=cm.coolwarm, rstride=1, cstride=1,
                    linewidth=0)
    plt.show()


def show_config(project, args):
    if project.data_directory is None:
        print "Invalid configuration detected, data directory is None."
        print "Populate jason.cfg in the current working directory to " \
              "set configuration parameters."
        sys.exit(1)
    print
    print "Project configuration"
    print "---------------------"
    print "  config files: " + ", ".join(args.config_files)
    print "data directory: " + project.data_directory
    print "         email: " + project.email
    print "      products: " + ", ".join(product.name for product in
                                         project.products)
    print "        passes: " + ", ".join(str(pass_) for pass_ in
                                         project.passes)
    if project.start_cycle:
        print "   start cycle: " + str(project.start_cycle)
    if project.end_cycle:
        print "     end cycle: " + str(project.end_cycle)
    sys.exit(0)


def parse_args():
    config, config_files = Project.read_config()

    parser = argparse.ArgumentParser(description="Download and analyze "
                                     "Jason2 data. Most command line arguments "
                                     "can also be specified in a configuration "
                                     "file (jason2.cfg or ~/.jason2.cfg).")
    parser.add_argument("-d", "--data-directory",
                        default=config.get("project", "data-directory"),
                        help="The root directory for raw jason2 data")
    parser.add_argument("-e", "--email",
                        default=config.get("project", "email"),
                        help="Email address to identify you when downloading "
                             "data")
    parser.add_argument("-p", "--products",
                        default=config.get("project", "products"),
                        help="A comma-delimted list of product names")
    parser.add_argument("-t", "--passes",
                        default=config.get("project", "passes"),
                        help="A comma-delimted list of pass numbers")
    parser.add_argument("--start-cycle", type=int,
                        default=config.get("project", "start-cycle"),
                        help="The first cycle to download")
    parser.add_argument("--end-cycle", type=int,
                        default=config.get("project", "end-cycle"),
                        help="The last cycle to download")
    parser.add_argument("--min-latitude", type=float,
                        default=config.get("project", "min-latitude"),
                        help="Minimum latitude in decimal degrees")
    parser.add_argument("--max-latitude", type=float,
                        default=config.get("project", "max-latitude"),
                        help="Maximum latitude in decimal degrees")
    parser.add_argument("--min-longitude", type=float,
                        default=config.get("project", "min-longitude"),
                        help="Minimum longitude in decimal degrees")
    parser.add_argument("--max-longitude", type=float,
                        default=config.get("project", "max-longitude"),
                        help="Maximum longitude in decimal degrees")

    subparsers = parser.add_subparsers()

    fetch_parser = subparsers.add_parser("fetch",
                                         help="Fetch jason2 data via FTP")
    fetch_parser.add_argument("--overwrite", action="store_true",
                              help="Re-download files even if they already "
                                   "exist in the data directory")
    fetch_parser.add_argument("--skip-unzipping", action="store_true",
                              help="Do not unzip sgdr files")
    fetch_parser.set_defaults(func=fetch)

    ice_heights_parser = subparsers.add_parser("ice-heights",
                                               help="Calculate the ice height "
                                               "timeseries between two "
                                               "latitudes")
    ice_heights_parser.add_argument(
        "product", help="Name of the product to use for heights")
    ice_heights_parser.set_defaults(func=ice_heights)

    list_products_parser = subparsers.add_parser("list-products",
                                                 help="List supported jason2 "
                                                      "products")
    list_products_parser.set_defaults(func=list_products)

    config_parser = subparsers.add_parser("config",
                                          help="Display configuration "
                                               "parameters")
    config_parser.set_defaults(func=show_config)

    plot_waveforms_parser = subparsers.add_parser("plot-waveforms",
                                                  help="Plot sgdr waveforms.")
    plot_waveforms_parser.add_argument("cycle", type=int,
                                       help="The cycle to plot")
    plot_waveforms_parser.set_defaults(func=plot_waveforms)

    args = parser.parse_args()
    args.config_files = config_files
    return args


def main():
    args = parse_args()
    project = Project()
    project.data_directory = args.data_directory
    project.email = args.email
    if args.products is None:
        project.products = []
    else:
        project.products = [products[product_name] for product_name in
                            str_to_list(args.products)]
    if args.passes is None:
        project.passes = []
    else:
        project.passes = [int(pass_) for pass_ in str_to_list(args.passes)]
    project.start_cycle = args.start_cycle
    project.end_cycle = args.end_cycle
    project.min_latitude = args.min_latitude
    project.max_latitude = args.max_latitude
    project.min_longitude = args.min_longitude
    project.max_longitude = args.max_longitude
    args.func(project, args)
