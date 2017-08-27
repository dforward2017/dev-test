#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import urllib2
import urllib
import re
import os
import json
import sys
import opsdb
def post_query(url, data):
    data = json.dumps(data).encode("utf-8")
    req = urllib2.urlopen(url,data)
    #json_file=open("outputfile","w")
    #json_file.write(req.read())
    #json_file.close()
    return req.read()


def getiplist():
    val=opsdb.conn_select()
    #print val
    return val
#    ip=[]
#    assetid=[]
#    for iplist1 in val:
#        ip.append(iplist1[0])
#    print ip
#    
#    
#    dbs_str=json.dumps(ip)
#    obj_ip=re.sub(';(\d+.\d+.\d+.\d+){1,}', '', dbs_str)
#    obj_ip=json.loads(obj_ip)
#    #print(type(obj_ip),obj_ip)
#    #print iplist
#    return obj_ip




def get_tscagent_status():
    value=getiplist()
    ip=[]
    assetid=[]
    for iplist1 in value:
        ip.append(iplist1[0])
    #print ip

    dbs_str=json.dumps(ip)
    obj_ip=re.sub(';(\d+.\d+.\d+.\d+){1,}', '', dbs_str)
    obj_ip=json.loads(obj_ip)
    url='http://api.disops.oa.com/arthur'
    info={"method": "arthur.query_tsc_status","params": {"hosts":obj_ip}}
    result = post_query(url,info)
    result=json.loads(result)
    #print result
    return result
    #dead_iplist=[]
    #for row in result['msg']:
    #    if row['alived']== 0:
    #        temp=row['ip']
    #        dead_iplist.append(temp)
    #print dead_iplist
    #return dead_iplist
def main():
    #getiplist()
    get_tscagent_status()
    
if __name__ == '__main__':  
    main() 
