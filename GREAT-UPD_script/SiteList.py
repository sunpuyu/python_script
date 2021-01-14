# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 17:45:58 2020

@author: sunpuyu
"""
import os


if __name__ == "__main__":
    infolder=r'C:\Users\sunpu\Desktop\2020089fcb\ambupd'
    siteListPath = r'C:\Users\sunpu\Desktop\2020089fcb\sitelist'
    
    #获取目录下所有文件名
    filenames = os.listdir(infolder)
    
    # Open file
    fo = open(siteListPath, "w")
    
    for srcFile in filenames:
        if srcFile.find('ambupd')>=0: #筛选文件
            fo.write(srcFile[:4]+'\n')
    
    fo.close()