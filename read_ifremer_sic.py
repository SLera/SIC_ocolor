import numpy as np
from netCDF4 import Dataset
#import matplotlib
#matplotlib.use('Agg')
from matplotlib import pyplot as plt


# def read_ifremer_sic_daily(FILENAME):
#     """Returns U-,V-wind components as flaaten np.arrays for each grid cell in
#     the for the SELS region (A) or central part of the SELS (B) or a grid point
#     (C)
#     CHECK THE REGION SETTINGS INSIDE THE FUNCTION
#     Parameters:
#     -----------
#     year
#     """
#     upath = 'D:\\DATA\\NCEP1\\Wind_6h@10m\\UWind\\uwnd.10m.gauss.'
#     vpath = 'D:\\DATA\\NCEP1\\Wind_6h@10m\\VWind\\vwnd.10m.gauss.'
#     # get u-wind component and the grid
#     f = Dataset(upath + str(year) + '.nc')
#     time = f.variables['time'][:]
#     lats = f.variables['lat'][:]
#     lons = f.variables['lon'][:]
#     uwind = f.variables['uwnd'][:]
#     # get v-wind component (time, lats, long identical to u-wind vars)
#     f = Dataset(vpath + str(year) + '.nc')
#     vwind = f.variables['vwnd'][:]
#     # A. slice data for the region based on lats_region and lons_region
#     uwind_reg = uwind[:, 6:10, 67:75]
#     vwind_reg = vwind[:, 6:10, 67:75]
#     lats_reg = lats[6:10]
#     lons_reg = lons[67:75]
#
#
#     wtime = np.arange(0, (len(time) / 4) + 0.25, 0.25)
#
#     return uwind_reg.flatten(), vwind_reg.flatten(), lats_reg, lons_reg, wtime

fname = '/home/valeria/NIERSC/Scripts/SIC_ocolor/test_data/19980101.nc'
fname_grid = '/home/valeria/NIERSC/Scripts/SIC_ocolor/test_data/grid_north_12km.nc'
f = Dataset(fname)
#f.variables
a = f.variables
qua_ma = f.variables['quality_flag'][:]
sic_ma = f.variables['concentration'][:]
sic = sic_ma.data[0,:,:]
fgr = Dataset(fname_grid)
lat = fgr.variables['latitude'][:]
lon= fgr.variables['longitude'][:]
OUTDIR = '/home/valeria/nfs0/data_sonarc/data/heap/ice_concentration/raw'

#plt.figure()
#plt.imshow(sic)
#plt.show()
