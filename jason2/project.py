import ConfigParser


class Project(object):
    """Holds project configuration parameters, such as data directory."""

    @classmethod
    def from_config(cls, filename):
        config = ConfigParser.RawConfigParser()
        config.read(filename)
        data_directory = config.get("project", "data_directory")
        products = [s.strip() for s in
                    config.get("project", "products").split(",")]
        return cls(data_directory, products)

    def __init__(self, data_directory, products):
        self.data_directory = data_directory
        self.products = products
