# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from osgeo import gdal
import netCDF4
import numpy as np
import os

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
#taget_xsize = 12500
#target_ysize = 12500
#####

def gdalwarp (input_file, target_file, epsg,xmin,xmax,ymin,ymax,x_size,y_size):
    #print 'gdalwarp -t_srs %s -te %s %s %s %s -tr %s %s -overwrite -of GTiff %s %s' % (epsg, xmin, ymin, xmax, ymax, x_size, y_size, input_file, target_file)
    os.system('gdalwarp --config GDAL_DATA "/home/valeria/Programs/miniconda/share/gdal" -t_srs %s -te %s %s %s %s -tr %s %s -overwrite -of GTiff %s %s -et 0.01' % (epsg, xmin, ymin, xmax, ymax, x_size, y_size, input_file, target_file))

def prepare_nsidc_ic (input_nc, output_tiff):
    dataset = netCDF4.Dataset(input_nc)
    ice_concentration = dataset.variables['concentration'][:][0]
    print ice_concentration.shape
    
    driver = gdal.GetDriverByName('GTiff')
    outData = driver.Create('temp.tif', ice_concentration.shape[1], ice_concentration.shape[0], 1, gdal.GDT_Byte)
    outData.GetRasterBand(1).WriteArray(ice_concentration)
    outData.SetGeoTransform(geotransform_opt)
    outData.SetProjection(NSIDC_WKT)
    
    outData.FlushCache()
    del outData
    
    gdalwarp('temp.tif', output_tiff, target_epsg, target_xmin, target_xmax, target_ymin, target_ymax, taget_xsize, target_ysize)

prepare_nsidc_ic('19980101.nc','19980101.tif')