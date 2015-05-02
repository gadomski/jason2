import argparse
import ConfigParser
import os
import sys

from jason2 import products
from jason2.project import Project
from jason2.utils import str_to_list


def fetch(project, args):
    project.fetch(args.skip_unzipping, args.overwrite)
    sys.exit(0)


def list_products(project, args):
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
    config = ConfigParser.ConfigParser(defaults={
        "data-directory": None,
        "email": None,
        "products": None,
        "passes": None,
        "start-cycle": None,
        "end-cycle": None,
    })
    config_files = config.read([os.path.abspath("jason2.cfg"),
                                os.path.expanduser("~/.jason2.cfg")])
    if not config.has_section("project"):
        config.add_section("project")

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
    args.func(project, args)
