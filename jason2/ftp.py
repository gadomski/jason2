import fnmatch
import ftplib
import os
import sys

from jason2.exceptions import ConnectionError
from jason2.utils import mkdir_p


def zfill3(integer):
    return str(integer).zfill(3)


def jason2_glob(product, cycle, pass_):
    # FIXME this is way too dumb
    if product == "gdr_d":
        product_type = "N"
    elif product == "sgdr_d":
        product_type = "S"
    cycle_str = zfill3(cycle)
    pass_str = zfill3(pass_)
    # FIXME also way too dumb
    extension = ".nc" if product == "gdr_d" else ".zip"
    return "JA2_GP{}_2PdP{}_{}_*{}".format(product_type, cycle_str, pass_str,
                                           extension)


class FtpConnection(object):

    SERVER = "avisoftp.cnes.fr"
    ROOT_PATH = "/Niveau0/AVISO/pub/jason-2/"

    def __init__(self, email, output=sys.stdout):
        self.email = email
        self.connection = None
        self.output = output

    def __enter__(self):
        self._inform("Opening FTP connection to {} as {}...".format(self.SERVER,
                                                                    self.email))
        self.connection = ftplib.FTP(self.SERVER)
        self.connection.login("anonymous", self.email)
        self._inform("done\n")
        return self

    def __exit__(self, type_, value, traceback):
        self._inform("Closing FTP connection...")
        self.connection.close()
        self.connection = None
        self._inform("done\n")

    def fetch(self, product, cycle, passes, data_directory):
        if self.connection is None:
            raise ConnectionError("Not connected to FTP server")
        cycle_str = "cycle_{}".format(zfill3(cycle))
        self.connection.cwd(os.path.join(self.ROOT_PATH, product,
                                         cycle_str))
        for pass_ in passes:
            glob = jason2_glob(product, cycle, pass_)
            filenames = fnmatch.filter(self.connection.nlst(), glob)
            assert len(filenames) == 1
            filename = filenames[0]
            outfile = os.path.join(data_directory, product, cycle_str,
                                   filename)
            mkdir_p(os.path.dirname(outfile))
            self._inform("Downloading {}...".format(filename))
            self.connection.retrbinary("RETR {}".format(filename),
                                       open(outfile, "wb").write)
            self._inform("done\n")

    def _inform(self, message):
        self.output.write(message)
        self.output.flush()
