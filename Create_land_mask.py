#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 14:04:59 2017

@author: valeria
@script name: through the ass script
"""

from osgeo import gdal
import netCDF4
import numpy as np
import os
import glob
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from datetime import datetime

def extract_land_mask(FILENAME):
     """Returns np.array with 1 for land and 0 otherwise
     Parameters:
     -----------
     FILENAME
     """
     data_set = netCDF4.Dataset(FILENAME)
     sic = filter_array(data_set, land_filter)
     return sic

def land_filter( q ):
    """to filter v based on quality flags (q)
     Parameters:
     -----------
     q - np.array 'quality_flag'
     """
    if q == 0:
        return 1
    else:
        return 0

def filter_array( data_set, filt ):
    q  = data_set.variables['quality_flag'][0,:,:]
    res = np.zeros( np.shape(q) )
    for i in range(np.shape(q)[0]):
        for j in range(np.shape(q)[1]):
            res[i,j] = filt(q[i,j])

    return res

def gdalwarp (input_file, target_file, epsg,xmin,xmax,ymin,ymax,x_size,y_size):
    #print 'gdalwarp -t_srs %s -te %s %s %s %s -tr %s %s -overwrite -of GTiff %s %s' % (epsg, xmin, ymin, xmax, ymax, x_size, y_size, input_file, target_file)
    os.system('gdalwarp --config GDAL_DATA "/home/lera/miniconda/share/gdal" '
              '-r near -t_srs %s -te %s %s %s %s -tr %s %s -overwrite '
              '-of GTiff %s %s -et 0.01 -dstnodata -999' %
                    (epsg, xmin, ymin, xmax, ymax,
                     x_size, y_size, input_file, target_file))

def prepare_nsidc_ic_filtered (sic_mean, output_tiff):
#    dataset = netCDF4.Dataset(input_nc)
##   ice_concentration = dataset.variables['concentration'][:][0]
#    sic = filter_array(dataset, filter1)
    ice_concentration = sic_mean
#    print ice_concentration

    driver = gdal.GetDriverByName('GTiff')
    outData = driver.Create('temp.tif', ice_concentration.shape[1], ice_concentration.shape[0], 1, gdal.GDT_Int16)
    outData.GetRasterBand(1).WriteArray(ice_concentration)
    outData.SetGeoTransform(geotransform_opt)
    outData.SetProjection(NSIDC_WKT)
    outData.FlushCache()
    del outData

    gdalwarp('temp.tif', output_tiff, target_epsg, target_xmin, target_xmax, target_ymin, target_ymax, taget_xsize, target_ysize)

##### CONSTS
xSize = 12500
ySize = -12500
xCorner = -3850074.56
yCorner = 5850046.72
geotransform_opt = [xCorner, xSize, 0, yCorner, 0, ySize]
NSIDC_WKT = 'PROJCS["NSIDC Sea Ice Polar Stereographic North",GEOGCS["Unspecified datum based upon the Hughes 1980 ellipsoid",DATUM["Not_specified_based_on_Hughes_1980_ellipsoid",SPHEROID["Hughes 1980",6378273,298.279411123064,AUTHORITY["EPSG","7058"]],AUTHORITY["EPSG","6054"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4054"]],PROJECTION["Polar_Stereographic"],PARAMETER["latitude_of_origin",70],PARAMETER["central_meridian",-45],PARAMETER["scale_factor",1],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["X",EAST],AXIS["Y",NORTH],AUTHORITY["EPSG","3411"]]'

# Domain
#EPSG:3973 -te -5000000 -5000000 5000000 5000000 -tr 4000 4000
target_epsg = 'EPSG:3973'
target_xmin = -5000000
target_ymin = -5000000
target_xmax = 5000000
target_ymax = 5000000
taget_xsize = 4000
target_ysize = 4000
#####

land = extract_land_mask('/home/lera/NIERSC/scripts/SIC_ocolor/19980101.nc')
prepare_nsidc_ic_filtered(land, '/home/lera/NIERSC/scripts/SIC_ocolor/land_mask.tif')