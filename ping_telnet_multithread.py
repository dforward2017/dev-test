#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import subprocess
import Queue
import threading
import time,sys,os
iplist=[]
with open('tnc_iplist') as f:
    for line in f:
        iplist.append(line.strip())
#print iplist
#sys.exit()
queue = Queue.Queue()
_thread = 15
for ip in iplist:
    queue.put(ip)


def check(i, q):
    while True:
        ip = q.get()  # 获取Queue队列传过来的ip，队列使用队列实例queue.put(ip)传入ip，通过q.get() 获得
#        print "Thread %s:Pinging %s" % (i, ip)
        data = os.system("ping -c 1 -i0.1 -w 2 %s > /dev/null 2>&1" % ip)  # 使用os.system返回值判断是否正常
        data1 = os.system("echo 'a' | telnet -e 'a' %s 23 > /dev/null 2>&1" % ip)
        #data = os.system("ping -c 1 -i0.1 -w 2 %s >> /tmp/1.log 2>&1" % ip)  # 使用os.system返回值判断是否正常
        #data = subprocess.call('ping -c 1 -i 0.1 -w 1 '+ ip,shell=True,stdout=open('/dev/null','w'))
        if data == 0:
            print "%s:正常运行" % ip
        else:
            print "%s:停止工作" % ip

        if data1 ==0:
            print "%s:23端口已通" % ip
        else:
            print "%s:23端口不通" % ip
        q.task_done()  # 表示queue.join()已完成队列中提取元组数据
        
print "开始ping工作 %s" % time.ctime()
for i in range(_thread):#线程开始工作
        run=threading.Thread(target=check,args=(i,queue)) #创建一个threading.Thread()的实例，给它一个函数和函数的参数
        run.setDaemon(True)#这个True是为worker.start设置的，如果没有设置的话会挂起的，因为check是使用循环实现的
        run.start()     #开始线程的工作
queue.join()#线程队列执行关闭
print "ping 工作已完成 %s" % time.ctime() 