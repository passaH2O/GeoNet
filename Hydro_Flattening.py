import os
import gdal, osr
from osgeo import ogr
import numpy as np
import pandas as pd
from scipy import stats


global d_x, d_y, g_x, g_y, nodata
d_x = [-1,-1,0,1,1,1,0,-1]
d_y = [0,-1,-1,-1,0,1,1,1]
g_x = [1.0,1.0,0.0,1.0,1.0,1.0,0.0,1.0]
g_y = [0.0,1.0,1.0,1.0,0.0,1.0,1.0,1.0]


def getnodata(rasterfn):
    global nodata
    raster = gdal.Open(rasterfn)
    band = raster.GetRasterBand(1)
    nodata = band.GetNoDataValue()
    

def raster2array(rasterfn):
    raster = gdal.Open(rasterfn)
    band = raster.GetRasterBand(1)
    array = band.ReadAsArray()
    return array


def hydro_flatten(demArray, pathArray, hfzoneArray,
                  nEndPoints,geodesicPathsCellDic):
    # Euclidean Allocation
    global d_x, d_y, g_x, g_y
    nodata = -9999
    distanceArray = np.full_like(demArray, nodata)
    allocationArray = np.zeros_like(demArray)
    distanceArray = np.where(pathArray == 1, 0, np.inf)
    totalcell_no = 0
    for i in range(nEndPoints):
        centerlineX = geodesicPathsCellDic[str(i)][1]
        centerlineY = geodesicPathsCellDic[str(i)][0]
        centerline = np.asarray([centerlineY,centerlineX])
        for j in range(centerline.shape[1]):
            allocationArray[centerline[0,j],centerline[1,j]]= totalcell_no + j+1
        totalcell_no += centerline.shape[1]
    allocationArray = np.where(pathArray == 0, np.inf, allocationArray)
##    r_x = np.full_like(demArray, nodata)
##    r_y = np.full_like(demArray, nodata)
    for row in range(distanceArray.shape[0]):
        for col in range(distanceArray.shape[1]):
            z = distanceArray[row, col]
            if z != 0:
                z_min = np.inf
                which_cell = 0
                for i in range(4):
                    x = col + d_x[i]
                    y = row + d_y[i]
                    if (x >= 0) and (x < distanceArray.shape[1]) and \
                       (y >= 0) and (y < distanceArray.shape[0]):
                        z2 = distanceArray[y,x]
                        if z2 != nodata:
                            if i == 0:
                                h = 1
                                #h = 2*r_x[y,x]+1
                            elif i == 1:
                                h = 1.414
                                #h = 2*(r_x[y,x]+r_y[y,x]+1)
                            elif i == 2:
                                h = 1
                                #h = 2*r_y[y,x]+1
                            elif i == 3:
                                h = 1.414
                                #h = 2*(r_x[y,x]+r_y[y,x]+1)
                            z2 += h
                            if z2 < z_min:
                                z_min = z2
                                which_cell = i
                if z_min < z:
                    distanceArray[row,col] = z_min
                    x = col + d_x[which_cell]
                    y = row + d_y[which_cell]
                    #r_x[row, col] = r_x[y,x] + g_x[which_cell]
                    #r_y[row, col] = r_y[y,x] + g_y[which_cell]
                    allocationArray[row, col] = allocationArray[y,x]
    for row in range(distanceArray.shape[0]-1,-1,-1):
        for col in range(distanceArray.shape[1]-1,-1,-1):
            z = distanceArray[row, col]
            if z != 0:
                z_min = np.inf
                which_cell = 0
                for i in range(4,8):
                    x = col + d_x[i]
                    y = row + d_y[i]
                    if (x >= 0) and (x < distanceArray.shape[1]) and \
                       (y >= 0) and (y < distanceArray.shape[0]):
                        z2 = distanceArray[y,x]
                        if z2 != nodata:
                            if i == 4:
                                h = 1
                                #h = 2*r_x[y,x]+1
                            elif i == 5:
                                h = 1.414
                                #h = 2*(r_x[y,x]+r_y[y,x]+1)
                            elif i == 6:
                                h = 1
                                #h = 2*r_y[y,x]+1
                            elif i == 7:
                                h = 1.414
                                #h = 2*(r_x[y,x]+r_y[y,x]+1)
                            z2 += h
                            if z2 < z_min:
                                z_min = z2
                                which_cell = i
                if z_min < z:
                    distanceArray[row,col] = z_min
                    x = col + d_x[which_cell]
                    y = row + d_y[which_cell]
                    #r_x[row, col] = r_x[y,x] + g_x[which_cell]
                    #r_y[row, col] = r_y[y,x] + g_y[which_cell]
                    allocationArray[row, col] = allocationArray[y,x]
    allocationArray = np.where(demArray==nodata,nodata,allocationArray)
    allocationArray = np.where(np.isinf(allocationArray),nodata,allocationArray)
    allocationArray = np.where(hfzoneArray == 1, allocationArray, nodata)
    totalcell_no = 0
    for i in range(nEndPoints):
        centerlineX = geodesicPathsCellDic[str(i)][1]
        centerlineY = geodesicPathsCellDic[str(i)][0]
        centerline = np.asarray([centerlineY,centerlineX])
        distance = 0
        x_list = []
        y_list = []
        for j in range(centerline.shape[1]):
            x_list.append(distance)
            if not (j == centerline.shape[1]-1):
                distance += np.sqrt((centerlineY[j+1]-centerlineY[j])**2+ \
                                    (centerlineX[j+1]-centerlineX[j])**2)
            y_list.append(np.mean(demArray[np.where(allocationArray==totalcell_no+j+1)]))
        slope, intercept,_,_,_ = stats.linregress(x_list, y_list)
        for j in range(centerline.shape[1]):
            demArray[np.where(allocationArray==totalcell_no+j+1)] = intercept+slope*x_list[j]
        totalcell_no += centerline.shape[1]
    return allocationArray, demArray


