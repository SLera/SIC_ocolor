#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 21:25:19 2017

@author: valeria
"""
import matplotlib
matplotlib.use('qt5agg')
import matplotlib as mpl


import glob
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import gdal
sys.path.append('/home/valeria/AWI/HPbckp/LaptevFastIceproject/Scripts/My_functions')


def clip_by_mask( data, mask ):
    x, y = np.where(mask_region == 1)
    lims = [x.min() - 10, x.max() + 10, y.min() - 10, y.max() + 10]
    cliped_data = data[lims[0]:lims[1], lims[2]:lims[3]]
    #cliped_data[np.where(mask_region[lims[0]:lims[1], lims[2]:lims[3]] != 1)] = np.nan
    return cliped_data

def read_tif(FILENAME):
    a = gdal.Open(FILENAME)
    a_band1 = a.GetRasterBand(1)
    a_band1_array = a_band1.ReadAsArray()
    ind = np.where(a_band1_array==-999)
    a=np.array(a_band1_array, dtype=float)
    a[ind]=np.nan
    return a

INDIR_data = './output/Barents_sic_frequency/'

flist = np.array(glob.glob(os.path.join(INDIR_data, '*')))
land = read_tif('./land_mask.tif')
mask_region = np.load('./vars/barentsSea.npy')

cliped_land = clip_by_mask( land, mask_region )

for i in range(1):#len(flist)):
    plt.figure()
    r = np.load(flist[i])
    plt.imshow(r)
    plt.imshow(cliped_land, alpha=.7, cmap=plt.cm.gray )
    plt.title(str(i))
    plt.colorbar()
    plt.show()

a = 1