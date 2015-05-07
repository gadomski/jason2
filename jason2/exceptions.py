class Jason2Error(Exception):
    pass


class ConnectionError(Jason2Error):
    pass


class InvalidProductType(Jason2Error):
    pass


class InvalidProductFamily(Jason2Error):
    pass

class FileNotFound(Jason2Error):
    pass
