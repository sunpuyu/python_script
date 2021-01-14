# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 17:06:01 2020

@author: sunpuyu
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math


def blh2xyz(blh):
    a = 6378137.0
    f=1.0/298.257223563
    e=math.sqrt(2*f-f*f);
    e2 = 0.00669437999013

    lat = blh[0]
    lon = blh[1]
    height = blh[2]

    slat = np.sin(lat)
    clat = np.cos(lat)
    slon = np.sin(lon)
    clon = np.cos(lon)

    t2lat = (np.tan(lat))*(np.tan(lat))
    tmp = 1 - e*e
    tmpden = np.sqrt(1 + tmp * t2lat)
    tmp2 = np.sqrt(1 - e*e*slat*slat)
    N=a/tmp2

    x = (N+height)*clat*clon
    y = (N+height)*clat*slon
    z = (a*tmp*slat) / tmp2 + height * slat
    return [x,y,z]


def xyz2enu( xyz,  orgblh):

    lat = orgblh[0]
    lon = orgblh[1]
    height = orgblh[2]

    slat = np.sin(lat)
    clat = np.cos(lat)
    slon = np.sin(lon)
    clon = np.cos(lon)

    tmpxyz=[0,0,0]
    orgxyz=[0,0,0]
    tmporg=[0,0,0]
    difxyz= [0,0,0]
    enu=[0,0,0]

    orgxyz=blh2xyz(orgblh)


    for i in range(3):
        tmpxyz[i] = xyz[i]
        tmporg[i] = orgxyz[i]
        difxyz[i] = tmpxyz[i] - tmporg[i]

    R_list = [[-slon,clon,0] , [-slat * clon,-slat * slon,clat ], [clat*clon,clat*slon,slat ] ]

    for i in range(3):
        enu[0] = enu[0] + R_list[0][i] * difxyz[i]
        enu[1] = enu[1] + R_list[1][i] * difxyz[i]
        enu[2] = enu[2] + R_list[2][i] * difxyz[i]
    return enu
    

        

def xyz2blh(xyz):  # 空间直角坐标转换为大地坐标
    blh=[0,0,0]
    # 长半轴
    a = 6378137.0
    # 扁率
    f = 1.0/298.257223563
    e2=f*(2-f)
    r2=xyz[0]*xyz[0]+xyz[1]*xyz[1]
    z=xyz[2]
    zk=0.0
    v=0.0
    while(abs(z-zk)>=0.0001):
        zk=z;
        sinp=z/math.sqrt(r2+z*z);
        v=a/math.sqrt(1.0-e2*sinp*sinp);
        z=xyz[2]+v*e2*sinp;
        
    if(r2>1E-12):
        blh[0]=math.atan(z/math.sqrt(r2))
        blh[1]=math.atan2(xyz[1],xyz[0])
    else:
        if(r2>0):
            blh[0]=math.pi/2.0
        else:
            blh[0]=-math.pi/2.0
        blh[1]=0.0
    
    blh[2]=math.sqrt(r2+z*z)-v
        
    return blh

def getSnxPos(snxPath,siteName):
    Esti=False
    snxPos=[0,0,0]
    with open(snxPath) as fp:
        for ln in fp.readlines():
            if(ln.find("+SOLUTION/ESTIMATE")>=0):
                Esti=True
            if(Esti==False):
                continue
            if(ln.find(siteName.upper())>=0 or ln.find(siteName.lower())>=0):
                if(ln.find("STAX")>=0):
                    snxPos[0]=float(ln[47:69])
                if(ln.find("STAY")>=0):
                    snxPos[1]=float(ln[47:69])
                if(ln.find("STAZ")>=0):
                    snxPos[2]=float(ln[47:69])
    return snxPos

