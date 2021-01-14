# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 09:23:22 2020

@author: sunpuyu
"""

import datetime
import os, sys
import gzip
from dateutil.relativedelta import relativedelta
import xlrd


# =============================================================================
# 读取Excel文件
# =============================================================================
def readExcel(excelName,colno):
    data = xlrd.open_workbook(excelName) #打开excel
    table1 = data.sheet_by_name("Sheet1")#读sheet
    result = table1.col_values(colno)
    #print(result)
    return result

# =============================================================================
# 年月日转年积日
# =============================================================================
def ymd2doy(year, mon, day):
    dn = datetime.datetime(year, mon, day, 0, 0, 0)
    return int(dn.strftime("%j"))


# =============================================================================
# 调用cmd命令下载文件
# =============================================================================
def call_wget_(dir_dst, url):
    cmd = 'wget -c -t 0  -P %s %s' % (dir_dst, url)
    print (cmd)
    os.system(cmd)

# =============================================================================
# 调用cmd命令进行d文件转换
# =============================================================================
def call_crx2rnx_(dfilename):
    cmd = 'crx2rnx %s' % (dfilename)
    print (cmd)
    os.system(cmd)

# =============================================================================
# 解压文件，并改名，返回值为新的名称（带路径）
# =============================================================================
def un_gz(file_name):
    # 获取文件新名称
    f_name = file_name[:-37]+file_name[-25:-21]+'.'+file_name[-29:-27]+'d'
    print(f_name)
    # 开始解压
    g_file = gzip.GzipFile(file_name)
    #读取解压后的文件，并写入去掉后缀名的同名文件（即得到解压后的文件）
    open(f_name, "wb+").write(g_file.read())
    g_file.close()
    return f_name
    
# =============================================================================
# 下载megx的ofile
# =============================================================================
def down_megx_ofile(year, mon, day, siteName, dir_dst):
    if not os.path.exists(dir_dst):
        os.makedirs(dir_dst)

    doy  = ymd2doy(year, mon, day)
    y_sh = year-2000 if year>=2000 else year-1900

    name = '%s_R_%d%03d0000_01D_30S_MO.crx.gz' % (siteName, year, doy)
    ofile = 'fttps://cddis.gsfc.nasa.gov/pub/gps/data/daily/%d/%03d/%02dd/%s' % (year, doy, y_sh, name)
    call_wget_(dir_dst, ofile)
    
    if os.path.exists(dir_dst+'/'+name)==True:
        print(dir_dst+'/'+name)
        f_name=un_gz(dir_dst+'/'+name)
        call_crx2rnx_(f_name)
        
        
if __name__ == "__main__":
    tm0 = datetime.datetime(2020, 1, 1, 0, 0, 0)
    tm9 = datetime.datetime(2020, 1, 1, 0, 0, 0)
    tmn = tm0
    
    excelName="E:/软件与程序/Python代码/自己的程序/down ofile wget/IGS site.xlsx"
    siteNames=[]
    siteNames=readExcel(excelName,0)

    while 1:
        dir_dst = 'C:/Users/sunpu/Desktop/2020148/obs file/megx_ofiles_%d%02d%02d' % (tmn.year, tmn.month, tmn.day)
        if (tmn - tm9).total_seconds() > 0:
            break
        print(len(siteNames))
        
        for i in range(1,len(siteNames)):
            siteName=siteNames[i]
            print(siteName)
            down_megx_ofile(tmn.year, tmn.month, tmn.day, siteName, dir_dst)
        tmn = tmn + relativedelta(days=1)








