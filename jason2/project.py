import ConfigParser
import glob
import os
import re
import sys

from jason2.bounds import Bounds
from jason2.dataset import Dataset
from jason2.exceptions import Jason2Error, FileNotFound
from jason2.ftp import FtpConnection
from jason2.pass_ import Pass
from jason2.product import PRODUCTS
from jason2.utils import zfill3, str_to_list, get_cycle_range


class Project(object):
    """Holds project configuration parameters, such as data directory."""

    @classmethod
    def from_config(cls, filename):
        defaults = {
            "min_longitude": None,
            "max_longitude": None,
        }
        config = ConfigParser.ConfigParser(defaults)
        config.read(filename)
        try:
            products = [PRODUCTS[name] for name in
                        str_to_list(config.get("project", "products"))]
            pass_sections = [section for section in config.sections()
                             if section.startswith("pass-")]
            passes = []
            for section in pass_sections:
                match = re.match(r"pass-(\d+)", section)
                assert match
                minx = config.get(section, "min_longitude")
                maxx = config.get(section, "max_longitude")
                bounds = Bounds(
                    miny=config.getfloat(section, "min_latitude"),
                    maxy=config.getfloat(section, "max_latitude"),
                    minx=(float(minx) if minx is not None else None),
                    maxx=(float(maxx) if maxx is not None else None),
                )
                pass_ = Pass(number=int(match.group(1)), bounds=bounds)
                passes.append(pass_)

            return cls(
                data_directory=config.get("project", "data_directory"),
                email=config.get("project", "email"),
                products=products,
                passes=passes)
        except ConfigParser.Error as err:
            sys.stderr.write("Invalid configuration file: {}\n".format(
                os.path.abspath(filename)))
            raise err

    def __init__(self, data_directory, email, products, passes):
        self.data_directory = data_directory
        self.email = email
        self.products = products
        self.passes = passes

    def fetch(self, skip_unzipping=False, overwrite=False):
        with FtpConnection(self.email, self.data_directory, self.passes) as ftp:
            for product in self.products:
                ftp.fetch_product(product, skip_unzipping=skip_unzipping,
                                  overwrite=overwrite)

    def get_waveforms(self, cycle, pass_number=None, clip=None):
        if PRODUCTS["sgdr"] not in self.products:
            raise Jason2Error("Can get waveforms without sgdr product")
        if len(self.passes) == 0:
            raise Jason2Error("No passes configured for project")
        if len(self.passes) > 1:
            if pass_number is None:
                raise Jason2Error("Must provide pass if project has more than "
                                  "one pass")
            else:
                pass_ = self.get_pass_by_number(pass_number)
        else:
            pass_ = self.passes[0]
        dataset = self._get_dataset(PRODUCTS["sgdr"], cycle, pass_)
        return dataset.get_waveforms(clip)

    def get_dataset(self, product_name, cycle, pass_number):
        return self._get_dataset(PRODUCTS[product_name],
                                 cycle,
                                 self._get_pass_by_number(pass_number))

    def get_heights(self, product_name, pass_number, stddev_threshold=None):
        return self._get_heights(PRODUCTS[product_name],
                                 self._get_pass_by_number(pass_number),
                                 stddev_threshold)

    def get_cycle_heights(self, cycle, pass_number=None):
        if len(self.passes) == 0:
            raise Jason2Error("No passes configured for project")
        if len(self.passes) > 1:
            if pass_number is None:
                raise Jason2Error("Must provide pass if project has more than "
                                  "one pass")
            else:
                pass_ = self.get_pass_by_number(pass_number)
        else:
            pass_ = self.passes[0]
        dataset = self._get_dataset(PRODUCTS["sgdr"], cycle, pass_)
        return dataset.get_heights()

    def _get_dataset(self, product, cycle, pass_):
        filename = self._get_filename(product, cycle, pass_)
        return Dataset(filename, pass_.bounds)

    def _get_filename(self, product, cycle, pass_):
        g = os.path.join(self.data_directory, product.directory_name,
                         "cycle_{}".format(zfill3(cycle)),
                         product.get_glob(cycle, pass_, unzipped_only=True))
        files = glob.glob(g)
        if len(files) == 1:
            return files[0]
        else:
            raise FileNotFound("Could not find one data file")

    def _get_heights(self, product, pass_, stddev_threshold):
        dirname = os.path.join(self.data_directory, product.directory_name)
        heights = []
        for cycle in get_cycle_range(os.listdir(dirname)):
            try:
                dataset = self._get_dataset(product, cycle, pass_)
            except FileNotFound:
                continue
            heights.append(dataset.get_heights())
        if stddev_threshold:
            heights = [h for h in heights
                       if not self._exceed_threshold(h, stddev_threshold)]
        return heights

    def _exceed_threshold(self, heights, threshold):
        for value in heights.data.values():
            if value.stddev > threshold:
                return True
        return False

    def _get_pass_by_number(self, number):
        return next(pass_ for pass_ in self.passes if pass_.number == number)
