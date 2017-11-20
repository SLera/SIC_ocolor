#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 17:09:52 2017

@author: valeria
"""
import os
import gdal
import numpy as np


def read_tif(FILENAME):
    a = gdal.Open(FILENAME)
    a_band1 = a.GetRasterBand(1)
    a_band1_array = a_band1.ReadAsArray()
    ind = np.where(a_band1_array==-999)
    a=np.array(a_band1_array, dtype=float)
    a[ind]=np.nan
    return a

INDIR_data_tif = '/home/valeria/DATA/SeaIceConcentration/IFREMER/processed_ocolor/'
OUTDIR = '/home/valeria/NIERSC/Scripts/SIC_ocolor/output/Barents_sic/'
mask_region = np.load('./vars/barentsSea.npy')

flist=[]
for root, dirs, ffiles in os.walk(INDIR_data_tif):
  for ffile in ffiles:
      flist.append(os.path.join(root, ffile))
flist.sort()

ms = []
ds = []
yrs = []
sic = []

sic_Barents = []

for i in range(len(flist)):
    fname = flist[i]
    yr = fname[-12:-8]
    m = fname[-8:-6]
    d = fname[-6:-4]
    ms.append(m)
    ds.append(d)
    yrs.append(yr)
    
    sic = read_tif(fname)
    x,y = np.where(mask_region==1)
    lims = [x.min()-10, x.max()+10, y.min()-10, y.max()+10]
    sic_region = sic[lims[0]:lims[1],lims[2]:lims[3]]
    sic_region[np.where(mask_region[lims[0]:lims[1],lims[2]:lims[3]]!=1)]=np.nan
    sic_region.dump(OUTDIR+'Barents_'+yr+m+d)

