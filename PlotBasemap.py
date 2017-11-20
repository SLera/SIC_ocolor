#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 18:50:36 2017

@author: valeria
"""
import gdal
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

#INDIR_data_tif = '/home/valeria/DATA/SeaIceConcentration/IFREMER/processed_ocolor/'
INDIR_data = '/home/valeria/NIERSC/Scripts/SIC_ocolor/output/Barents_sic/'
mask_region = np.load('./vars/barentsSea.npy')

#lats, lons = load from grid.nc
lats = np.load('./vars/latsEASE')
lons = np.load('./vars/lonsEASE')

x,y = np.where(mask_region==1)
lims = [x.min()-10, x.max()+10, y.min()-10, y.max()+10]
lats_reg = lats[lims[0]:lims[1],lims[2]:lims[3]]
lons_reg = lons[lims[0]:lims[1],lims[2]:lims[3]]

xx,yy=np.meshgrid(np.arange(-1250,1250),np.arange(-1250,1250))

xx=xx*4000
yy=yy*4000

xx_reg = xx[lims[0]:lims[1],lims[2]:lims[3]]
yy_reg = yy[lims[0]:lims[1],lims[2]:lims[3]]

m1 = Basemap(resolution="i",
            projection='laea', lat_ts=70, lat_0=90., lon_0=-45.,
            llcrnrlon= 16, llcrnrlat= 85,
            urcrnrlon= 76, urcrnrlat= 50,
            rsphere=6371228)

#lo1,la1 = m1(xx_reg[-1,0],yy_reg[-1,0], inverse = True)
#lo2,la2 = m1(xx_reg[0,-1],yy_reg[0,-1], inverse = True)

lo1,la1 = m1(xx_reg[0,0],yy_reg[0,0], inverse = True)
lo2,la2 = m1(xx_reg[-1,-1],yy_reg[-1,-1], inverse = True)
#
#lo1,la1 = m1(xx_reg[0,-1],yy_reg[0,-1], inverse = True)
#lo2,la2 = m1(xx_reg[-1,0],yy_reg[-1,0], inverse = True)

lo1,la1 = m1(xx_reg[-1,-1],yy_reg[-1,-1], inverse = True)
lo2,la2 = m1(xx_reg[0,0],yy_reg[0,0], inverse = True)


print '1',lo1, la1
print '2',lo2, la2


#plt.figure()
#m1.drawcoastlines()
#m1.drawmeridians(np.arange(10,80,10))
#m1.drawparallels(np.arange(60,80,5))
#plt.show()
#
#lat_l = lats_reg[-1,0]
#lon_l = lons_reg[-1,0]
#
#lat_u = lats_reg[0,-1]
#lon_u = lons_reg[0,-1]
#
#
#lat_l = lats_reg[0,0]
#lon_l = lons_reg[0,0]
#
#lat_u = lats_reg[-1,-1]
#lon_u = lons_reg[-1,-1]
#
#print lon_l, lat_l
#print lon_u, lat_u

#m = Basemap(resolution="i",
#            projection='laea', lat_ts=70, lat_0=90., lon_0=-45.,
#            llcrnrlon= lon_l, llcrnrlat= lat_l,
#            urcrnrlon= lon_u, urcrnrlat= lat_u,
#            rsphere=6371228)

m = Basemap(resolution="i",
            projection='laea', lat_ts=70, lat_0=90., lon_0=-45.,
            llcrnrlon= lo1, llcrnrlat= la1,
            urcrnrlon= lo2, urcrnrlat= la2,
            rsphere=6371228)

test = np.load(INDIR_data+'Barents_19980101')
plt.figure()
m.imshow(test,origin = 'lower')
m.fillcontinents()
m.drawparallels(np.arange(60.,80.,5.),labels=[1, 1, 1, 1])
m.drawmeridians(np.arange(-10.,60.,10.),labels=[1, 1, 1, 1])
plt.show()