import errno
import os
import re


def str_to_list(string):
    return [s.strip() for s in string.split(",")]


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def zfill3(integer):
    return str(integer).zfill(3)


def get_cycle_range(directory_names):
    cycles = []
    for cycle_directory in directory_names:
        match = re.match(r"cycle_(\d\d\d)", cycle_directory)
        if not match:
            continue
        cycles.append(int(match.group(1)))
    return cycles
