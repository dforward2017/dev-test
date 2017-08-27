#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import paramiko    
import sys,os


class remoteLinux(object):
    def __init__(self, ip, port ,username, password, timeout=30):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.timeout = timeout
        # 链接失败的重试次数
        self.try_times = 3

    def connect(self,cmd):
        s = paramiko.SSHClient()
        s.load_system_host_keys()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(self.ip,self.port,self.username,self.password,timeout=5)
        stdin,stdout,stderr=s.exec_command(cmd)
        cmd_result = stdout.read(),stderr.read()
        for line in cmd_result:
            print line
        s.close()

    def close(self,):
        pass

    def sftp(self,):
        t = paramiko.Transport((self.ip,self.port))
        t.connect(username=self.username,password=self.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        #sftp.get('/tmp/hello.txt','hello.txt')   # 下载文件
        sftp.put('ssh.py','/tmp/ssh.py')          #  上传文件
        t.close()

if __name__ == '__main__':
    obj = remoteLinux('172.16.0.203',36000,'root','Ya2dQ7b4ptxJmEPC')
    obj.connect('df -h')
    obj.sftp()
    

 

