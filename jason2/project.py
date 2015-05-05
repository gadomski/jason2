import glob
import os

from jason2.dataset import Dataset
from jason2.exceptions import Jason2Error
from jason2.ftp import FtpConnection
from jason2.product import PRODUCTS
from jason2.utils import zfill3


class Project(object):
    """Holds project configuration parameters, such as data directory."""

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

    def get_waveforms(self, cycle, pass_number=None):
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
        dataset = self.get_dataset(PRODUCTS["sgdr"], cycle, pass_)
        return dataset.get_waveforms()

    def _get_dataset(self, product, cycle, pass_):
        filename = self.get_filename(product, cycle, pass_)
        return Dataset(filename, pass_.bounds)

    def _get_filename(self, product, cycle, pass_):
        g = os.path.join(self.data_directory, product.directory_name,
                         "cycle_{}".format(zfill3(cycle)),
                         product.get_glob(cycle, pass_, unzipped_only=True))
        files = glob.glob(g)
        assert len(files) == 1
        return files[0]

    def _get_pass_by_number(self, number):
        return next(pass_ for pass_ in self.passes if pass_.number == number)
