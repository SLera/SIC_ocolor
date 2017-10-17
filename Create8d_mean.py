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

#INDIR_filter_name = '/home/valeria/DATA/Ocolor/Spectra_test'
#
#filter_name = []
#for root, dirs, files in os.walk(INDIR_filter_name):
#    for file in files:
#        filter_name.append(os.path.join(root, file))
#        
#with open ('filter_name_test.txt', 'w') as in_files:
#    for item in filter_name: 
#        in_files.write(item+'\n')

##creater list of 8-days mean reference dates (1 day of 8-days intrval)
def extract_ref_dates(test_file):
    filter_date= []
    for item in test_file:
        filter_date_txt = item[-19:-11]
        filter_date.append(datetime.strptime(filter_date_txt, '%Y%m%d'))
        
text_file = open('filter_name_test.txt', 'r')
filter_name = text_file.readlines()
filter_name.sort()
    
##find files fitting to an 8-days intercal
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

INDIR_sic = '/home/valeria/DATA/Ocolor/SIC_test'
f,d = extract_dates_sic(INDIR_sic,1998)

ref_date = filter_date[0]

