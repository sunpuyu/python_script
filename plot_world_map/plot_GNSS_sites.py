# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 17:18:40 2020

@author: sunpuyu
"""

# Feel free to use or modify this script.
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np


#===========读站点坐标，只要有站点名称、经度、纬度就可以，注意文件格式
def readSiteCrd(pospath):
    sites = []
    lats  = []
    lons  = []
    with open(pospath) as fp:
        for ln in fp.readlines():
            info = ln.split()
    
            sites.append(info[0])
            lat  = float(info[1])
            lon  = float(info[2])
            lats.append(lat)
            lons.append(lon)
    return zip(sites,lats,lons)


# resolution of boundary database to use. Can be c (crude), l (low), i (intermediate), h (high), f (full) or None.
# If None, no boundary data will be read in (and class methods such as drawcoastlines will raise an if invoked).
# Resolution drops off by roughly 80% between datasets. Higher res datasets are much slower to draw. Default c.
# Coastline data is from the GSHHS (http://www.soest.hawaii.edu/wessel/gshhs/gshhs.html).
# State, country and river datasets from the Generic Mapping Tools (http://gmt.soest.hawaii.edu).

#projection = cyl, robin, ortho

if __name__ == "__main__":
    # 站点坐标文件路径
    pospath = r"E:\Program_Code\Python_Script\my_script\plot_world_map\crd.txt"
    # 图片存储路径
    picpath = r".\map.jpg"
    
    
    # plot
    plt.figure(figsize=(10,8))
    my_map = Basemap(projection='cyl', lat_0=0, lon_0=0, resolution='i', area_thresh=5000.0)
    
    # color = gray  slategray  olive
    my_map.fillcontinents(color='white', lake_color='lightskyblue')
    my_map.drawmapboundary(fill_color='skyblue')
    
    # 绘制网格线
    #my_map.drawmeridians(np.arange(0, 360, 60), labels=[1,0,0,1])
    #my_map.drawparallels(np.arange(-90, 90.001, 30), labels=[1,0,0,1])
    
    
    for name,lat,lon in readSiteCrd(pospath):
        #print (name, lon, lat)
        plt.plot(lon, lat, marker='o', color='coral', markersize=9)
        plt.text(lon,lat,name,rotation=0,fontsize=12)
    
    print ('map have been saved to '+picpath)
    
    plt.savefig(picpath, dpi=360, bbox_inches='tight')
    plt.show()
    plt.close('all')
