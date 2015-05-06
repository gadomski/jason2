"""Working with netCDF4 data."""

from collections import namedtuple

import netCDF4
import numpy


Waveforms = namedtuple("Waveforms", ["data", "latitudes"])


class Dataset(object):
    """Wrapper around a netCDF4 dataset.

    We wrap because we have some common functions that we need to do on the
    data, such as location masking.

    """

    def __init__(self, filename, bounds):
        self.data = netCDF4.Dataset(filename)
        self.variables = self.data.variables
        self.bounds = bounds

    def get_waveforms(self, clip=None):
        """Get waveform data for this dataset.

        The dataset needs to be an sgdr dataset, otherwise there won't be any
        waveform data to extract.

        """
        mask20hz = self._get_20hz_mask().flatten()
        waveforms = self.variables["waveforms_20hz_ku"][:]
        waveforms.shape = (waveforms.shape[0] * waveforms.shape[1],
                           waveforms.shape[2])
        waveforms = waveforms[mask20hz, :]
        if clip is not None:
            waveforms = waveforms.masked_outside(0, clip)
        return Waveforms(waveforms,
                         self.variables["lat_20hz"][:].flatten()[mask20hz])

    def get_sea_surface_height(self):
        """Ocean height"""
        correction = self._get_20hz_correction()
        mask20hz = self._get_20hz_mask()
        return (
            self.variables["alt_20hz"] -
            correction -
            self.variables["range_20hz_ku"][:]
        )[mask20hz].flatten()

    def _get_1hz_mask(self):
        return numpy.any(self._get_20hz_mask(), 1)

    def _get_20hz_mask(self):
        """Get a location mask for 20hz data."""
        mask = numpy.logical_and(
            self.variables["lat_20hz"][:] >= self.bounds.miny,
            self.variables["lat_20hz"][:] <= self.bounds.maxy)
        if self.bounds.minx is not None:
            mask = numpy.logical_and(
                mask,
                self.variables["lon_20hz"][:] >=
                self.bounds.minx)
        if self.bounds.maxx is not None:
            mask = numpy.logical_and(
                mask,
                self.variables["lon_20hz"][:] <=
                self.bounds.maxx)
        return mask

    def _get_20hz_correction(self):
        correction = (
            self.variables["model_dry_tropo_corr"][:] +
            self.variables["model_wet_tropo_corr"][:] +
            self.variables["iono_corr_gim_ku"][:] +
            self.variables["solid_earth_tide"][:] +
            self.variables["pole_tide"][:]
        )
        correction.shape = (len(correction), 1)
        return numpy.tile(correction, (1, 20))
