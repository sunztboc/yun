import  pexpect
import threading
import getpass
import os


def put_public_key(remote_ip,publickey,password):
    child=pexpect.spawn("/usr/bin/ssh-copy-id -i %s %s" %(publickey,remote_ip))
    flag=child.expect(["yes/no","password",pexpect.EOF,pexpect.TIMEOUT])
    #print (flag)
    if flag==0:    #0匹配yes/no成功，1匹配到password,2子程序退出,3超时
        print ("开始向%s上传公钥" %remote_ip)
        try:
            child.sendline("yes")
            child.expect("password")
            child.sendline(password)   #send不换行，sendline换行
            child.expect('added')    #远程命令返回成功，无此行，会显示已上传，但是实际没传输过去。
            print ("%s已上传公钥" %remote_ip)
        except Exception as e:
            print("上传公钥失败")
            print(e)
        finally:
            child.close()
    elif flag==1:
        try:
            child.sendline(password)
            child.expect('added')
            print ("%s已上传公钥" %remote_ip)
        except Exception as e:
            print("上传公钥失败")
            print(e)
        finally:
            child.close()
    else:
        print ("因本机已有公钥，故未向%s上传公钥,如需重新上传，请删除本机公钥" %remote_ip)
        child.close()
    lock.release() # 必须在执行函数里面释放锁。
if __name__=='__main__':
    ip_list=['192.168.31.12','192.168.31.11']
    default_public_key = os.path.expanduser('~/.ssh/id_rsa.pub')
    public_key=default_public_key
    passwd = getpass.getpass("\033[33mplease input password:\033[0m")
    lock = threading.BoundedSemaphore(30)
    if not os.path.exists(public_key) and not os.path.isfile(public_key):   #无公钥时创建
           
        key_path=os.path.expanduser('~/.ssh/id_rsa')
        os.remove(r'/root/.ssh/id_rsa')
        child = pexpect.spawn("/usr/bin/ssh-keygen -t rsa -P '' -f %s" %key_path)  #必须-f指定放置位置
        child.expect(pexpect.exceptions.EOF)
        child.close(force=True)
    for i in ip_list:
        lock.acquire() # 必需要在创建时加锁，否则不生效  pstree -p 22786|wc -l 可以查看线程数
        t=threading.Thread(target=put_public_key, args=(i,public_key,passwd))
        t.start()
        #this is a good method
