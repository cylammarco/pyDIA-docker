import sys
import os
import numpy as np

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

# WD physical position 
x0, y0 = 268.349, 265.786
prefix = input_folder
locate_date_range = (-1e10,1e10)

dates, seeing, roundness, bgnd, signal, flux, dflux, quality, x0, y0 = \
        CF.photom_variable_star(x0,y0,params,save_stamps=True,patch_half_width=20,locate_half_width=3,locate_date_range=locate_date_range)


refmags = np.loadtxt(params.loc_output+'/ref.mags.calibrated')
refflux = np.loadtxt(params.loc_output+'/ref.flux.calibrated')

star_dist2 = (refmags[:,1]-x0)**2 + (refmags[:,2]-y0)**2
star_num = np.argmin(star_dist2)

print 'x0 y0:', x0, y0
print 'Nearest star', star_num, 'located at', refmags[star_num,1], refmags[star_num,2]
print 'Reference flux', refflux[star_num,:]
print 'Reference mag', refmags[star_num,:]

mag = 25 - 2.5*np.log10(refflux[star_num,0] + flux)
mag_err = 25 - 2.5*np.log10(refflux[star_num,0] + flux - dflux) - mag 


lightcurve_header='      Date   Delta_Flux Err_Delta_Flux     Mag  Err_Mag        Q    FWHM Roundness      Sky    Signal'
dates += 2450000.5
np.savetxt(params.loc_output+'/'+prefix+'-lightcurve.dat',np.vstack((dates,flux,dflux,mag,mag_err,quality,seeing,roundness,bgnd,signal)).T, \
                    fmt='%12.5f  %12.4f  %12.4f  %7.4f  % 7.4f  %6.2f  %6.2f  %5.2f  %10.2f  %8.2f', \
                    header=lightcurve_header)

cal.plot_lightcurve(params.loc_output+'/'+prefix+'-lightcurve.dat',plotfile=prefix+'-lightcurve.png')