def readPosFile(fpath,snxPos,t,istart=500,iend=2880):
    time=[] #记录时间
    pos_n=[]
    pos_e=[]
    pos_u=[]
    pos_ts=[] #指定时刻t的偏差
    convEpoch=-1 #收敛(<10cm)历元
    aveENU=[0,0,0]
    sumAveI=0
    xyz=[0,0,0]
    enu=[]
    blh0=xyz2blh(snxPos)
    #print(blh0)
    xyz2=blh2xyz(blh0)
    #print(xyz2)
    
    i=0
    with open(fpath) as fp:
        for ln in fp.readlines():
            
            if(len(ln.strip())<100):
                continue
            time.append(i)
            xyz[0]=(float(ln[34:48]))
            xyz[1]=(float(ln[49:63]))
            xyz[2]=(float(ln[64:78]))
            enu=xyz2enu(xyz,blh0)
            
            #存储enu
            pos_e.append(enu[0])
            pos_n.append(enu[1])
            pos_u.append(enu[2])
            
            #输出指定历元的偏差
            for it in t:
                if(i==it):
                    posStr='epoch:{0:04d}, ENU:{1: .4f}, {2: .4f}, {3: .4f} '.format(it,enu[0],enu[1],enu[2])
                    pos_ts.append(posStr)
            
            #计算收敛时间 小于10cm
            if enu[0]<=0.10 and enu[1]<=0.10 and enu[2]<=0.10:
                if convEpoch<0:
                    convEpoch=i
            elif convEpoch>=0 and i-convEpoch<10:
                convEpoch=-1
                    
            #下一个历元
            i=i+1
            
            #取istart到iend之间的均值
            if i>=istart and i<=iend:
                sumAveI=sumAveI+1
                aveENU[0]=aveENU[0]+enu[0]
                aveENU[1]=aveENU[1]+enu[1]
                aveENU[2]=aveENU[2]+enu[2]
                
    aveENU[0]=aveENU[0]/sumAveI
    aveENU[1]=aveENU[1]/sumAveI
    aveENU[2]=aveENU[2]/sumAveI
    return time,pos_e,pos_n,pos_u,pos_ts,convEpoch,aveENU

if __name__ == "__main__":
    # read gamp pos file
    fpath=r"C:\Users\sunpu\Desktop\2018063 bia\result_fix\aggo0630.18o.pos"
    snxPath=r"C:\Users\sunpu\Desktop\2018063 bia\igs18P19910_all.snx"
    #snxPos=[-2.27982902547736e+06,5.00470647928423e+06,3.21977740804160e+06]
    
    #从snx文件中获取坐标
    siteName=fpath[-16:-12]
    snxPos=getSnxPos(snxPath,fpath[-16:-12])
    
    #读取POS文件
    epochi=[60,120,300,500,1200] #要输出结果的历元
    time,pos_e,pos_n,pos_u,pos_ts,convEpoch,aveENU=readPosFile(fpath,snxPos,epochi,500,2800)
    for ti in range(len(epochi)):
        print(pos_ts[ti])
    
    # Data for plotting
    #fig, ax = plt.subplots()
    plt.plot(time,pos_e,label="E")
    plt.plot(time,pos_n,label="N")
    plt.plot(time,pos_u,label="U")
    plt.legend() #让图例生效
    
    #添加标注
    strText='convEpoch : {0}\naveE = {1: .2f} cm\naveN = {2: .2f} cm\naveU = {3: .2f} cm'.format(convEpoch,aveENU[0]*100,aveENU[1]*100,aveENU[2]*100)
    plt.text(x=1500,#文本x轴坐标 横纵坐标的刻度
        y=1.0, #文本y轴坐标
        s=strText, #文本内容
        ha='left',#参数x的位置
        va='baseline',#参数y的位置
        fontdict=dict(fontsize=10, color='r',family='serif',weight='normal'),#字体属性设置
        bbox={'facecolor': '#74C476', 'edgecolor':'b','alpha': 1, 'pad': 8}#添加文字背景色
        )
    
    plt.xlabel('Epoch') #x轴标签
    plt.ylabel('Deviation (m)') #y轴标签
    plt.title('PPP') #标题
    plt.grid(axis='y',linestyle='--')
    
    plt.savefig("./test.png", dpi=360)
    plt.show()