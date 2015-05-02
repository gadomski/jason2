import errno
import os


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
