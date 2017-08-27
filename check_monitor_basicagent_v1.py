#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import urllib2
import re
import os
import json
import sys
import dbops
import commands
sql = " select asset_id,inner_ip from t_server_info where business_module not like '%%%s%%' and business_module not like '%%%s%%' and business_module not like '%%%s%%' and business_module not like '%%%s%%' limit 30" % ('IDC模块化','实验室专业设备','开发测试环境','未分配')

def post_query(url, data):
    data = json.dumps(data).encode("utf-8")
    req = urllib2.urlopen(url,data)
    return req.read()


def get_tmpiplist():
    global sql
    #obj = dbops.MySQLClass('localhost','root','','basic_agent',3306)
    obj = dbops.MySQLClass('172.16.5.100','checkpass','checkpass@2017###','iyunwei',4001)
    #sql = "select assetid,ip from t_basic_agent_status where ip !='' and tmp_agent='1' limit 2"
    #sql = " select asset_id,inner_ip from t_server_info where business_module not like '%%%s%%' and business_module not like '%%%s%%' and business_module not like '%%%s%%' and business_module not like '%%%s%%' limit 30" % ('IDC模块化','实验室专业设备','开发测试环境','未分配')
    #print sql
    val = obj.select(sql)
    #val = obj.select(sql,('%IDC模块化%','%实验室专业设备%','%开发测试环境%','%未分配%'))
    #print val
    #sys.exit()
    ip=[]
    assetid=[]
    for iplist1 in val:
        ip.append(iplist1[1])
    #print ip
    
    dbs_str=json.dumps(ip)
    obj_ip=re.sub(';(\d+.\d+.\d+.\d+){1,}', '', dbs_str)
    obj_ip=json.loads(obj_ip)
    #print(type(obj_ip),obj_ip)
    #sys.exit()
    return obj_ip

def get_tsciplist():
    global sql
    #obj = dbops.MySQLClass('localhost','root','','basic_agent',3306)
    obj = dbops.MySQLClass('172.16.5.100','checkpass','checkpass@2017###','iyunwei',4001)
    #sql = "select assetid,ip from t_basic_agent_status where ip !='' and tsc_agent='1' limit 2"
    val = obj.select(sql)
    ip=[]
    #assetid=[]
    for iplist1 in val:
        ip.append(iplist1[1])
    #print ip

    dbs_str=json.dumps(ip)
    obj_ip=re.sub(';(\d+.\d+.\d+.\d+){1,}', '', dbs_str)
    obj_ip=json.loads(obj_ip)
    url='http://api.disops.oa.com/arthur'
    info={"method": "arthur.query_tsc_status","params": {"hosts":obj_ip}}
    result = post_query(url,info)
    result=json.loads(result)
    #print result
    tsc_dead=[]
    for row in result['msg']:
        if row['alived']== 0:
            temp=row['ip']
            tsc_dead.append(temp) 
    #print tsc_dead
    str_ip=",".join(tsc_dead).encode("utf8")
    iplist=list(str_ip.split(","))
    #print iplist
    return iplist


def get_tmpagent_status():
    value=get_tmpiplist()
    #print(type(value),value)
    #sys.exit()
    length=len(value)
    index=0
    count=50
    data={}
    L=[]
    while index < length:
        splitval=value[index:index+count]

        #url='http://api.disops.oa.com/arthur'
        url='http://172.16.8.70/new_api/getdata.get_servers_basic_attr'
        #info={"method": "arthur.query_tsc_status","params": {"hosts":obj_ip}}
        info={"method":"getdata.get_servers_basic_attr", "params":{"iplist":splitval, "attr":9, "count":5}}
        result = post_query(url,info)
        #print result
        index=index+count
        #print splitval
        result=json.loads(result)
        #print result
        #L.append(result.items()) 
        #print result
        #print result.items()
        data=dict(data.items() + result.items())

    #print data
    return data
    

def check_tmp_status():
    #retval type(dict) format {"10.161.88.6":[18,85,21,17,15],"172.16.0.203":[20,20,26,23,15]}
    retval=get_tmpagent_status()
    #print retval
    #sys.exit()
    obj_ip=get_tmpiplist()
    #print obj_ip
    #sys.exit()
    #db_val=opsdb.conn_select()
    #print retval
    #print obj_ip
    tmp_alive=[]
    tmp_dead=[]
    for ip in obj_ip: 
        if retval.has_key(ip): 
            cpu_info = retval[ip] 
            #print cpu_info 
            cpu=reduce(lambda x, y:  x+y, cpu_info) 
            if cpu < -2: 
                #print ip  
                tmp_dead.append(ip)
            else: 
                tmp_alive.append(ip)

        else:
            tmp_alive.append(ip)
    #print tmp_dead
    #print tmp_alive
    str_ip=",".join(tmp_dead).encode("utf8")
    #print str_ip
    str_ip=list(str_ip.split(","))
    print str_ip
    return str_ip

def tmp_monitor_alert():
    obj_iplist=check_tmp_status()
    #print obj_iplist
    for ip in obj_iplist:
        cmd="/usr/local/agenttools/agent/agentRepStr %s %d 'test alert'" % (ip,866431)
        print cmd
        status,output = commands.getstatusoutput(cmd)
        print output


def tsc_monitor_alert():
    obj_iplist=get_tsciplist()
    #print obj_iplist
    for ip in obj_iplist:
        cmd="/usr/local/agenttools/agent/agentRepStr %s %d 'test alert'" % (ip,866549)
        print cmd
        #sys.exit()
        status,output = commands.getstatusoutput(cmd)
        print output

    
if __name__ == '__main__':  
    tmp_monitor_alert()
    #tsc_monitor_alert()
