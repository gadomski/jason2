import argparse

from jason2.project import Project


def fetch(project):
    project.fetch()


def parse_args():
    parser = argparse.ArgumentParser(description="Work with Jason2 data")

    parser.add_argument("--configfile", default="jason2.cfg",
                        help="Project configuration file")

    subparsers = parser.add_subparsers()

    fetch_parser = subparsers.add_parser("fetch",
                                         help="Fetch jason2 data via FTP")
    fetch_parser.set_defaults(func=fetch)

    return parser.parse_args()


def main():
    args = parse_args()
    project = Project.from_config(args.configfile)
    args.func(project)
