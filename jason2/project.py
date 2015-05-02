from jason2.exceptions import MissingEmail
from jason2.ftp import FtpConnection


class Project(object):
    """Holds project configuration parameters, such as data directory."""

    def __init__(self):
        self.data_directory = "."
        self.email = None
        self.products = []
        self.passes = []
        self.start_cycle = None
        self.end_cycle = None

    def fetch(self, skip_unzipping=False):
        if self.email is None:
            raise MissingEmail("No email provided for fetch")
        with FtpConnection(self.email) as ftp:
            for product in self.products:
                cycle_range = ftp.get_cycle_range(self.start_cycle,
                                                  self.end_cycle)
                for cycle in cycle_range:
                    ftp.fetch(product, cycle, self.passes, self.data_directory,
                              skip_unzipping)
