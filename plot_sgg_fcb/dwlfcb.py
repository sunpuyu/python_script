# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 20:31:40 2020

@author: sunpuyu
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Data for plotting
satid=['G01','G02','G03','G05','G06','G07','G08','G09','G10','G11','G12','G13','G14','G15','G16','G17','G19','G20','G21','G22','G23','G24','G25','G26','G27','G28','G29','G30','G31','G32']

mywlfcb = [0.086,  0.915,  0.513,  0.476,  0.834,  0.890,  0.560, -0.312, -0.028,  0.237,  0.395,  0.812, -0.035,  0.346,  0.006,  0.129,  0.091,  0.604,  0.862,  0.841, -0.076,  0.797, -0.136,  0.688,  0.786,  0.339,  0.020, -0.030,  0.160,  0.241]

sggwlfcb=[0.333,  0.191, -0.115, -0.297,  0.207,  0.141, -0.106,  0.046,  0.214, -0.544, -0.396,  0.017,  0.214, -0.432,  0.312,  0.351,  0.349, -0.115,  0.143,  0.181,  0.159,  0.052,  0.097, -0.013,  0.014, -0.408,  0.219,  0.215, -0.571, -0.460]

dwlfcb=[]
for i in range(len(satid)):
    dfcb=mywlfcb[i]-sggwlfcb[i]
    dfcb=dfcb-round(dfcb)
    dwlfcb.append(dfcb)


fig, ax = plt.subplots()
ax.plot(satid, mywlfcb,'g',label='my.fcb')
ax.plot(satid, sggwlfcb,'b',label='sgg.fcb')
ax.plot(satid, dwlfcb,'r',label='difference')
plt.legend(prop={'size':20})

#设置横纵坐标的名称以及对应字体格式
font = {'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 20,
}
plt.xlabel('sat ID',font)
plt.ylabel('WL FCB (cycle)',font)

#ax.set(xlabel='sat ID', ylabel='wlfcb (cycle)')

plt.tick_params(labelsize=15) #刻度字体大小13
fig.savefig("test.png")
plt.show()
