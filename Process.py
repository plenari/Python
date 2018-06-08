# -*- coding: utf-8 -*-
"""注意：
1,含有'.for'文件的文件夹只能含有一个'.for'文件
2,use 'ctrl+c' to stop. 
@author: 409200093@qq.com
"""
print(__doc__)
import os
import subprocess as sp
from multiprocessing import cpu_count,Pool
import math
import psutil as ps
import time

def done(path_bonus):
    start=time.time() 
    idir,ifile=os.path.split(path_bonus)
    os.chdir(idir)
    for i in os.listdir(idir):
        if os.path.splitext(i)[1] in ['.out','.dat']:
            os.remove(i)
    a=sp.call('gfortran %s'%path_bonus,shell=True)
    if 'a.out' in os.listdir(os.getcwd()) and a==0: 
        print('Pid is %d. Address is %s is starting!'%(os.getpid(),path_bonus))
        time.sleep(10.0)
        a=sp.call('./a.out',shell=True)
        print('Pid is %d. Address is %s has done! last %.3f hours'%(os.getpid(),path_bonus,(time.time()-start)/3600.0))
        return ('Pid is %d. Address is %s has done! last %.3f hours'%(os.getpid(),path_bonus,(time.time()-start)/3600.0))
    else:
        print('Pid is %d. Address is %s is wrong!! last %.3f seconds'%(os.getpid(),path_bonus,(time.time()-start)))
        time.sleep(10.0)
        return ('Pid is %d. Address is %s is wrong!! last %.3f seconds'%(os.getpid(),path_bonus,(time.time()-start)))
   

path_dir=input(r'please input dir addres:')
for_file=[]
def get_for(path_dir):    
    for root,dirs,files in os.walk(path_dir):
        for ifile in files:
            for_file.append(os.path.join(root,ifile))
get_for(path_dir)            

path_omf=[i for i in for_file if os.path.splitext(os.path.split(i)[1])[1]=='.for']
assert len(path_omf)>0,"输入包含'.for'的文件夹"

if __name__=='__main__':
    min_cpu=math.ceil(cpu_count()*0.95-sum(ps.cpu_percent(percpu=True))/100)-1
    lensub=min(min_cpu,len(path_omf))
    assert lensub>=1, 'None cpu is avaliable,please try again at another time!'
    print('Pid is %d'%os.getpid())    
    print('%d cpus is available,%d subprocess needed ,so %d subprocess is created'%(min_cpu,len(path_omf),lensub))
    if input('"ENTER" to continue,others to exit: ')=='':
        pass
    else:
        raise Exception('Stopped by user!')
    time.sleep(1.0)
    pool=Pool(lensub)
    result=[]
    for i in path_omf:
        c=pool.apply_async(done,args=(i,))
        result.append(c)
    pool.close()
    pool.join()
    for res in result:
        print(res.get())
    os.chdir(path_dir)
    with open('done.txt','w') as f:
        f.write('All in %s is over!'%path_dir)
    print('All in %s is over!'%path_dir)