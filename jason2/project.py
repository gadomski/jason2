import ConfigParser

from jason2.ftp import FtpConnection
from jason2.system import FIRST_CYCLE, LAST_CYCLE


class Project(object):
    """Holds project configuration parameters, such as data directory."""

    def __init__(self, data_directory, products, passes, email,
                 start_cycle=FIRST_CYCLE, end_cycle=LAST_CYCLE):
        self.data_directory = data_directory
        self.products = products
        self.passes = passes
        self.email = email
        self.start_cycle = start_cycle
        self.end_cycle = end_cycle

    def fetch(self, skip_unzipping=False):
        with FtpConnection(self.email) as ftp:
            for product in self.products:
                for cycle in range(self.start_cycle, self.end_cycle + 1):
                    ftp.fetch(product, cycle, self.passes, self.data_directory,
                              skip_unzipping)
