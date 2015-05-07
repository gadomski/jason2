"""Very simple rectagular bounds."""

from collections import namedtuple


class Bounds(object):

    def __init__(self, miny, maxy, minx=None, maxx=None):
        self.miny = miny
        self.minx = minx
        self.maxy = maxy
        self.maxx = maxx
