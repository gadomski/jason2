import argparse
import ConfigParser
import os

from jason2.project import Project


def fetch(project, args):
    project.fetch(args.skip_unzipping)


def parse_args():
    config = ConfigParser.ConfigParser(defaults={
        "data-directory": None,
        "email": None,
        "products": [],
        "passes": [],
        "start-cycle": None,
        "end-cycle": None,
    })
    config.read(["jason2.cfg", os.path.expanduser("~/.jason2.cfg")])
    if not config.has_section("project"):
        config.add_section("project")

    parser = argparse.ArgumentParser(description="Download and analyze "
                                     "Jason2 data")
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
    parser.add_argument("--start-cycle",
                        default=config.get("project", "start-cycle"),
                        help="The first cycle to download")
    parser.add_argument("--end-cycle",
                        default=config.get("project", "end-cycle"),
                        help="The last cycle to download")

    subparsers = parser.add_subparsers()

    fetch_parser = subparsers.add_parser("fetch",
                                         help="Fetch jason2 data via FTP")
    fetch_parser.add_argument("--skip-unzipping", action="store_true",
                              help="Do not unzip sgdr files")
    fetch_parser.set_defaults(func=fetch)

    return parser.parse_args()


def main():
    args = parse_args()
    project = Project.from_config(args.config)
    args.func(project, args)
