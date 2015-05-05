"""Connect to and download data from the jason-2 servers."""
import fnmatch
import ftplib
import os
import sys
import zipfile

from jason2.exceptions import ConnectionError
from jason2.utils import mkdir_p, zfill3, get_cycle_range


class FtpConnection(object):
    """An FTP connection to the jason-2 servers.

    Use it like this:

        from jason2.pass_ import Pass
        from jason2.product import PRODUCTS

        pass_ = Pass(195, 33.22, 33.33)
        with FtpConnection("me@example.com", ".", pass_) as ftp:
            ftp.fetch_product(PRODUCTS["sgdr"])

    """

    SERVER = "avisoftp.cnes.fr"
    ROOT_PATH = "/Niveau0/AVISO/pub/jason-2/"

    def __init__(self, email, data_directory, passes, output=sys.stdout):
        self.email = email
        self.data_directory = data_directory
        self.passes = passes
        self.connection = None
        self.output = output

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type_, value, traceback):
        self.close()

    def open(self):
        """Open the FTP connection.

        It is recommended to use the with-as syntax over explicitly opening
        and closing the connection yourself.

        """
        self._inform("Opening FTP connection to {} as {}...".format(self.SERVER,
                                                                    self.email))
        self.connection = ftplib.FTP(self.SERVER)
        self.connection.login("anonymous", self.email)
        self._inform("done\n")

    def is_open(self):
        """Boolean checker on connection status."""
        return self.connection is not None

    def close(self):
        """Close the FTP connection.

        Again, use the with-as syntax over explicit open-close.

        """
        self._inform("Closing FTP connection...")
        self.connection.close()
        self.connection = None
        self._inform("done\n")

    def fetch_product(self, product, skip_unzipping=False, overwrite=False):
        """Fetch all cycles for a given product.

        The passes of interest are provided to the Ftp connection on
        construction.

        """
        self._assert_connected()
        for cycle in self._get_cycle_range(product):
            cycle_str = "cycle_{}".format(zfill3(cycle))
            self.connection.cwd(os.path.join(self.ROOT_PATH,
                                             product.directory_name,
                                             cycle_str))
            for pass_ in self.passes:
                filenames = fnmatch.filter(self.connection.nlst(),
                                           product.get_glob(cycle, pass_))
                if len(filenames) == 0:
                    self._inform("WARNING: no {} product for "
                                 "cycle {}, pass {}\n".format(
                                     product.name, cycle, pass_.number))
                    continue
                if len(filenames) > 1:
                    raise ConnectionError("Too many matching products")
                filename = filenames[0]
                outfile = os.path.join(self.data_directory,
                                       product.directory_name,
                                       cycle_str,
                                       filename)
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
                if (os.path.splitext(outfile)[1] == ".zip" and
                        not skip_unzipping):
                    self._unzip(outfile)

    def _get_cycle_range(self, product):
        self._assert_connected()
        cycle_directories = self.connection.nlst(
            os.path.join(self.ROOT_PATH, product.directory_name))
        return get_cycle_range(cycle_directories)

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
