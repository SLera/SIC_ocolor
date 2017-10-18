#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 14:04:59 2017

@author: valeria
"""

from osgeo import gdal
import netCDF4
import numpy as np
import os
import glob
import matplotlib
#matplotlib.use('Agg')
from matplotlib import pyplot as plt
from datetime import datetime

#INDIR_ref_dates= '/home/valeria/DATA/Ocolor/Spectra_test'
#filter_name = []
#for root, dirs, files in os.walk(INDIR_ref_dates):
#    for file in files:
#        filter_name.append(os.path.join(root, file))
#        
#with open ('filter_name_test.txt', 'w') as in_files:
#    for item in filter_name: 
#        in_files.write(item+'\n')

###creater list of 8-days mean reference dates (1 day of 8-days intrval)
#def extract_ref_dates_temp(test_file):
#    ref_dates= []
#    for item in test_file:
#        ref_dates_txt = item[-19:-11]
#        #print item[-19:-11]
#        ref_dates.append(datetime.strptime(ref_dates_txt, '%Y%m%d'))
#    return ref_dates 

##creater list of 8-days mean reference dates (1 day of 8-days intrval)
def extract_ref_dates(INDIR_ref_dates):
    ref_dates= []
    for root, dirs, files in os.walk(INDIR_ref_dates):
        for file in files:
            fpath = os.path.join(root, file)
            ref_date = datetime.strptime(fpath[-18:-10], '%Y%m%d')
            ref_dates.append(ref_date)
    return ref_dates 
    
##find files fitting to an 8-days interval
def extract_dates_sic(INDIR_SIC, year):
    flist_sic = []
    dates_sic = []
    for root, dirs, files in os.walk(INDIR_sic+'/'+str(year)):
        for file in files:
            fpath = os.path.join(root, file)
            flist_sic.append(fpath)
            date_sic = datetime.strptime(fpath[-11:-3], '%Y%m%d')
            dates_sic.append(date_sic)
    return flist_sic, dates_sic

def read_ifremer_sic_daily(FILENAME):
     """Returns np.array with 0-100 sea ice concentration, (%)
     Parameters:
     -----------
     FILENAME
     """
     data_set = netCDF4.Dataset(FILENAME)
     sic = filter_array(data_set, filter1)
     return sic

def filter1( v, mv, q, land_val, nodata_val):
    """to filter v based on quality flags (q)
     Parameters:
     -----------
     v - np.array 'concentration'
     mv - UNUSED np.array mask for 'concentration'
     q - np.array 'quality_flag'
     land_value - value to use for land pixels
     nodata_value - value to to use for bad quality/nodata pixels
     """
    if q == 0:
        return v
    elif q == 1:
        return land_val
    else:
        return nodata_val

def filter2( v, mv, q, land_val, nodata_val ):
    """to filter v based on binary mask (mv)
     Parameters:
     -----------
     v - np.array 'concentration'
     mv - np.array mask for 'concentration'
     q - UNUSED np.array 'quality_flag'
     land_value - value to use for land pixels
     nodata_value - value to to use for bad quality/nodata pixels
     """
    if mv:
        return v
    else:
        return nodata_val
    
def filter_array( data_set, filt ):
    q  = data_set.variables['quality_flag'][0,:,:]
    v  = data_set.variables['concentration'][:].data[0,:,:]
    mv = data_set.variables['concentration'][:].mask[0,:,:]
    #np.save('q.npy')
    res = np.zeros( np.shape(v) )
    land_val = np.nan
    nodata_val = np.nan
    for i in range(np.shape(q)[0]):
        for j in range(np.shape(q)[1]):
            res[i,j] = filt( v[i,j], mv[i,j], q[i,j], land_val, nodata_val)
#    plt.figure()
#    plt.imshow(res)
#    plt.colorbar()
#    plt.show()
    print np.unique(res), res.min(), res.max()
    return res

INDIR_sic = '/home/valeria/DATA/Ocolor/SIC_test'
fpath_sic,dates_sic = extract_dates_sic(INDIR_sic,1998)

INDIR_ref_dates= '/home/valeria/DATA/Ocolor/Spectra_test'

text_file = open('filter_name_test.txt', 'r')
ref_ls = text_file.readlines()
ref_ls.sort()

ref_dates = extract_ref_dates(INDIR_ref_dates)

ref_dateA = ref_dates[0]

def find_8d_files(ref_date,dates_sic):
    ls_sic_8days = []
    for i in range(len(dates_sic)):
        timedif = dates_sic[i]-ref_date
        if (timedif.days>=0 and timedif.days<8):
            ls_sic_8days.append(fpath_sic[i])
    return ls_sic_8days

def calculate_8d_mean(ls_sic_8days):
    ls = []            
    for i in range(len(ls_sic_8days)):
        daily_sic = read_ifremer_sic_daily(ls_sic_8days[i])
        ls.append(daily_sic)
    sic_array = np.array(ls)
    sic_mean = np.nanmean(sic_array,axis=0)
    return sic_array, sic_mean


ls_sic_8days = find_8d_files(ref_dateA,dates_sic)
sic_array, sic_mean = calculate_8d_mean(ls_sic_8days)
plt.figure()
plt.imshow(sic_mean)
plt.title('mean')
plt.show()

