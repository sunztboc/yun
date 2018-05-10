# -*- coding: utf-8 -*-
# 读取excel数据
# 小罗的需求，取第二行以下的数据，然后取每行前13列的数据
import xlrd
data = xlrd.open_workbook('test.xls') # 打开xls文件
table = data.sheets()[0] # 打开第一张表
nrows = table.nrows # 获取表的行数
ncols = table.ncols
#print nrows
findint =  table.col_values(3,0)
print findint
findstr = ','.join(findint)
yuanshi = table.col_values(2,0)
yuanshistr=','.join(yuanshi)
#findout = findstr.strip(' ').split(',')
#yuanshiout=yuanshistr.strip(' ').split(',')
#print yuanshiout
#print findout
numfind= len(findstr.split(','))
checkout=open('out.txt','w')
for i in range(numfind):
    print i
    findline= findstr.strip().split(',')[i]
    print findline
    if findline in yuanshistr.strip(' ').split(','):
        print "I have been find out!!!"
    else:
        print "nonono!!!!!"
        checkout.write(findline+'\n')




#    print table.row_values(i)[:13] # 取前十三列

