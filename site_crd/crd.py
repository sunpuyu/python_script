# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 23:58:45 2020

@author: sunpuyu
"""
import math

class site():
    sitename=''
    x=0
    y=0
    z=0
    
def pos2ecef(lat,long,height):
    sinp=math.sin(lat)
    cosp=math.cos(lat)
    sinl=math.sin(long)
    cosl=math.cos(long)
    FE_WGS84=1.0/298.257223563
    RE_WGS84=6378137.0 
    e2=FE_WGS84*(2.0-FE_WGS84)
    v=RE_WGS84/math.sqrt(1.0-e2*sinp*sinp)
    
    x=(v+height)*cosp*cosl
    y=(v+height)*cosp*sinl
    z=(v*(1-e2)+height)*sinp
    return x,y,z
    

sec2rad=math.pi/180.0
sites=[]
    
sitepath = "C:/Users/sunpu/Desktop/Python绘图/自己的程序/site crd/sitepos.txt"


with open(sitepath) as fp:
    for ln in fp.readlines():
        info = ln.split()
        print(info)
        
        s=site()
        s.sitename=(info[0][0:4]).lower()
        lat  = float(info[1])
        lon  = float(info[2])
        height=float(info[3])
        s.x,s.y,s.z=pos2ecef(lat*sec2rad,lon*sec2rad,height)
        sites.append(s)

print(len(sites))
crdfile=open('site.crd','w')

for s in sites:
    crdfile.write("%s%14.4f%14.4f%14.4f\n" %(s.sitename,s.x,s.y,s.z))
    
crdfile.close()