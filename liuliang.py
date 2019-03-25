# -*- coding: utf-8 -*-
import time,re
#from tqdm import  *
import  multiprocessing
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException
import sys,xlwt
from xlutils.copy import copy
from xlrd import open_workbook
from datetime import datetime
#import openpyxl
import os
reload(sys)
sys.setdefaultencoding('utf8')

'''def set_style(name,height,bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style
def write_excel(result):
    f = xlwt.Workbook()
    sheet1 = f.add_sheet('drop',cell_overwrite_ok=True)
    row0 = ["name","old","birthday","hab"]
    i = 1
    for data in result:
        for j in range(len(data)):
            sheet1.write(i, j, data[j])
        i = i + 1
    f.save('test.xls')
'''

def NetworkDevice(iplist,cmd,enablepass):
    global hostname
    rt = {
        'device_type':'cisco_ios',
        'username':'admin',
        'password':'admin',
        'ip': iplist,
        'secret':enablepass
    }
    print('-' * 50)
    print(u'[+] connecting to network device {0}...'.format(iplist))
    net_connect = ConnectHandler(**rt)
    net_connect.enable()
    hostname = net_connect.find_prompt().replace("#", "")
    if ':' in hostname:
        hostname=str(hostname).split(':')[1]
    print (u'[+] hostname:{0}'.format(hostname))
    timestr = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
    output = net_connect.send_command(cmd)
    #print output.find('total input drops')
    p1 = r"(\d+) packets input, (\d+) bytes, (\d+) total input drops"
    pattern1 = re.compile(p1)
    result= pattern1.findall(output)
    net_connect.disconnect()
    return result
    #write_excel(result)


def sun(key,value):
    #print "[+] The Program is running......."
    #username = ('%s' %(sheet.cell_value(ips, 5)))
    #password = ('%s' %(sheet.cell_value(ips, 6)))
    enablepass = 'admin'
    timestr = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    try:
            try:
                result=NetworkDevice(key,value, enablepass)
                return result
                # output.write('\rcomplete percent:%.0f%%' % float(ips/linenum))
            except (EOFError, NetMikoTimeoutException):
                print ('Can not connect to Device')
            except (EOFError, NetMikoAuthenticationException):
                print ('username/password wrong!')
            except (ValueError, NetMikoAuthenticationException):
                print ('enable password wrong!')
            print "Time elapsed: {0}\n".format(datetime.now() - start_time)

            # time.sleep(2)
            # output.flush()
    except Exception, e:
        print e
if __name__ == '__main__':
    enablepass = 'admin'
    timestr = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    netyuan = {'10.12.18.102': 'show int g0/0/0/0', '10.12.18.103': 'show int g0/0/0/0',
               '10.12.18.104': 'show int g0/0/0/0', '10.12.18.105': 'show int g0/0/0/0'}
    i=1
    while i<1000 :
        j=0
        for key, value in netyuan.items():
            start_time = datetime.now()
            r_xls = open_workbook("test.xls")
            #wb = openpyxl.load_workbook("test.xls")
            #ws = wb.worksheets[0]

            i = r_xls.sheets()[0].nrows
            j = r_xls.sheets()[0].ncols
            excel = copy(r_xls)
            table = excel.get_sheet(0)
            try:
                result = sun(key, value)
                for data in result:
                    for j in range(len(data)):
                        table.write(i, j, data[j])
                        table.write(i, j + 1, timestr)
                        table.write(i, j + 2, hostname)
                        #j=j+7
                    i = i + 1
                excel.save('test.xls')
            except Exception, e:
                print e
        time.sleep(60)

    #r_xls = open_workbook("test.xls")

    #write_excel(result)
