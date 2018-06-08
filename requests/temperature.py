#coding=utf-8
'''
远程获得cpu温度，检测温度和网络的畅通
'''
import time
from multiprocessing import Process
import paramiko
from base64 import decodestring
import matplotlib.pyplot as plt


hostname='用户名'
username='test1'
password=b''
password = decodestring(password).decode('utf-8')
ssh = paramiko.SSHClient()#创建SSH对象
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())#把要连接的机器添加到known_hosts文件中

def plot_wrong():
    plt.text(0,0.5,'something wrong',fontsize=100)
    plt.show()
	
def get_ssh():
    try:#get  data
        ssh.connect(hostname=hostname, port=22, username=username, password=password)
        cmd = 'cat /sys/class/hwmon/hwmon0/device/temp1_input'
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = int(stdout.read().decode('utf-8'))/1000  
        ssh.close()
        return 1,result#net is ok,temperature of cpu
    except:
        p1=Process(target=plot_wrong)
        p1.start()
        return 0,0
		

def beep(mess='high temp'): #waring 
    print(time.strftime('%m-%d %H:%M'),mess,) 
    for i in range(20):
        print('\a')
        time.sleep(1)
        
def analys():#analys
    global net,temp
    _net,_cpu=get_ssh()
    net.pop(0);net.append(_net);temp.append(_cpu)
    print(time.strftime('%m-%d %H:%M'),'net',_net,'cpu',_cpu)
    return net,_cpu

if __name__=='__main__':
    net,temp=[1,1],[]
    cpu=60
    while True:       
        net,_cpu=analys()#
        if sum(net)==0:#[0,0]
            p1=Process(target=beep,args=('network is disable',))
            p1.run()
        if _cpu>cpu:
            p2=Process(target=beep,args=('high temperature',))
            p2.run()
        time.sleep(10*60)
    
    