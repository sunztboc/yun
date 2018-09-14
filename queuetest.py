#coding:utf8

from threading import Thread,current_thread
import time,paramiko,os,sys
import xlrd,datetime
from tqdm import *
from Queue import Queue
queue = Queue(5)
starttime = datetime.datetime.now()
reload(sys)
sys.setdefaultencoding('utf8')
def mkdir(path):
    # 引入模块
    import os
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs(path)
        #print path + ' 创建成功'
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        #print path + ' 目录已存在'
        return False

class producerthread(Thread):#定义一个类（生产者）
    starttime = datetime.datetime.now()
    '''def run1(self):
        name = current_thread().getName()
        nums = range(50)
        print nums
        global queue
        while True:
            num =random.choice(nums)
            queue.put(num)
            print('生产者%s 生产了数据%s'%(name,num))
            t= random.randint(1,3)
            time.sleep(t)
            print('生产者%s 睡眠了 %s 秒' %(name,t))'''
    name = current_thread().getName()
    print name+'+1'
    def run(self):
        global mid
        ExcelFile = xlrd.open_workbook(r'Backboneshow.xlsx')
        # 获取目标EXCEL文件sheet名
        #    print ExcelFile.sheet_names()
        sheet = ExcelFile.sheet_by_name('DeviceInfo')
        platform = ExcelFile.sheet_by_name('ShowCommand')
        nogood = open("nogood.txt", 'w')
        linenum = sheet.nrows
        N1_N9K1 = platform.col_values(2, 3)
        N1_N9K = (','.join(N1_N9K1))
        #    print N1_N9K
        N1_IOS1 = platform.col_values(3, 3)
        N1_IOS = ','.join(N1_IOS1)
        N2_N9K1 = platform.col_values(4, 3)
        N2_N9K = ','.join(N2_N9K1)
        N2_IOS1 = platform.col_values(5, 3)
        N2_IOS = ','.join(N2_IOS1)
        HW_DEV1 = platform.col_values(6, 3)
        HW_DEV = ','.join(HW_DEV1)
        #start = input('please input start line:')
        mid = int(linenum / 2)
        for i in tqdm(range(1, mid)):
            ip1 = sheet.cell_value(i, 3)
            try:
                username = "op01"
                passwd = "Ecc82973548"
                s = paramiko.SSHClient()
                s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                s.connect(hostname=ip1, username=username, password=passwd, timeout=5)
                ssh_shell = s.invoke_shell()
                # 读取命令文件
                save = sheet.cell_value(i, 2)
                print save
                curpath = os.getcwd()
                mkpath = (curpath + "\\" + sheet.cell_value(i, 9)).encode("gb2312")
                mkdir(mkpath)
                os.chdir(mkpath)
                # 执行命令
                # print sheet.cell_value(i,8)
                if sheet.cell_value(i, 8) == "N2_IOS":
                    cmdlist = N2_IOS
                elif sheet.cell_value(i, 8) == "N2_A9K":
                    cmdlist = N2_N9K
                elif sheet.cell_value(i, 8) == "N1_IOS":
                    cmdlist = N1_IOS
                elif sheet.cell_value(i, 8) == "N2_IOS":
                    cmdlist = N2_IOS
                elif sheet.cell_value(i, 8) == "N1_A9K":
                    cmdlist = N1_N9K
                else:
                    sheet.cell_value(i, 8) == "HW_DEV"
                    cmdlist = HW_DEV
                    #            cmdnum=''.join(cmdlist)
                    #            print cmdlist
                for line1 in cmdlist.strip(', ,').split(','):
                    line = line1.replace(' ', '_').replace('/', '_')
                    saveout = open((save + ".txt"), "a")
                    ssh_shell.sendall(line1 + '\n')
                    time.sleep(1)
                    config_result = ssh_shell.recv(99999).decode()
                    print (config_result)
                    # time.sleep(2)
                    saveout.write(config_result)
                    saveout.close()
                os.chdir(curpath)
                # 关闭连接
                s.close()
            except Exception, e:
                print (ip1 + " " + str(e))
                nogood.write(ip1 + " " + str(e))
                continue

    endtime = datetime.datetime.now()
    print (endtime - starttime).seconds
