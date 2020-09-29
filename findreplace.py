# -*- coding:utf8 -*-
import xlrd,os
import sys
def rep(rawstr, dict_rep):
    for i in dict_rep:
        rawstr = rawstr.replace(i, dict_rep[i])
    return rawstr

def txtreplace(txtold,sheetname):
    f1 = open(txtold,"r")
    content = f1.read()
    f1.close()
    filePath = os.path.join(os.getcwd(), sheetname)
    x1 = xlrd.open_workbook(filePath)
    st = x1.sheet_by_index(0)
    old = [(str(st.cell_value(i, 0))).strip() for i in range(0, st.nrows)]
    new = [(str(st.cell_value(i, 1))).strip() for i in range(0, st.nrows)]
    dic = dict(map(lambda x,y:[x,y],old,new))
    for k in list(dic.keys()):
        if not dic[k]:
            del dic[k]
    print (dic)
    return  content,dic
'''
def rep(rawstr, dict_rep):
    for i in dict_rep:
        rawstr = rawstr.replace(i, dict_rep[i])
    return rawstr


print (rep(content,dic))
'''
if __name__ == '__main__':
    txtold="scripte.txt"
    createname=txtold.split('.')[0]
    stname="replace.xlsx"
    dicnew=txtreplace(txtold,stname)
    with open((createname+'finish.txt'),'w',encoding="utf8") as f:
        f.write(rep(dicnew[0],dicnew[1]))
