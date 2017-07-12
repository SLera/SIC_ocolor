import numpy as np
from netCDF4 import Dataset
import matplotlib
matplotlib.use('Agg')
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

land_val = 101
nodata_val = 102
def filter1( v, mv, q ):
    if q == 0:
        return v
    elif q == 1:
        return land_val
    else:
        return nodata_val

def filter2( v, mv, q ):
    if mv:
        return v
    else:
        return nodata_val
    
def filter_array( data_set, filt ):
    q  = data_set.variables['quality_flag'][0,:,:]
    v  = data_set.variables['concentration'][:].data[0,:,:]
    mv = data_set.variables['concentration'][:].mask[0,:,:]
    res = np.zeros( np.shape(v) )
    for i in range(np.shape(q)[0]):
        for j in range(np.shape(q)[1]):
            res[i,j] = filt( v[i,j], mv[i,j], q[i,j] )
    return res

fname = '/home/lera/NIERSC/scripts/SIC_ocolor/19980101.nc'
fname_grid = '/home/lera/NIERSC/scripts/SIC_ocolor/grid_north_12km.nc'
f = Dataset(fname)
r = filter_array(f, filter1)
#f.variables
#a = f.variables
#qua_ma = f.variables['quality_flag'][:]
#sic_ma = f.variables['concentration'][:]
#sic = sic_ma.data[0,:,:]
#fgr = Dataset(fname_grid)
#lat = fgr.variables['latitude'][:]
#lon= fgr.variables['longitude'][:]
#OUTDIR = '/home/valeria/nfs0/data_sonarc/data/heap/ice_concentration/raw'
#
#plt.figure()
#plt.imshow(sic)
#plt.show()
#a=5
#
#cmap=plt.cm.rainbow
#norm = matplotlib.colors.BoundaryNorm(np.arange(0,15,1), cmap.N)
#plt.scatter(x,y,c=z,cmap=cmap,norm=norm,s=100,edgecolor='none')
#plt.colorbar(ticks=np.linspace(0,15,1))