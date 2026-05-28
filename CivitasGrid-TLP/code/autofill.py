import rasterio
import numpy as np
import math as math
arcsec = round(1.0/3600.0, 8)
arcmin = round(1.0/60.0, 8)
arcsec, arcmin
#/Volumes/Winston_Elements/Data/SCPKU ML/Data/VIIRS Nighttime Light/2015/2015.dat.tif
#lon和lat的標準格式可以是小數也可以是三個數字的字符串

def getavgviirs(lon_min, lat_min, lon_max, lat_max, year):
    #數據格式化函數
    def dms_to_decimal(a):
        a = a.split(' ')
        sign = 0
        if a[0][0] == '-':
            sign = 1
            a[0] = list(a[0])
            a[0].pop(0)
            a[0] = ''.join(a[0])
        else:
            pass
        a_output = (float(a[0]) + float(a[1]) * arcmin + float(a[2]) * arcsec)
        if sign:
            a_output = -a_output
        return a_output

    #數據格式化成小數

    if lon_min == None or lat_min == None or lat_max == None or lon_max == None or year == None:
        raise ValueError("Input is None")
    try:
        lon_min = float(lon_min)
        lat_min = float(lat_min)
        lon_max = float(lon_max)
        lat_max = float(lat_max)
    except ValueError:
        lon_max = dms_to_decimal(lon_max)
        lat_max = dms_to_decimal(lat_max)
        lon_min = dms_to_decimal(lon_min)
        lat_min = dms_to_decimal(lat_min)

    #異常值處理
    if lon_max == lon_min or lat_max == lat_min:
        raise ValueError("Degenerate grid: zero width/height")
    if lon_max <= lon_min:
        lon_max, lon_min = lon_min, lon_max
    if lat_max <= lat_min:
        lat_max, lat_min = lat_min, lat_max

    sample_time = max(2,min(int(round((lat_max-lat_min)*1200.0, 0)),200))

    lat_interval = (lat_max - lat_min)/sample_time
    lon_interval = (lon_max - lon_min)/sample_time

    lat_sample = []
    lon_sample = []

    for i in range(sample_time):
        lon_sample.append(lon_min + lon_interval/2 + i*lon_interval)
    for i in range(sample_time):
        lat_sample.append(lat_min + lat_interval/2 + i*lat_interval)
    
    total = 0.0
    nodatacount = 0
    
    with rasterio.open("/Volumes/Winston_Elements/Data/SCPKU ML/Data/VIIRS Nighttime Light/"+str(year)+"/"+str(year)+".dat.tif") as src:
        nodata = src.nodata
        for i in lat_sample:
            for j in lon_sample:
                v = next(src.sample([(j, i)]))[0] 
                if v is None:
                    nodatacount += 1
                    continue
                if isinstance(v, float) and np.isnan(v):
                    nodatacount += 1
                    continue
                if v < 0:
                    nodatacount += 1
                    continue
                total += v
    if (sample_time**2 - nodatacount) == 0:
        return -9999
    else:
        avg_viirs = total / (sample_time**2-nodatacount)

    return float(avg_viirs)

    
def getavgworldpop(lon_min, lat_min, lon_max, lat_max, year):
    #數據格式化函數
    def dms_to_decimal(a):
        a = a.split(' ')
        sign = 0
        if a[0][0] == '-':
            sign = 1
            a[0] = list(a[0])
            a[0].pop(0)
            a[0] = ''.join(a[0])
        else:
            pass
        a_output = (float(a[0]) + float(a[1]) * arcmin + float(a[2]) * arcsec)
        if sign:
            a_output = -a_output
        return a_output

    #數據格式化成小數
    if lon_min == None or lat_min == None or lat_max == None or lon_max == None or year == None:
        raise ValueError("Input is None")
    try:
        lon_min = float(lon_min)
        lat_min = float(lat_min)
        lon_max = float(lon_max)
        lat_max = float(lat_max)
    except ValueError:
        lon_max = dms_to_decimal(lon_max)
        lat_max = dms_to_decimal(lat_max)
        lon_min = dms_to_decimal(lon_min)
        lat_min = dms_to_decimal(lat_min)

    #異常值處理
    if lon_max == lon_min or lat_max == lat_min:
        raise ValueError("Degenerate grid: zero width/height")
    if lon_max <= lon_min:
        lon_max, lon_min = lon_min, lon_max
    if lat_max <= lat_min:
        lat_max, lat_min = lat_min, lat_max

    sample_time = max(2, min(int(round((lat_max - lat_min) * 1200.0, 0)), 200))

    lat_interval = (lat_max - lat_min) / sample_time
    lon_interval = (lon_max - lon_min) / sample_time

    lat_sample = []
    lon_sample = []

    for i in range(sample_time):
        lon_sample.append(lon_min + lon_interval/2 + i*lon_interval)
    for i in range(sample_time):
        lat_sample.append(lat_min + lat_interval/2 + i*lat_interval)
    
    total = 0.0
    nodatacount = 0
    
    with rasterio.open("/Volumes/Winston_Elements/Data/SCPKU ML/Data/WorldPop Population/"+str(year)+"/global_pop_"+str(year)+"_CN_1km_R2025A_UA_v1.tif") as src:
        nodata = src.nodata
        for i in lat_sample:
            for j in lon_sample:
                v = next(src.sample([(j, i)]))[0]
                if v is None:
                    nodatacount += 1
                    continue
                if isinstance(v, float) and np.isnan(v):
                    nodatacount += 1
                    continue
                if v < 0:
                    nodatacount += 1
                    continue
                total += v
    
    if (sample_time**2 - nodatacount) == 0:
        return -9999
    else:
        avg_worldpop = total / (sample_time**2 - nodatacount)

    return float(avg_worldpop)
