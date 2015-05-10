"""Command line interface for jason2."""

import argparse
import sys

import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D  # pylint: disable=unused-import
import numpy

from jason2.product import PRODUCTS
from jason2.project import Project


def fetch(project, args):
    project.fetch(args.skip_unzipping, args.overwrite)
    sys.exit(0)


def list_products(*_):
    for name, product in PRODUCTS.iteritems():
        namestr = "Name: " + name
        print
        print namestr
        print "-" * len(namestr)
        print " family: " + product.family
        print "   type: " + product.type_
        print "version: " + product.version
        print " zipped: " + str(product.zipped)
        print
    sys.exit(0)


def plot_waveforms(project, args):
    waveforms, latitudes = project.get_waveforms(args.cycle,
                                                 pass_number=args.pass_number,
                                                 clip=args.clip)
    (nrows, ncols) = waveforms.shape
    x = numpy.arange(ncols)
    X, Y = numpy.meshgrid(x, latitudes)
    fig = plt.figure()
    if args.raster:
        ax = fig.add_subplot(111)
        ax.pcolormesh(X, Y, waveforms, cmap=cm.coolwarm)
        plt.axis([0, ncols, latitudes.min(), latitudes.max()])
    else:
        ax = fig.add_subplot(111, projection="3d")
        ax.plot_surface(X, Y, waveforms, cmap=cm.coolwarm, rstride=1, cstride=1,
                        linewidth=0)
    if args.invertx:
        fig.gca().invert_xaxis()

    if args.save:
        plt.savefig(args.save, dpi=args.dpi, transparent=True)
    else:
        plt.show()


def plot_cycle(project, args):
    heights = project.get_cycle_heights(args.cycle, args.pass_number)
    plt.plot(heights.data["ocean"].latitudes,
             heights.data["ocean"].data, "bo", label="Ocean")
    plt.plot(heights.data["ice"].latitudes,
             heights.data["ice"].data, "c^", label="Ice")
    plt.plot(heights.data["threshold_50"].latitudes,
             heights.data["threshold_50"].data, "g+", label="Threshold 50%")
    plt.title("Altimeter ellipsoidal heights for cycle {}".format(args.cycle))
    plt.xlabel("Latitude")
    plt.ylabel("Ellipsoidal height(m)")
    plt.legend()
    plt.show()


def show_config(project, args):
    print
    print "Project configuration"
    print "-" * 79
    print "   config file: " + args.config
    print "data directory: " + project.data_directory
    print "         email: " + project.email
    print "      products: " + ", ".join(product.name for product in
                                         project.products)
    for pass_ in project.passes:
        print
        print "Pass " + str(pass_.number)
        print "-" * 40
        print " min_latitude: {}".format(pass_.bounds.miny)
        print " max_latitude: {}".format(pass_.bounds.maxy)
        print "min_longitude: {}".format(pass_.bounds.minx)
        print "max_longitude: {}".format(pass_.bounds.maxy)

    sys.exit(0)


def parse_args():
    parser = argparse.ArgumentParser(description="Download and analyze "
                                     "Jason2 data.")
    parser.add_argument("--config", default="jason2.cfg",
                        help="Path to the configuration file. Defaults to "
                             "`jason2.cfg` in your current working directory.")

    subparsers = parser.add_subparsers()

    fetch_parser = subparsers.add_parser("fetch",
                                         help="Fetch jason2 data via FTP")
    fetch_parser.add_argument("--overwrite", action="store_true",
                              help="Re-download files even if they already "
                                   "exist in the data directory")
    fetch_parser.add_argument("--skip-unzipping", action="store_true",
                              help="Do not unzip sgdr files")
    fetch_parser.set_defaults(func=fetch)

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
    plot_waveforms_parser.add_argument("--pass", dest="pass_number", type=int,
                                       default=None,
                                       help="The pass number to plot. "
                                       "Only required if your project uses "
                                       "more than one pass.")
    plot_waveforms_parser.add_argument("--clip", type=float,
                                       default=None,
                                       help="Crop waveform intensity values so "
                                       "very large values don't dominate the "
                                       "plot")
    plot_waveforms_parser.add_argument("--invertx", action="store_true",
                                       help="Invert the x axis")
    plot_waveforms_parser.add_argument("--raster", action="store_true",
                                       help="Show a raster instead of a pretty "
                                       "3D plot")
    plot_waveforms_parser.add_argument("--save", default=None,
                                       help="Save that plot to the given file")
    plot_waveforms_parser.add_argument("--dpi", default=300, type=int,
                                       help="DPI when saving")
    plot_waveforms_parser.set_defaults(func=plot_waveforms)

    plot_cycle_parser = subparsers.add_parser("plot-cycle",
                                              help="Plot range values for a "
                                              "single cycle")
    plot_cycle_parser.add_argument("cycle", type=int,
                                   help="The cycle to plot")
    plot_cycle_parser.add_argument("--pass", dest="pass_number", type=int,
                                   default=None,
                                   help="The pass number to plot. "
                                   "Only required if your project uses "
                                   "more than one pass.")
    plot_cycle_parser.set_defaults(func=plot_cycle)

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    project = Project.from_config(args.config)
    args.func(project, args)
