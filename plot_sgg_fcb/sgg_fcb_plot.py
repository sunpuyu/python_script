# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 11:02:06 2020

@author: sunpuyu
"""

import os
import sys
import getopt
import matplotlib.pyplot as plt


maxGpsNum=32
maxBdsNum=60
maxGloNum=27
maxGalNum=40
maxSatNum=maxGpsNum+maxBdsNum+maxGloNum+maxGalNum #最大卫星个数

#求天内秒 str格式为："2020  3 29  0  0  0"
def str2SecOfDay(strTime):
    H=int(strTime[11:13])
    M=int(strTime[14:16])
    S=int(strTime[17:19])
    return (H*3600+M*60+S)
    

#卫星编号
def satno(sid):
    sys=sid[0]
    prn=int(sid[1:3])
    if sys=='G':
        return prn-1
    if sys=='C':
        return maxGpsNum+prn-1
    if sys=='R':
        return maxBdsNum+maxGpsNum+prn-1
    if sys=='E':
        return maxGloNum+maxBdsNum+maxGpsNum+prn-1
    return -1

#求卫星id
def satid(sn):
    if sn>=maxGloNum+maxBdsNum+maxGpsNum:
        sys='E'
        prn=sn-(maxGloNum+maxBdsNum+maxGpsNum)+1
        return (sys+str(prn))
    if sn>=maxBdsNum+maxGpsNum:
        sys='R'
        prn=sn-(maxBdsNum+maxGpsNum)+1
        return (sys+str(prn))
    if sn>=maxGpsNum:
        sys='C'
        prn=sn-maxGpsNum+1
        return (sys+str(prn))
    if sn>=0:
        sys='G'
        prn=sn+1
        return (sys+str(prn))
    return ''

#读fcb文件记录窄巷fcb
def read_nlfcb(fpath):
    fcb_sat=[[]for i in range(maxSatNum)]#定义二维数组记录fcb（maxSatNum个一维数组）
    time=[[]for i in range(maxSatNum)]#定义二维数组记录时间
    i=0
    
    #读文件
    with open(fpath) as fp:
        for ln in fp.readlines():
            if(ln.find('END OF HEADER')>=0):
                i=i+1
            if i<0:
                continue
            if(ln[0]=='*'):
                t=str2SecOfDay(ln[2:22])
                continue
            if(ln[0]=='P'):
                sn=satno(ln[1:4])
                if(sn<0):#去掉其他系统的数据
                    continue
                fcb_sat[sn].append(float(ln[20:30]))
                time[sn].append(t)
    fp.close()
    return time,fcb_sat

def usage():
    print ("                                                                           ")
    print ("    Purpose: fcb plot                                         ")
    print ("    Usage: python  sgg_fcb_plot.py  -c  <file> (or -f=<file>)       ")
    print ("                                                                           ")

if __name__ == "__main__":
    #fcb路径
    fpath=r""
    
    # Get Arguments
    try:
        opts,args = getopt.getopt(sys.argv[1:],"hc:",["help","f="])
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    # print(opts)

    for opt,arg in opts:
        if opt in ("-c","-f"):
            fpath = arg
        elif opt in ("-h","--help"):
            usage()
            sys.exit(1)

    # Program Terminated due to Incomplete Arguments
    if fpath=="" :
        usage()
        sys.exit(1)
    
    time,fcb_sat=read_nlfcb(fpath)
    
    fig, ax = plt.subplots(1, 1)
    #fig.suptitle('FCB')
    
    for i in range(maxSatNum):
        if len(time[i])<1:
            continue
        ax.scatter(time[i], fcb_sat[i],s=20,label=satid(i))
    
    #设置横纵坐标的名称以及对应字体格式
    font = {'family' : 'Times New Roman',
    'weight' : 'normal',
    'size'   : 20,
    }
    ax.set_xlabel('TIME (s)',font)
    ax.set_ylabel('NL FCB(cycle)',font)
    #图例参数设置 bbox_to_anchor的左值为左右，右值为高低
    plt.legend(bbox_to_anchor=(1.06, 1.0), loc=0, borderaxespad=0,ncol=1) 
    
    plt.show()