import ConfigParser

from jason2.ftp import FtpConnection
from jason2.system import FIRST_CYCLE, LAST_CYCLE
from jason2.utils import str_to_list


class Project(object):
    """Holds project configuration parameters, such as data directory."""

    @classmethod
    def from_config(cls, filename):
        config = ConfigParser.RawConfigParser()
        config.read(filename)
        data_directory = config.get("project", "data_directory")
        products = str_to_list(config.get("project", "products"))
        passes = str_to_list(config.get("project", "passes"))
        email = config.get("project", "email")
        try:
            start_cycle = config.getint("project", "start_cycle")
        except ConfigParser.NoOptionError:
            start_cycle = FIRST_CYCLE
        try:
            end_cycle = config.getint("project", "end_cycle")
        except ConfigParser.NoOptionError:
            end_cycle = LAST_CYCLE
        return cls(data_directory, products, passes, email,
                   start_cycle, end_cycle)

    def __init__(self, data_directory, products, passes, email,
                 start_cycle=FIRST_CYCLE, end_cycle=LAST_CYCLE):
        self.data_directory = data_directory
        self.products = products
        self.passes = passes
        self.email = email
        self.start_cycle = start_cycle
        self.end_cycle = end_cycle

    def fetch(self):
        with FtpConnection(self.email) as ftp:
            for product in self.products:
                for cycle in range(self.start_cycle, self.end_cycle + 1):
                    ftp.fetch(product, cycle, self.passes, self.data_directory)
