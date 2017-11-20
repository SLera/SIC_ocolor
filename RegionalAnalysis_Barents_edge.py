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
INDIR_var = ''
OUTDIR ='/home/valeria/NIERSC/Scripts/SIC_ocolor/output/Barents_sic_frequency/'

flist=[]
for root, dirs, ffiles in os.walk(INDIR_data_reg):
  for ffile in ffiles:
      flist.append(os.path.join(root, ffile))
flist.sort()

months = np.array([u'Янв', u'Фев',u'Мар', u'Апр',u'Май',u'Июн',u'Июл',u'Авг', u'Сен', u'Окт', u'Ноя',u'Дек' ])
months_n = np.arange(1,13)

        
extent_yr = []
plt.figure()

for month in months_n:
    print month
    SIC = []
    for f in range(len(flist)):
        fname = flist[f]
        yr = fname[-8:-4]
        m = fname[-4:-2]
        d = fname[-2:]
        #print yr,m,d
        if int(m) == month:
            SIC.append(np.load(fname))
                    
    mean = np.zeros(np.shape(SIC[0]))
    num = 0
 
    for j in range(len(SIC)):
        extent = np.zeros(np.shape(SIC[0]))
        ind = np.where(SIC[j]>15)
        extent[ind]=1
        num = num+1
        mean = mean + extent
        
    if np.nansum(mean)>0:    
        frequency =mean/num*100 
        print num
        frequency.dump(OUTDIR+str(month)+'_fr_av')
  