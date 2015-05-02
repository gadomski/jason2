import argparse

from jason2.project import Project


def fetch(project, args):
    project.fetch(args.skip_unzipping)


def parse_args():
    parser = argparse.ArgumentParser(description="Work with Jason2 data")

    parser.add_argument("--config", default="jason2.cfg",
                        help="Project configuration file")

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
