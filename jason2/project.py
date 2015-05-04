import ConfigParser
import glob
import os

import netCDF4

from jason2 import products
from jason2.exceptions import MissingEmail, Jason2Error
from jason2.ftp import FtpConnection
from jason2.utils import get_cycle_range, zfill3, str_to_list


class Project(object):
    """Holds project configuration parameters, such as data directory."""

    @classmethod
    def read_config(cls):
        config = ConfigParser.ConfigParser(defaults={
            "data-directory": None,
            "email": None,
            "products": [],
            "passes": [],
            "start-cycle": None,
            "end-cycle": None,
            "min-latitude": None,
            "max-latitude": None,
        })
        config_files = config.read([os.path.abspath("jason2.cfg"),
                                    os.path.expanduser("~/.jason2.cfg")])
        if not config.has_section("project"):
            config.add_section("project")
        return config, config_files

    @classmethod
    def from_config(cls):
        config, _ = cls.read_config()
        project = cls()
        project.data_directory = config.get("project", "data-directory")
        project.email = config.get("project", "email")
        project.products = [products[name] for name in
                            str_to_list(config.get("project", "products"))]
        project.passes = str_to_list(config.get("project", "passes"))
        project.start_cycle = config.get("project", "start-cycle")
        project.end_cycle = config.get("project", "end-cycle")
        return project

    def __init__(self):
        self.data_directory = "."
        self.email = None
        self.products = []
        self.passes = []
        self.start_cycle = None
        self.end_cycle = None

    def fetch(self, skip_unzipping=False, overwrite=False):
        if self.email is None:
            raise MissingEmail("No email provided for fetch")
        with FtpConnection(self.email) as ftp:
            for product in self.products:
                cycle_range = ftp.get_cycle_range(product, self.start_cycle,
                                                  self.end_cycle)
                for cycle in cycle_range:
                    ftp.fetch(product, cycle, self.passes, self.data_directory,
                              skip_unzipping=skip_unzipping,
                              overwrite=overwrite)

    def get_ice_heights(self, product, min_latitude, max_latitude):
        for dataset in self.dataset_iterator(product):
            pass
        return [1], [2]

    def get_cycle_range(self, product):
        directory = os.path.join(self.data_directory, product.directory_name)
        return get_cycle_range(os.listdir(directory), self.start_cycle,
                               self.end_cycle)

    def get_filename(self, product, cycle, pass_):
        g = os.path.join(self.data_directory, product.directory_name,
                         "cycle_{}".format(zfill3(cycle)),
                         product.get_glob(cycle, pass_, unzipped_only=True))
        files = glob.glob(g)
        assert len(files) == 1
        return files[0]

    def get_waveforms(self, cycle):
        if products["sgdr"] not in self.products:
            raise Jason2Error("Can get waveforms without sgdr product")
        if len(self.passes) != 1:
            raise Jason2Error("Can only get waveforms from a single pass")
        pass_ = self.passes[0]
        filename = self.get_filename(products["sgdr"], cycle, pass_)
        dataset = netCDF4.Dataset(filename)
        return dataset

    def dataset_iterator(self, product):
        return DatasetIterator(self, product)


class DatasetIterator(object):

    def __init__(self, project, product):
        self.project = project
        self.product = product
        cycle_range = project.get_cycle_range(product)
        self.cycle_iterator = iter(cycle_range)
        self.cycle = self.cycle_iterator.next()
        self.pass_iterator = iter(project.passes)

    def __iter__(self):
        return self

    def next(self):
        try:
            pass_ = self.pass_iterator.next()
        except StopIteration:
            self.cycle_directory = self.cycle_iterator.next()
            self.pass_iterator = iter(self.project.passes)
            return self.next()
        filename = self.project.get_filename(self.product, self.cycle, pass_)
        return netCDF4.Dataset(filename)
