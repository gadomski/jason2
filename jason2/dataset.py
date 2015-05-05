import netCDF4
import numpy


class Dataset(object):

    def __init__(self, filename, bounds):
        self.data = netCDF4.Dataset(filename)
        self.variables = self.data.variables
        self.bounds = bounds

    def get_waveforms(self):
        mask20hz = self._get_20hz_mask()
        waveforms = self.variables["waveforms_20hz_ku"][:]
        waveforms.shape = (waveforms.shape[0] * waveforms.shape[1],
                           waveforms.shape[2])
        return waveforms[mask20hz, :], \
            self.variables["lat_20hz"][:].flatten()[mask20hz]

    def _get_20hz_mask(self):
        mask = numpy.logical_and(
            self.variables["lat_20hz"][:].flatten() >= self.bounds.miny,
            self.variables["lat_20hz"][:].flatten() <= self.bounds.maxy)
        if self.bounds.minx is not None:
            mask = numpy.logical_and(
                mask,
                self.variables["lon_20hz"][:].flatten() >=
                self.bounds.minx)
        if self.bounds.maxx is not None:
            mask = numpy.logical_and(
                mask,
                self.variables["lon_20hz"][:].flatten() <=
                self.bounds.maxx)
        return mask
