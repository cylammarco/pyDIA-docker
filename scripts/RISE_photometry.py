import sys
import os
import numpy as np
from astropy.io import fits

#
# Import the high-level pipeline routines
#
import DIA_CPU as DIA
params = DIA.DS.Parameters()

import calibration_functions as cal
import c_interface_functions as CF

input_folder = sys.argv[1]
output_folder = sys.argv[2]

#
# RISE parameters
#
params.use_GPU = False
params.gain = 2.30
params.readnoise = 10.0
params.pixel_min = 0
params.pixel_max = 20000
params.pdeg = 1
params.sdeg = 1
params.bdeg = 1
params.n_parallel = 2
params.star_detect_sigma = 10.0
params.psf_fit_radius = 3.0
params.reference_min_seeing = 0.5
params.reference_seeing_factor = 10.0
params.use_stamps = False
#params.nstamps = 100
params.name_pattern = '*.fits'
params.datekey = 'MJD'
params.loc_data = os.path.join('/root/input_images', input_folder)
params.loc_output = os.path.join('/root/output_dir', output_folder)

#
# Perform the difference imaging, photometry and calibration
#
print('Differencing images')
DIA.imsub_all_fits(params)
print('Calibrating')
cal.calibrate(params.loc_output)
