# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 16:13:31 2020

@author: sunpuyu
"""
import datetime


# 字符串转时间------------------------------------------------
# str format："2020  3 29  0  0  0[.000000]" []表示可有可无
def str2time(strTime):
    if len(strTime)>20:#暂时未用到
        msec=int(float('0.'+strTime[20:])*1000000) #微秒
    str2=strTime[0:19]+' '+str(msec)
    return datetime.datetime.strptime(str2,'%Y %m %d %H %M %S %f')
    

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


if '__main__' == __name__:
    strTime='2020  1  1  1  2  3.456789'
    dateT=str2time(strTime)
    mjd=time2mjd(dateT)
    print(mjd)
    print(mjd2time(mjd))
    