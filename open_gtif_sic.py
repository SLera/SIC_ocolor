#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 15:41:44 2017

@author: valeria
"""

import gdal
from gdalconst import * 
import matplotlib.pyplot as plt


def read_SAR_tiff(filename):
    dataset = gdal.Open(filename, GA_ReadOnly)
    
    cols = dataset.RasterXSize
    rows = dataset.RasterYSize
    bands = dataset.RasterCount
    driver = dataset.GetDriver().LongName
    geotransform = dataset.GetGeoTransform()
    
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeigh = geotransform[5]
    
    band = dataset.GetRasterBand(1)
    
    data = band.ReadAsArray(0, 0, cols, rows)
    
    return data

filename = '19980101_NaN_2.tif'

data = read_SAR_tiff(filename)