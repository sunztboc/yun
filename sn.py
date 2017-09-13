#coding:utf8
import os
import os.path
import xlwt
import xlrd
#  --- 获取当前路径 ---
filePath=os.getcwd()
#  --- 指定测试路径 ---
file01='D:\python'
#  --- 开始特定标识 ---
startSign='PID: '
#  --- 结束特定标识 ---
endSign='SN: '
#  --- 创建表格 ---
getWordExcel=xlwt.Workbook()
#  --- 创建 Sheet ---
getTable=getWordExcel.add_sheet('getword',cell_overwrite_ok=True)
#  --- 行数 ---
index = 0
#  --- 遍历相应路径下的 parent ：父目录 dirnames 所有文件夹 filenames 所有文件名 ---
for parent,dirnames,filenames in os.walk(filePath):
    #  --- 遍历所有文件 ---
    for filename in filenames:
        #  --- 设置/获取 当前文件父目录 ---
        totalFilePath=os.path.join(parent,filename)
        #  --- 获取后缀为 .cs 或者 .txt的文件 ---
        if filename.endswith('.txt') or filename.endswith('.xls'):
            #  --- 获取文件全路径 ---
            totalFile=os.path.abspath(totalFilePath)
            #  --- 打开读取文件 'r' 为读取  'w' 为写入
            fileInfo02=open(totalFilePath,'r')
            #  --- 遍历当前文件查看每一行 ---
            for file02 in fileInfo02:
                #  --- 去掉每行换行符 '\n' ---
                file02 = file02.strip('\n')
                #  --- 判断开始标识 与 结束标识是否存在于当前行中 ---
                if file02.endswith('#'):
                    name=file02.split('#')[0]
                    if file02.startswith('RP/'):
                        name = file02.split(':')[1]
                if startSign in file02:
                    #print file02
                    PID=file02.split(',')[0].strip(' ').split(':')[1]
                    #print PID
                    SN=file02.split(':')[-1]
                    getTable.write(index,0,name)
                    getTable.write(index,1,PID)
                    getTable.write(index, 2, SN)
                    index+=1

                    #print SN


#  --- 判断该表格是否存在 ---
if os.path.isfile(filePath+os.sep+'sun1.xls'):
    os.remove(filePath+os.sep+'sun1.xls')
getWordExcel.save(filePath+os.sep+'sun1.xls')
