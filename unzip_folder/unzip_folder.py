import os
import gzip


#解压指定文件
def unzipFile(srcFile,dstFile):
    # 开始解压
    g_file = gzip.GzipFile(srcFile)
    #读取解压后的文件，并写入去掉后缀名的同名文件（即得到解压后的文件）
    open(dstFile, "wb+").write(g_file.read())
    g_file.close()


#解压文件夹下的所有文件
def unzipFolder(filePath,batPath):
    filenames = os.listdir(filePath)#获取目录下所有文件名
    # Open a file
    fo = open(batPath, "w")
    for srcFile in filenames:
        #目标文件名
        if len(srcFile)>15:
            dstFile=srcFile[0:4].lower()+srcFile[16:20]+'.'+srcFile[14:16]+'d'
        else:
            continue
        #记录所有解压后的文件
        fo.write('crx2rnx '+dstFile+'\n')
        #文件的绝对路径=文件名+路径
        srcFile = os.path.join(filePath,srcFile)
        dstFile = os.path.join(filePath,dstFile)
        #解压
        unzipFile(srcFile,dstFile)
        #删除原始文件
        os.remove(srcFile)
    # Close opend file
    fo.close()


if __name__ == '__main__':
    filePath=r'C:\Users\sunpu\Desktop\2020089\obs file'
    batPath=filePath+'\\rinex.bat'
    unzipFolder(filePath,batPath)
    
	