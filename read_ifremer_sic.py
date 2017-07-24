import numpy as np
from netCDF4 import Dataset
import gdal, ogr, os, osr
import matplotlib
#matplotlib.use('Agg')
from matplotlib import pyplot as plt


def read_ifremer_sic_daily(FILENAME):
     """Returns np.array with 0-100 sea ice concentration, (%)
     Parameters:
     -----------
     FILENAME
     """
     data_set = Dataset(FILENAME)
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
     nodata_value - valur to to use for bad quality/nodata pixels
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
     nodata_value - valur to to use for bad quality/nodata pixels
     """
    if mv:
        return v
    else:
        return nodata_val
    
def filter_array( data_set, filt ):
    q  = data_set.variables['quality_flag'][0,:,:]
    v  = data_set.variables['concentration'][:].data[0,:,:]
    mv = data_set.variables['concentration'][:].mask[0,:,:]
    res = np.zeros( np.shape(v) )
    land_val = np.NaN
    nodata_val = np.NaN
    for i in range(np.shape(q)[0]):
        for j in range(np.shape(q)[1]):
            res[i,j] = filt( v[i,j], mv[i,j], q[i,j], land_val, nodata_val)
    return res




fname = '/home/valeria/NIERSC/Scripts/SIC_ocolor/19980101.nc'
fname_grid = '/home/valeria/NIERSC/Scripts/SIC_ocolor/grid_north_12km.nc'
#f = Dataset(fname)
#r = filter_array(f, filter1)

sic =  read_ifremer_sic_daily(fname)

plt.figure()
plt.imshow(sic)
plt.show()

fgrd= Dataset(fname_grid)
lat = fgrd.variables['latitude'][:]
lon = fgrd.variables['longitude'][:]

array = sic

fgr = Dataset(fname_grid)
lat = fgr.variables['latitude'][:]
lon = fgr.variables['longitude'][:]
lat0 = lat[0,0]
lon0 = lon[0,0]

class x(float):
    pass
lat0 = lat0.astype(x)
lon0 = lon0.astype(x)

wkt_wgs84 = """
GEOGCS["WGS 84",
    DATUM["WGS_1984",
        SPHEROID["WGS 84",6378137,298.257223563,
            AUTHORITY["EPSG","7030"]],
        AUTHORITY["EPSG","6326"]],
    PRIMEM["Greenwich",0,
        AUTHORITY["EPSG","8901"]],
    UNIT["degree",0.01745329251994328,
        AUTHORITY["EPSG","9122"]],
    AUTHORITY["EPSG","4326"]]"""
    
wkt_gtiff = """
PROJCS["WGS 84 / NSIDC EASE-Grid North",
    GEOGCS["WGS 84",
        DATUM["WGS_1984",
            SPHEROID["WGS 84",6378137,298.257223563,
                AUTHORITY["EPSG","7030"]],
            AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0,
               AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.0174532925199433,
             AUTHORITY["EPSG","9122"]],
        AUTHORITY["EPSG","4326"]],
             PROJECTION["Lambert_Azimuthal_Equal_Area"],
                 PARAMETER["latitude_of_center",90],
                     PARAMETER["longitude_of_center",0],
                         PARAMETER["false_easting",0],
                PARAMETER["false_northing",0],
                    UNIT["metre",1,
        AUTHORITY["EPSG","9001"]],
            AXIS["X",EAST],
                AXIS["Y",NORTH],
        AUTHORITY["EPSG","3973"]]"""
                    
wkt1 = 'LOCAL_CS["WGS 84 / NSIDC EASE-Grid North",GEOGCS["WGS 84",DATUM["unknown",SPHEROID["unretrievable - using WGS84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]],AUTHORITY["EPSG","3973"],UNIT["metre",1,AUTHORITY["EPSG","9001"]]]'

sic_cs = osr.SpatialReference()
sic_cs.ImportFromWkt(wkt_wgs84)

gtiff_cs = osr.SpatialReference()
gtiff_cs.ImportFromWkt(wkt_gtiff)

transform = osr.CoordinateTransformation(sic_cs,gtiff_cs)
(x0,y0,z0) = transform.TransformPoint(lon0,lat0)

newRasterfn = 'sic7.tiff'
rasterOrigin = [x0,y0]
pixelWidth = 12500  # size of the pixel in m    
pixelHeight= 12500 

def array2raster(newRasterfn,rasterOrigin,pixelWidth,pixelHeight,array):

    cols = array.shape[1]
    rows = array.shape[0]
    originX = rasterOrigin[0]
    originY = rasterOrigin[1]
    
    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(newRasterfn, cols, rows, 1, gdal.GDT_Byte)
    outRaster.GetRasterBand(1).WriteArray(array)
    #outband = outRaster.GetRasterBand(1)
    #outband.WriteArray(array)
    #outRasterSRS = osr.SpatialReference()
    #outRasterSRS.ImportFromEPSG(3973)
    #outRasterSRS.ImportFromWkt(wkt_gtiff)
    EPSG3973_proj4 = '+proj=laea +lat_0=90 +lon_0=0 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs'
    outRaster.SetProjection(wkt1)
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
    #outRaster.SetProjection(outRasterSRS.ImportFromWkt(wkt_gtiff))
    #outRaster.FlushCache()

array2raster(newRasterfn,rasterOrigin,pixelWidth,pixelHeight,array)

#gdalCommand = 'gdalwarp -t_srs EPSG:3973 -wo SAMPLE_STEPS=1000 -wo SAMPLE_GRID=YES -te -5000000 -5000000 5000000 5000000 -tr 4000 4000 -overwrite'
#		
#		# process these files
#		inputFile = 'HDF4_SDS:SEAWIFS_L2:"' + iFile + '":' + band
#		outputFile = oDir + band + '.tif'
#		
#				
#		# convert command to list of strings
#		gdalCommandList = gdalCommand.split(' ')
#		# add input and output files to the list
#		gdalCommandList += [inputFile, outputFile]
#		
#		#print gdalCommandList
#		
#		# execute the command
#		status = subprocess.call(gdalCommandList)        
