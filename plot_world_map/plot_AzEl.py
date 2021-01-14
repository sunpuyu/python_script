# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 18:55:27 2020

@author: sunpuyu
"""

# copyright
# @Pan Li. Email:lipan.whu@gmail.com
# @Jiahuan Hu. Email:hhu@whu.edu.cn

import os
import math
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

class Satpos_base_t:
    def __init__(self):
        self.id = 'X00'
        self.csys  = 'X'
        self.prn   = 0
        self.x   = 0.0
        self.y   = 0.0
        self.z     = 0.0

class Satpos_1ep:
    def __init__(self):
        self.tm   = ''
        self.inf_fbs = []


def ecef2blh(x,y,z):
    e2=(1.0/298.257223563)*(2-(1.0/298.257223563))
    v=6378137.0
    r2=x*x+y*y

    b=math.atan(z/(math.sqrt(r2)))
    l=math.atan2(y,x)
    h=math.sqrt(r2+z*z)-v

    return b,l,h

def xyz2enu(b,l,h):
    sinp=math.sin(b)
    cosp=math.cos(b)
    sinl=math.sin(l)
    cosl=math.cos(l)
    E0=-sinl
    E1=-sinp*cosl
    E2=cosp*cosl
    E3=cosl
    E4=-sinp*sinl
    E5=cosp*sinl
    E6=0.0
    E7=cosp
    E8=sinp
    return E0,E1,E2,E3,E4,E5,E6,E7,E8

def ecef2enu(b,l,h,Ex,Ey,Ez):

    E=xyz2enu(b,l,h)
    ENUe=E[0]*Ex+E[3]*Ey+E[6]*Ez
    ENUn=E[1]*Ex+E[4]*Ey+E[7]*Ez
    ENUu=E[2]*Ex+E[5]*Ey+E[8]*Ez
    return ENUe,ENUn,ENUu



def pos2ecef(b,l,h):
    sinp=math.sin(b)
    cosp=math.cos(b)
    sinl=math.sin(l)
    cosl=math.cos(l)
    e2=(1.0/298.257223563)*(2-(1.0/298.257223563))
    v=6378137.0/math.sqrt(1-e2*sinp*sinp)

    x=(v+h)*cosp*cosl
    y=(v+h)*cosp*sinl
    z=(v*(1-e2)+h)*sinp

    return x,y,z


def averagenum(num):
    nsum=0
    for i in range(len(num)):
        nsum+=num[i]

    return nsum/len(num)


def  readsp3file(fpath):
    fp=open(fpath)
    f_Eps=[]
    ln=fp.readline()
    while ln:
        if '*' ==ln[0]:
            fEp=Satpos_1ep()
            while 1:
                ln=fp.readline()
                if not ln:
                    break
                if  '*' ==ln[0]:
                    break
                if 'P'!=ln[0]:
                    continue
                strs=ln.split()

                ss=strs[0][1:]
                ch=ss[0]
                prn=int(strs[0][2:])

                x=float(strs[1])*1000
                y=float(strs[2])*1000
                z=float(strs[3])*1000

                Satp=Satpos_base_t()
                Satp.id=ss
                Satp.sys=ch
                Satp.prn=prn
                Satp.x=x
                Satp.y=y
                Satp.z=z
                fEp.inf_fbs.append(Satp)
            f_Eps.append(fEp)
        else:
            ln=fp.readline()
    fp.close()
    return f_Eps


def count_ns_el_az(Satposs,blh):

    b = blh[0]*(math.pi/180)
    l = blh[1]*(math.pi/180)
    h = blh[2]
    Rexyz=pos2ecef(b,l,h)
    Rx=Rexyz[0]
    Ry=Rexyz[1]
    Rz=Rexyz[2]

    To_nsat=[]
    EP_nsat=[]
    AZ_sum=[]
    EL_sum=[]

    for fE0 in Satposs:
        n_sat = 0
        EL = []
        AZ = []
        ID=[]
        i=0
        for fb in fE0.inf_fbs:
            i+=1
            Sx=fb.x
            Sy=fb.y
            Sz=fb.z

            r = math.sqrt((Rx-Sx) * (Rx-Sx) + (Ry-Sy) * (Ry-Sy) +(Rz-Sz) * (Rz-Sz))

            Ex=(Sx-Rx)/r
            Ey=(Sy-Ry)/r
            Ez=(Sz-Rz)/r

            ENU=ecef2enu(b,l,h,Ex,Ey,Ez)
            el=math.asin(ENU[2])*180/math.pi
            az=math.atan2(ENU[0],ENU[1])
            if az<0:
                az+=2*math.pi

            EL.append(el)
            AZ.append(az)
            ID.append(fb.id)

            if el>0.0:
                n_sat=n_sat+1
            else:
                continue

        EL_sum.append(EL)
        AZ_sum.append(AZ)

        EP_nsat.append(n_sat)
    E_nsat=averagenum(EP_nsat)
    return E_nsat,EL_sum,AZ_sum,ID


if __name__ == "__main__":
    
    fpath=r'C:\Users\sunpu\Desktop\2018063 fcb\gbm19910.sp3'
    site_blh=[-19.01830, 47.22921, 1552.9369] #测站的blh（角度）
    
    Total=[]
    N_sat = []
    EL=[]
    AZ=[]
    ID=[]
    
    #读sp3文件
    Satposs=readsp3file(fpath)
    nsat,EL,AZ,ID=count_ns_el_az(Satposs,site_blh)

    Nepoch=len(EL)
    Nsat=len(EL[0])

    # 绘图
    ax=plt.subplot(111,projection='polar')

    for ep in range(1,Nepoch):
        for sat in range(1,Nsat):
            if EL[ep-1][sat-1]>0:
                if ID[sat-1]=='G01':
                    theta=float(AZ[ep-1][sat-1])
                    r=90-float(EL[ep-1][sat-1])
                    c=ax.scatter(theta,r,s=15,color='b',marker=".")
                    #print('ep:%2d '%ep,ID[sat-1])

    ax.tick_params('y',labelleft=False)
    plt.savefig('./skyplot.jpg', dpi=360)
    plt.show()