class consumerthread(Thread):#定义一个类（消费者）
    '''def run1(self):
    name = current_thread().getName()
        global queue
        while True:
            num =queue.get()
            queue.task_done()
            print('消费者%s 消耗了数据%s'%(name,num))
            t= random.randint(1,5)
            time.sleep(t)
            print('消费者%s 睡眠了 %s 妙' %(name,t))'''
    name = current_thread().getName()
    print name
    def run(self):
        ExcelFile = xlrd.open_workbook(r'Backboneshow.xlsx')
        # 获取目标EXCEL文件sheet名
        #    print ExcelFile.sheet_names()
        sheet = ExcelFile.sheet_by_name('DeviceInfo')
        platform = ExcelFile.sheet_by_name('ShowCommand')
        nogood = open("nogood.txt", 'w')
        linenum = sheet.nrows
        N1_N9K1 = platform.col_values(2, 3)
        N1_N9K = (','.join(N1_N9K1))
        #    print N1_N9K
        N1_IOS1 = platform.col_values(3, 3)
        N1_IOS = ','.join(N1_IOS1)
        N2_N9K1 = platform.col_values(4, 3)
        N2_N9K = ','.join(N2_N9K1)
        N2_IOS1 = platform.col_values(5, 3)
        N2_IOS = ','.join(N2_IOS1)
        HW_DEV1 = platform.col_values(6, 3)
        HW_DEV = ','.join(HW_DEV1)
        #start = input('please input start line:')
        mid = int(linenum / 2)
        for i in tqdm(range(mid, linenum)):
            ip1 = sheet.cell_value(i, 3)
            try:
                username = "op01"
                passwd = "Ecc82973548"
                s = paramiko.SSHClient()
                s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                s.connect(hostname=ip1, username=username, password=passwd, timeout=5)
                ssh_shell = s.invoke_shell()
                # 读取命令文件
                save = sheet.cell_value(i, 2)
                print save
                curpath = os.getcwd()
                mkpath = (curpath + "\\" + sheet.cell_value(i, 9)).encode("gb2312")
                mkdir(mkpath)
                os.chdir(mkpath)
                # 执行命令
                # print sheet.cell_value(i,8)
                if sheet.cell_value(i, 8) == "N2_IOS":
                    cmdlist = N2_IOS
                elif sheet.cell_value(i, 8) == "N2_A9K":
                    cmdlist = N2_N9K
                elif sheet.cell_value(i, 8) == "N1_IOS":
                    cmdlist = N1_IOS
                elif sheet.cell_value(i, 8) == "N2_IOS":
                    cmdlist = N2_IOS
                elif sheet.cell_value(i, 8) == "N1_A9K":
                    cmdlist = N1_N9K
                else:
                    sheet.cell_value(i, 8) == "HW_DEV"
                    cmdlist = HW_DEV
                    #            cmdnum=''.join(cmdlist)
                    #            print cmdlist
                for line1 in cmdlist.strip(', ,').split(','):
                    line = line1.replace(' ', '_').replace('/', '_')
                    saveout = open((save + ".txt"), "a")
                    ssh_shell.sendall(line1 + '\n')
                    time.sleep(1)
                    config_result = ssh_shell.recv(99999).decode()
                    print (config_result)
                    # time.sleep(2)
                    saveout.write(config_result)
                    saveout.close()
                os.chdir(curpath)
                # 关闭连接
                s.close()
            except Exception, e:
                print (ip1 + " " + str(e))
                nogood.write(ip1 + " " + str(e))
                continue

p1 = producerthread(name = 'p1')
p1.start()
c1=consumerthread(name = 'c1')
c1.start()
#c2 = consumerthread(name = 'c2')
#c2.start()
endtime = datetime.datetime.now()
print (endtime - starttime).seconds
