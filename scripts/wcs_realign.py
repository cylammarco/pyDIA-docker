import os
from ccdproc import wcs_project
from ccdproc import Combiner
from astropy.io import fits
from astropy.wcs import WCS
from astropy.nddata import CCDData


folder_RISE = "/Users/marcolam/Downloads/20190602_1"
RISE_file = os.listdir(folder_RISE)
RISE_file.sort()
RISE_file = RISE_file[2:]

target_hdu = fits.open(folder_RISE + '/' + RISE_file[0])[0]
target_wcs = WCS(target_hdu.header)

RISE_reprojected = []

for filename in RISE_file:
    input_image = fits.open(folder_RISE + '/' + filename)[0]
    input_image = CCDData(input_image.data, header=input_image.header, unit='adu')
    input_image.wcs = WCS(input_image.header)
    new_image = wcs_project(input_image, target_wcs)
    new_image.write(folder_RISE + '/' + filename.split('.')[0] + '_WCS.fits')
    RISE_reprojected.append(new_image)



RISE_combiner = Combiner(RISE_reprojected)
RISE_stacked_image = RISE_combiner.median_combine()
RISE_stacked_image.wcs = target_wcs
RISE_stacked_image.write(folder_RISE + '/RISE_stacked.fits')