def array2raster(newRasterfn,rasterfn,array,datatype):
    global nodata
    raster = gdal.Open(rasterfn)
    geotransform = raster.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]
    cols = array.shape[1]
    rows = array.shape[0]
    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(newRasterfn, cols, rows, 1, datatype)
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
    outband = outRaster.GetRasterBand(1)
    outband.WriteArray(array)
    outband.SetNoDataValue(nodata)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromWkt(raster.GetProjectionRef())
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()


def main():
    infilepath = "H:\USDA_Deliver\Dataset\data"
    demFileName = "EMS.tif"
    demfn = os.path.join(infilepath, demFileName)
    demName = demFileName.split('.')[0]
    outfilepath = "H:\USDA_Deliver\Dataset\\results\EMS"
    pathfn = os.path.join(outfilepath, demName+'_path.tif')
    hfzfn = os.path.join(outfilepath, demName+'_hfzone.tif')
    allofn = os.path.join(outfilepath, demName+'_Allocation.tif')
    hfdemfn = os.path.join(outfilepath, demName+'_hfDEM.tif')
    streamcellFileName = os.path.join(outfilepath, demName+'_streamcell.csv')
    demArray = raster2array(demfn)
    getnodata(demfn)
    pathArray = raster2array(pathfn)
    hfzoneArray = raster2array(hfzfn)
    df = pd.read_csv(streamcellFileName, dtype={'ID':str})
    df['PathCellList'] = df['PathCellList'].apply(eval)
    NewgeodesicPathsCellDic = df.set_index('ID')['PathCellList'].to_dict()
    numberOfEndPoints = max(map(int,NewgeodesicPathsCellDic.keys()))+1
    allocationArray, hfdemArray = hydro_flatten(demArray, pathArray, hfzoneArray,
                                                numberOfEndPoints,NewgeodesicPathsCellDic)
    array2raster(allofn,demfn,allocationArray,gdal.GDT_Float32)
    array2raster(hfdemfn,demfn,hfdemArray,gdal.GDT_Float32)
    

if __name__ == "__main__":
    main()
