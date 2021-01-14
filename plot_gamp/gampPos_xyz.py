# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 17:06:01 2020

@author: sunpuyu
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
#coding=utf-8


if __name__ == "__main__":
    
    # read gamp pos file
    fpath="C:/Users/sunpu/Desktop/2018063/result/JFNG0630.18o.pos"
    snxPos=[-2279829.02547736,5004706.47928423,3219777.40804160]
    time=[]
    pos_x=[]
    pos_y=[]
    pos_z=[]
    i=0
    with open(fpath) as fp:
        for ln in fp.readlines():
            i=i+1
            if(len(ln.strip())<100):
                #pos_x.append(20.0)
                #pos_y.append(20.0)
                #pos_z.append(20.0)
                continue
            time.append(i)
            pos_x.append(float(ln[34:48])-snxPos[0])
            pos_y.append(float(ln[49:63])-snxPos[1])
            pos_z.append(float(ln[64:78])-snxPos[2])
    
      
    
    # Data for plotting
    fig, ax = plt.subplots()
    ax.scatter(time,pos_x, s=0.01)
    ax.scatter(time,pos_y, s=0.01)
    ax.scatter(time,pos_z, s=0.01)
    
    ax.set(xlabel='time (s)', ylabel='Deviation (m)',
           title='坐标偏移')
    ax.grid()
    
    fig.savefig("test.png")
    plt.show()