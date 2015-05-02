import fnmatch
import ftplib
import os
import re
import sys
import zipfile

from jason2.exceptions import ConnectionError
from jason2.utils import mkdir_p, zfill3


class FtpConnection(object):

    SERVER = "avisoftp.cnes.fr"
    ROOT_PATH = "/Niveau0/AVISO/pub/jason-2/"

    def __init__(self, email, output=sys.stdout):
        self.email = email
        self.connection = None
        self.output = output

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type_, value, traceback):
        self.close()

    def open(self):
        self._inform("Opening FTP connection to {} as {}...".format(self.SERVER,
                                                                    self.email))
        self.connection = ftplib.FTP(self.SERVER)
        self.connection.login("anonymous", self.email)
        self._inform("done\n")

    def is_open(self):
        return self.connection is not None

    def close(self):
        self._inform("Closing FTP connection...")
        self.connection.close()
        self.connection = None
        self._inform("done\n")

    def fetch(self, product, cycle, passes, data_directory,
              skip_unzipping=False, overwrite=False):
        self._assert_connected()
        cycle_str = "cycle_{}".format(zfill3(cycle))
        self.connection.cwd(os.path.join(self.ROOT_PATH, product.directory_name,
                                         cycle_str))
        for pass_ in passes:
            filenames = fnmatch.filter(self.connection.nlst(),
                                       product.get_glob(cycle, pass_))
            assert len(filenames) == 1
            filename = filenames[0]
            outfile = os.path.join(data_directory, product.directory_name,
                                   cycle_str, filename)
            if os.path.exists(outfile) and not overwrite:
                self._inform(
                    "{} already exists on filesystem, skipping.\n".format(
                        filename))
                continue
            mkdir_p(os.path.dirname(outfile))
            self._inform("Downloading {}...".format(filename))
            self.connection.retrbinary("RETR {}".format(filename),
                                       open(outfile, "wb").write)
            self._inform("done\n")
            if os.path.splitext(outfile)[1] == ".zip" and not skip_unzipping:
                self._unzip(outfile)

    def get_cycle_range(self, product, start_cycle, end_cycle):
        self._assert_connected()
        cycle_directories = self.connection.nlst(
            os.path.join(self.ROOT_PATH, product.directory_name))
        cycles = []
        for cycle_directory in cycle_directories:
            match = re.match(r"cycle_(\d\d\d)", cycle_directory)
            if not match:
                continue
            cycles.append(int(match.group(1)))
        if start_cycle is None:
            start_cycle = min(cycles)
        if end_cycle is None:
            end_cycle = min(cycles)
        return [cycle for cycle in cycles if
                start_cycle <= cycle <= end_cycle]

    def _assert_connected(self):
        if self.connection is None:
            raise ConnectionError("Not connected to FTP server")

    def _unzip(self, outfile):
        self._inform("Unzipping {}...".format(outfile))
        with zipfile.ZipFile(outfile, "r") as zfile:
            zfile.extractall(os.path.dirname(outfile))
        self._inform("done\n")

    def _inform(self, message):
        self.output.write(message)
        self.output.flush()
