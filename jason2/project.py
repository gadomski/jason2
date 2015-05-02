import ConfigParser

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
        tracks = str_to_list(config.get("project", "tracks"))
        try:
            start_cycle = config.getint("project", "start_cycle")
        except ConfigParser.NoOptionError:
            start_cycle = FIRST_CYCLE
        try:
            end_cycle = config.getint("project", "end_cycle")
        except ConfigParser.NoOptionError:
            end_cycle = LAST_CYCLE
        return cls(data_directory, products, tracks, start_cycle, end_cycle)

    def __init__(self, data_directory, products, tracks,
                 start_cycle=FIRST_CYCLE, end_cycle=LAST_CYCLE):
        self.data_directory = data_directory
        self.products = products
        self.tracks = tracks
        self.start_cycle = start_cycle
        self.end_cycle = end_cycle
