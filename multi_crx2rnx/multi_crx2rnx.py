# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 21:47:25 2020

@author: sunpuyu
"""

import os

# =============================================================================
# 调用cmd命令进行d文件转换
# =============================================================================
def call_crx2rnx_(dfilename):
    cmd = 'crx2rnx %s' % (dfilename)
    print (cmd)
    os.system(cmd)
    
    
# 遍历文件夹
def walkFile(file):
    for root, dirs, files in os.walk(file):

        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list

        # 遍历文件
        for f in files:
            print(os.path.join(root, f))

        # 遍历所有的文件夹
        for d in dirs:
            print(os.path.join(root, d))
    
    return root, dirs, files


if __name__ == "__main__":
    root_path = r'E:/固定解PPP测试数据/ceshi'
    
    root, dirs, files=walkFile(root_path)
    for file in files:
        fname=root+'/'+file
        print(fname)
        if fname[-1]=='d':
            call_crx2rnx_(fname)