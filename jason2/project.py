import ConfigParser


class Project(object):
    """Holds project configuration parameters, such as data directory."""

    @classmethod
    def from_config(cls, filename):
        config = ConfigParser.RawConfigParser()
        config.read(filename)
        return cls(config.get("data", "directory"))

    def __init__(self, data_directory):
        self.data_directory = data_directory
