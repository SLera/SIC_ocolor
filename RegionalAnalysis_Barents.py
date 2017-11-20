#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 17:09:52 2017

@author: valeria
"""
import os
import gdal
import numpy as np
import matplotlib.pyplot as plt

def read_tif(FILENAME):
    a = gdal.Open(FILENAME)
    a_band1 = a.GetRasterBand(1)
    a_band1_array = a_band1.ReadAsArray()
    ind = np.where(a_band1_array==-999)
    a=np.array(a_band1_array, dtype=float)
    a[ind]=np.nan
    return a

INDIR_data_reg = '/home/valeria/NIERSC/Scripts/SIC_ocolor/output/Barents_sic/'

PIXAREA = 4*4 #km^2

flist=[]
for root, dirs, ffiles in os.walk(INDIR_data_reg):
  for ffile in ffiles:
      flist.append(os.path.join(root, ffile))
flist.sort()

months = np.array([u'Янв', u'Фев',u'Мар', u'Апр',u'Май',u'Июн',u'Июл',u'Авг', u'Сен', u'Окт', u'Ноя',u'Дек' ])
months_n = np.arange(1,13)

sic_Barents = []

area_m1 = np.zeros(np.shape(months))
extent_m = np.zeros(np.shape(months))
file_n1 = np.zeros(np.shape(months))
area_yr = []
extent_yr = []

for f in range(len(flist)):
    fname = flist[f]
    yr = fname[-8:-4]
    m = fname[-4:-2]
    d = fname[-2:]
    #print yr,m,d
    
    sic = np.load(fname)
    area_km = (sic/100)*PIXAREA
    ind_ext = np.where(sic>15)
    extent_km = np.nansum(len(ind_ext[0])*PIXAREA)
    area_m1[int(m)-1]+=np.nansum(area_km)
    extent_m[int(m)-1]+=extent_km
    file_n1[int(m)-1]+=+1


plt.figure()
plt.plot(area_m1/file_n1, label = u'Площадь льдов')
plt.plot(extent_m/file_n1, label = u'Протяженность льдов')
plt.ylabel(u'км^2')
plt.grid()
plt.title(u'Баренцево море, 1998-2016')
plt.xticks(np.arange(len(months)),months)
plt.show()

years = np.arange(1998,2017)
area_yr = []
extent_yr = []
plt.figure()
for y in range(len(years)):
    file_n = np.zeros(np.shape(months))
    area_m = np.zeros(np.shape(months))
    extent_m = np.zeros(np.shape(months))

    for f in range(len(flist)):
        fname = flist[f]
        yr = fname[-8:-4]
        m = fname[-4:-2]
        d = fname[-2:]
        #print yr,m,d
        if int(yr) == years[y]:
            #print yr,m,d
            file_n[int(m)-1]+=1
            sic = np.load(fname)
            area_km = (sic/100)*PIXAREA
            ind_ext = np.where(sic>15)
            extent_km = np.nansum(len(ind_ext[0])*PIXAREA)
            area_m[int(m)-1]+=np.nansum(area_km)
            extent_m[int(m)-1]+=extent_km
            
    area_yr.append(area_m/file_n) 
    plt.plot(area_m/file_n, color = 'grey', lw = 0.5, label = years[y])
    #plt.legend()

    #plt.plot(extent_m/file_n, label = yr)
    
area_yr = np.array(area_yr)
area_mean = np.zeros(len(months))
std_m = np.zeros(len(months))
min_m = np.zeros(len(months))
max_m = np.zeros(len(months))
for m in range(len(months)):
    a = area_yr[:,m]
    std_m[m]= a.std()
    area_mean[m] = a.mean()
    min_m[m] = a.min()
    max_m[m] = a.max()
    
plt.plot(area_mean, 'k--', lw=2.0)
#lower_bound = area_mean-(2*std_m)
#upper_bound = area_mean+(2*std_m)

lower_bound = min_m
upper_bound = max_m

plt.plot(lower_bound, 'k')
plt.plot(upper_bound, 'k')
plt.ylabel(u'км^2')
plt.grid()
#plt.legend()
plt.title(u'Площадь ледового покрова, 1998-2016')
plt.xticks(np.arange(len(months)),months)
plt.tight_layout()
plt.show()
#plt.savefig('SeaIceAreaBarents1998-2019.pdf',dpi=400)

#statistics