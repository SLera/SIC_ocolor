# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import gdal
from gdalconst import * 
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
sys.path.append('/home/valeria/AWI/HPbckp/LaptevFastIceproject/Scripts/My_functions')
import SAR_drift as Sdr

def read_tif(FILENAME):
    a = gdal.Open(FILENAME)
    a_band1 = a.GetRasterBand(1)
    a_band1_array = a_band1.ReadAsArray()
    ind = np.where(a_band1_array==-999)
    a=np.array(a_band1_array, dtype=float)
    a[ind]=np.nan
    return a

def tiff_to_latlon(filename, x_im,y_im):
    dataset = gdal.Open(filename, GA_ReadOnly)
    geotransform = dataset.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeigh = geotransform[5]
    
    from osgeo import osr
    # get the existing coordinate system
    NSIDC_WKT = 'PROJCS["NSIDC Sea Ice Polar Stereographic North",GEOGCS["Unspecified datum based upon the Hughes 1980 ellipsoid",DATUM["Not_specified_based_on_Hughes_1980_ellipsoid",SPHEROID["Hughes 1980",6378273,298.279411123064,AUTHORITY["EPSG","7058"]],AUTHORITY["EPSG","6054"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4054"]],PROJECTION["Polar_Stereographic"],PARAMETER["latitude_of_origin",70],PARAMETER["central_meridian",-45],PARAMETER["scale_factor",1],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["X",EAST],AXIS["Y",NORTH],AUTHORITY["EPSG","3411"]]'
    old_cs= osr.SpatialReference()
    old_cs.ImportFromWkt(NSIDC_WKT)
    
    # create the new coordinate system
    wgs84_wkt = """
    GEOGCS["WGS 84",
        DATUM["WGS_1984",
            SPHEROID["WGS 84",6378137,298.257223563,
                AUTHORITY["EPSG","7030"]],
            AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.01745329251994328,
            AUTHORITY["EPSG","9122"]],
        AUTHORITY["EPSG","4326"]]"""
    new_cs = osr.SpatialReference()
    new_cs .ImportFromWkt(wgs84_wkt)
    
    # create a transform object to convert between coordinate systems
    transform = osr.CoordinateTransformation(old_cs,new_cs) 
    #get the coordinates in lat long
    x = x_im*pixelWidth+originX
    y = y_im*pixelHeigh+originY
    latlong = transform.TransformPoint(x,y) 
    
    return latlong[0],latlong[1]

filename ='/home/valeria/DATA/SeaIceConcentration/IFREMER/processed_ocolor/IFREMER_IceConcentration_8day_19980101.tif'

data = read_tif(filename)

x,y=np.shape(data)
xx,yy=np.meshgrid(np.arange(0,x),np.arange(0,y))
#lons = np.zeros((x,y))
#lats = np.zeros((x,y))
lons = np.load('lons_i2175j1056')
lats = np.load('lats_i2175j1056')

for i in range(2175,x):
    for j in range(y):
        lons1,lats1 = tiff_to_latlon(filename,xx[i,j],yy[i,j])
        lons[i,j]=lons1
        lats[i,j]=lats1

lons.dump('lonsEASE')
lats.dump('latsEASE')
        
#Basemap = 

#la,lo = tiff_to_latlon(filename,0,0)