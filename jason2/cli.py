import argparse

from jason2.project import Project


def parse_args():
    parser = argparse.ArgumentParser(description="Work with Jason2 data")

    parser.add_argument("--configfile", default="jason2.cfg",
                        help="Project configuration file")

    return parser.parse_args()


def main():
    args = parse_args()
    project = Project.from_config(args.configfile)
    print project.products
