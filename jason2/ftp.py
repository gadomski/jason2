import ftplib
import os

from jason2.exceptions import ConnectionError
from jason2.utils import get_jason2_filename


class FtpConnection(object):

    SERVER = "avisoftp.cnes.fr"
    ROOT_PATH = "/Niveau0/AVISO/pub/jason2/"

    def __init__(self, email):
        self.email = email
        self.connection = None

    def __enter__(self):
        self.connection = ftplib.FTP(self.server)
        self.connection.login("anonymous", self.email)
        return self

    def __exit__(self):
        self.connection.close()
        self.connection = None

    def fetch(self, product, cycle, tracks, data_directory):
        if self.connection is None:
            raise ConnectionError("Not connected to FTP server")
        cycle_str = str(cycle).zfill(3)
        self.connection.cwd(os.path.join(self.ROOT_PATH, product,
                                         cycle_str))
        for track in tracks:
            filename = get_jason2_filename(product, cycle, track)
            outfile = os.path.join(data_directory, product, cycle_str,
                                   filename)
            self.connection.retrbinary("RETR {}".format(filename),
                                       open(outfile, "wb").write)
