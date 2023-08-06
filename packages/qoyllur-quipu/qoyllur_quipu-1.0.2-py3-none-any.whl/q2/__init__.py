#!/bin/bash
"""q2 was created to facilitate standard 1D/LTE spectroscopic analyses
of stars. It helps determining fundamental parameters (Teff, logg,
[Fe/H], etc.) of solar-type stars given an observational data set. q2
requires the FEB 2017 version of the spectrum synthesis code MOOG
(http://www.as.utexas.edu/~chris/moog.html) and files containing the
model atmosphere and isochrone grids. The latter can be downloaded from
http://www.astrochasqui.com/projects/astro/share/q2Data.tar.gz and must
be placed in the q2/Data folder.
"""

import matplotlib

matplotlib.use('Agg')
from .config import *
from .star import *
from . import moog, specpars, errors, abundances
from . import isopars
import logging

logger = logging.getLogger(__name__)

__author__ = 'Ivan Ramirez (Tacoma Community College)'
__email__ = 'iramirez@tacomacc.edu'


logging.basicConfig(level=logging.ERROR)
logger.setLevel('WARNING')

_moog = moog_is_available()
_data = data_are_available()

logger.setLevel('ERROR')

