"""Command line interface for jason2."""

import argparse
import ConfigParser
import os
import re
import sys

import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D  # pylint: disable=unused-import
import numpy

from jason2.bounds import Bounds
from jason2.pass_ import Pass
from jason2.product import PRODUCTS
from jason2.project import Project
from jason2.utils import str_to_list


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
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    (nrows, ncols) = waveforms.shape
    x = numpy.arange(ncols)
    X, Y = numpy.meshgrid(x, latitudes)
    ax.plot_surface(X, Y, waveforms, cmap=cm.coolwarm, rstride=1, cstride=1,
                    linewidth=0)
    plt.gca().invert_xaxis()
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
    plot_waveforms_parser.set_defaults(func=plot_waveforms)

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    defaults = {
        "min_longitude": None,
        "max_longitude": None,
    }
    config = ConfigParser.ConfigParser(defaults)
    config.read(args.config)
    try:
        products = [PRODUCTS[name] for name in
                    str_to_list(config.get("project", "products"))]
        pass_sections = [section for section in config.sections()
                         if section.startswith("pass-")]
        passes = []
        for section in pass_sections:
            match = re.match(r"pass-(\d+)", section)
            assert match
            minx = config.get(section, "min_longitude")
            maxx = config.get(section, "max_longitude")
            bounds = Bounds(
                miny=config.getfloat(section, "min_latitude"),
                maxy=config.getfloat(section, "max_latitude"),
                minx=(float(minx) if minx is not None else None),
                maxx=(float(maxx) if maxx is not None else None),
            )
            pass_ = Pass(number=int(match.group(1)), bounds=bounds)
            passes.append(pass_)

        project = Project(
            data_directory=config.get("project", "data_directory"),
            email=config.get("project", "email"),
            products=products,
            passes=passes)
    except ConfigParser.Error as err:
        sys.stderr.write("Invalid configuration file: {}\n".format(
            os.path.abspath(args.config)))
        raise err
    args.func(project, args)
