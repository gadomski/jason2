from jason2.exceptions import InvalidProductType, InvalidProductFamily
from jason2.utils import zfill3


class Product(object):

    DEFAULT_FAMILY = "gdr"
    DEFAULT_VERSION = "d"

    def __init__(self, name, type_, zipped=False, directory_name=None,
                 family=DEFAULT_FAMILY, version=DEFAULT_VERSION):
        self.name = name
        self.type_ = type_
        self.zipped = zipped
        self.directory_name = name if directory_name is None else directory_name
        self.family = family
        self.version = version

    def get_glob(self, cycle, pass_):
        cycle_str = zfill3(cycle)
        pass_str = zfill3(pass_)
        return "JA2_{}P{}_2P{}P{}_{}_*{}".format(
            self.get_family_code(), self.get_type_code(), self.version,
            cycle_str, pass_str, self.get_extension())

    def get_type_code(self):
        if self.type_ == "native":
            return "N"
        elif self.type_ == "reduced":
            return "R"
        elif self.type_ == "sensor":
            return "S"
        else:
            raise InvalidProductType(
                "Unknown product type: {}".format(self.type_))

    def get_family_code(self):
        if self.family == "ogdr":
            return "O"
        elif self.family == "igdr":
            return "I"
        elif self.family == "gdr":
            return "G"
        else:
            raise InvalidProductFamily(
                "Unknown product family: {}".format(self.family))

    def get_extension(self):
        return ".zip" if self.zipped else ".nc"
