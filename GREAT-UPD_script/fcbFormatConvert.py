# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 19:02:13 2020

@author: sunpuyu
"""

import datetime
import math
import pandas as pd


pd.options.display.max_columns=12  #展示12列数据，超过12列，则以省略号显示
pd.options.display.max_rows=10 #展示10行数据，超过10行，则以省略号显示
pd.options.display.width=20000  #界面宽度扩展值20000

MAXSATNUM=35

# 字符串转时间------------------------------------------------
# str format："2020  3 29  0  0  0[.000000]" []表示可有可无
def str2time(strTime):
    if len(strTime)>20:
        msec=int(float('0.'+strTime[20:])*1000000) #微秒
    str2=strTime[0:19]+' '+str(msec)
    return datetime.datetime.strptime(str2,'%Y %m %d %H %M %S %f')
    
def time2str(dateTime):
    strMsec='{: >8.06f}'.format(dateTime.microsecond/1000000.0)
    strTime='{0.year: >4d} {0.month: >2d} {0.day: >2d} {0.hour: >2d} {0.minute: >2d} {0.second: >2d}'.format(dateTime)
    strTime=strTime+strMsec[1:8]
    return strTime

#datetime类转mjd
def time2mjd(dateT):
    t0=datetime.datetime(1858,11,17,0,0,0,0)#简化儒略日起始日
    mjd=(dateT-t0).days
    mjd_s=dateT.hour*3600.0+dateT.minute*60.0+dateT.second+dateT.microsecond/1000000.0
    return mjd+mjd_s/86400.0

#mjd转datetime类
def mjd2time(mjd):
    t0=datetime.datetime(1858,11,17,0,0,0,0)#简化儒略日起始日
    return t0+datetime.timedelta(days=mjd)

#mjd和jd互转
def mjd2jd(mjd):
    return mjd+2400000.5

def jd2mjd(jd):
    return jd-2400000.5

# 记录一个历元一颗卫星的fcb
class fcb_sat():
    def __init__(self):
        self.sys=''
        self.prn=0
        self.val=0.0
        self.var=0.0

#记录一个历元所有卫星的fcb
class fcb_epoch():
    def __init__(self):
        self.mjd=0
        self.mjd_s=0
        self.fcbs=[]



#读入fcb文件（李星星格式）
def read_nl_lxx(filesPath):
    fcbeps=[]
    sw=False #当前历元的时间已经出现过则为True
    
    fcb_i=-1
    
    for fpath in filesPath:#逐文件
        with open(fpath) as fp:#打开文件
            for ln in fp.readlines():#逐行
                if ln.find('EOF')>=0:#结尾
                    break
                if ln.find('EPOCH-TIME')>=0:#时间
                    sw=False
                    fcb_i=-1
                    mjd=int(ln[14:19])
                    mjd_s=float(ln[21:])
                    #查找之前的历元有没有跟当前历元时间一致的（合并时间）
                    for fi in fcbeps:
                        fcb_i=fcb_i+1
                        if fi.mjd==mjd and abs(fi.mjd_s-mjd_s)<1:
                            sw=True
                            break
                    if(sw==True):
                        continue
                    #没有相同时间的历元就新建一个历元
                    fcb_t=fcb_epoch()
                    fcb_t.mjd=int(ln[14:19])
                    fcb_t.mjd_s=float(ln[21:])
                    fcb_t.fcbs.clear()
                    fcbeps.append(fcb_t)
                    fcb_i=len(fcbeps)-1
                    continue
                
                #无效行
                if ln[0]=='x' or ln[0]=='%':
                    continue
                
                if ln[1]=='G' or ln[1]=='C' or ln[1]=='E' or ln[1]=='R' :
                    #一颗卫星的fcb
                    fcb=fcb_sat()
                    fcb.sys=ln[1]
                    fcb.prn=int(ln[2:4])
                    fcb.val=float(ln[12:22])
                    fcb.var=float(ln[22:32])
                    #print(fcb_i)
                    #print(fcb.sys)
                    fcbeps[fcb_i].fcbs.append(fcb)
                    
        fp.close()
        
    return fcbeps


#读入宽巷fcb（李星星格式）
def read_wl_lxx(filesPath):
    fcbs=[]
    for fpath in filesPath:#逐文件
        with open(fpath) as fp:#打开文件
            for ln in fp.readlines():#逐行
                if ln.find('EOF')>=0:#结尾
                    break
                
                #无效行
                if ln[0]=='x' or ln[0]=='%':
                    continue
                
                fcb=fcb_sat()
                fcb.sys=ln[1]
                fcb.prn=int(ln[2:4])
                fcb.val=float(ln[12:22])
                fcb.var=float(ln[22:32])
                fcbs.append(fcb)
        fp.close()
        
    return fcbs

# 求加权平均值 val为值，var为该值的均方差（标准差）
def weightMean(val,var):
    sumPower=0.0
    sumVal=0.0
    Var2=1.0 #加权平均后的标准差
    if len(val)!=len(var):
        print("weightMean function: 请检查输入的值!")
        return 0
    
    #求加权均值
    for i in range(len(val)):
        power=1.0/var[i]/var[i]
        sumVal=sumVal+val[i]*power
        sumPower=sumPower+power
    aveVal=sumVal/sumPower
    
    #求加权均值的标准差
    for i in range(len(val)):
        power=1.0/var[i]/var[i]
        Var2=Var2+power*(val[i]-aveVal)*(val[i]-aveVal)
    Var2=math.sqrt(Var2/len(val)/sumPower)
    
    return aveVal,Var2


#按指定间隔interval(unit:second)合并fcb值
def conbineFcbTime(nlfcbs,interval=900):
    nlfcbs_res=[]
    iStart=0
    iEnd=0
    index=0
    for epfcbi in range(len(nlfcbs)):
        Time0=mjd2time(nlfcbs[iStart].mjd+nlfcbs[iStart].mjd_s/86400.0)
        Time=mjd2time(nlfcbs[epfcbi].mjd+nlfcbs[epfcbi].mjd_s/86400.0)
        if (Time-Time0).seconds<interval: #判断时间
            index=index+1
            continue
        else:
            iEnd=index
            index=index+1
        
        #print(iStart)
        #合并时间
        satFcbVal = [[] for si in range(MAXSATNUM)]
        satFcbVar = [[] for si in range(MAXSATNUM)]
        for i in range(iStart,iEnd):
            for satfi in nlfcbs[i].fcbs:
                satFcbVal[satfi.prn].append(satfi.val)
                if math.fabs(satfi.var)<0.00001:
                    satFcbVar[satfi.prn].append(1.0)
                else:
                    satFcbVar[satfi.prn].append(satfi.var)
                
        epochFcb=fcb_epoch()
        epochFcb.mjd=nlfcbs[iStart].mjd
        epochFcb.mjd_s=nlfcbs[iStart].mjd_s
        
        for j in range(MAXSATNUM):
            if len(satFcbVal[j])<=0:
                continue
            satf=fcb_sat()
            satf.sys='G'
            satf.prn=j
            satf.val,satf.var=weightMean(satFcbVal[j],satFcbVar[j])
            epochFcb.fcbs.append(satf)
            
        nlfcbs_res.append(epochFcb)
        iStart=iEnd
        #epfcbi=epfcbi-1
    
    return nlfcbs_res


#写入到fpath中fcb数据（sgg格式）
def write_sgg_fcb(wlfcbs,nlfcbs,fpath):
    firstTime=mjd2time(nlfcbs[0].mjd+nlfcbs[0].mjd_s/86400.0)
    
    # Open a file
    fo = open(fpath, "w")
    #写入宽巷fcb
    fo.write("Widelane Satellite Fractional Cycle Biases                  COMMENT\n")
    fo.write('* {0}    86400.0                     COMMENT\n'.format(time2str(firstTime)))
    for wl in wlfcbs:
        fo.write('WL  {0}{1:0>2d}  2{2: >10.03f}{3: >10.03f}                              COMMENT\n'.format(wl.sys,wl.prn,wl.val,wl.var))
    fo.write('                                                            END OF HEADER\n')
    
    #写入窄巷fcb
    for ei in nlfcbs:
        Time=mjd2time(ei.mjd+ei.mjd_s/86400.0)
        fo.write('* '+time2str(Time)+'\n')
        for nl in ei.fcbs:
            fo.write('P{0}{1:0>2d}                {2: >10.03f}                    {3: >10.03f}\n'.format(nl.sys,nl.prn,nl.val,nl.var))
            
    # Close opend file
    fo.close()
    
    

if __name__ == "__main__":
    #宽巷fcb
    folder=r'C:\Users\sunpu\Desktop\2018063fcb\result' #输入路径
    
    wlfiles=[folder+r'\upd_wl_2018063_G']
             #folder+r'\upd_wl_2020001_E',
             #folder+r'\upd_wl_2020001_C'
    wlfcbs=read_wl_lxx(wlfiles)
    print('已读取所有宽巷文件！')
    
    #窄巷fcb
    nlfiles=[folder+r'\upd_nl_2018063_G']
             #folder+r'\upd_nl_2020001_E',
             #folder+r'\upd_nl_2020001_C']
    
    nlfcbs=read_nl_lxx(nlfiles)
    print('已读取所有窄巷文件！')
    
    #按指定间隔合并fcb的值
    interval=900
    nlfcbs_=conbineFcbTime(nlfcbs,interval)
    print('已按指定时间间隔合并窄巷数据！')
    
    #写入文件
    resultPath=r'C:\Users\sunpu\Desktop\2018063 bia\fcb\sun.fcb' #输出路径
    write_sgg_fcb(wlfcbs,nlfcbs_,resultPath)
    print('已将数据写入到文件中!')
    print('Normal End!')