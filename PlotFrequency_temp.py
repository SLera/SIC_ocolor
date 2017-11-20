#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 21:25:19 2017

@author: valeria
"""

import glob
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
sys.path.append('/home/valeria/AWI/HPbckp/LaptevFastIceproject/Scripts/My_functions')
import SAR_drift as Sdr


INDIR_data = '/home/valeria/NIERSC/Scripts/SIC_ocolor/output/Barents_sic_frequency/'

flist = np.array(glob.glob(os.path.join(INDIR_data, '*')))

for i in range(len(flist)):
    plt.figure()
    plt.imshow(np.load(flist[i]))
    plt.title(str(i))
    plt.colorbar()
    plt.show()