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
    return req.read()


def getiplist():
    val=opsdb.conn_select()
    #print val
    #return val
    ip=[]
    assetid=[]
    for iplist1 in val:
        ip.append(iplist1[0])
    #print ip
    
    dbs_str=json.dumps(ip)
    obj_ip=re.sub(';(\d+.\d+.\d+.\d+){1,}', '', dbs_str)
    obj_ip=json.loads(obj_ip)
    #print(type(obj_ip),obj_ip)
    #print iplist
    return obj_ip




def get_tmpagent_status():
    value=getiplist()
    #print(type(value),value)
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

    #print L 
    #L1=[]


    #for list1 in L:
    #    if list1 !=[]:
    #        L1.append(list1)
    #print L1
    #for i in L1:
        
    #    data[i[0][0]]=i[0][1]
    #print data
#    try:
#        result=json.loads(result)
#    except Exception as e:
#        print e
#        return
    #print data
    return data
    




def main():
    get_tmpagent_status()
    
if __name__ == '__main__':  
    main() 
