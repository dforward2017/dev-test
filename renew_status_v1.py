#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import opsdb
import tsc_getstatusv1
import opsdb
import re
import json
import tmp_getstatus
def tsc_update_status():
    #result type dic format {u'msg': [{u'ip': u'10.161.88.6', u'alived': 1}, {u'ip': u'172.16.0.203', u'alived': 0}], u'ReturnCode': 0, u'task_id': u'Arthur-1.1501553679.73.65085'}
    result=tsc_getstatusv1.get_tscagent_status()
    #db_val type list format [('172.16.0.203', 'TYSV04122448'), ('10.161.88.6', 'TYSV06020009')]
    db_val=opsdb.conn_select()
    #print db_val
    dead_iplist=[]
    alive_iplist=[]
    # from result get dead_iplist and alive_iplist list
    for row in result['msg']:
        if row['alived']== 0:
            temp=row['ip']
            dead_iplist.append(temp) 
        else: 
            temp=row['ip']
            alive_iplist.append(temp)
    #print dead_iplist
    #print alive_iplist
    #print alive_iplist
    

    for val in db_val:
        if val[0]=='':
            asset_id=val[1]
            #opsdb.update('tsc_agent','dead',asset_id)
            opsdb.update('tsc_agent','1',asset_id)

    for ip in dead_iplist:
        for val in db_val:
            if ip in val[0] and ip !='':
                asset_id=val[1]
                #print asset_id
                #opsdb.update('tsc_agent','dead',asset_id)
                opsdb.update('tsc_agent','1',asset_id)

    for ip in alive_iplist:
        for val in db_val:
            if ip in val[0] and ip !='':
                asset_id=val[1]
                #print asset_id
                #opsdb.update('tsc_agent','alive',asset_id)
                opsdb.update('tsc_agent','0',asset_id)
                

def tmp_update_status():
    #retval type(dict) format {"10.161.88.6":[18,85,21,17,15],"172.16.0.203":[20,20,26,23,15]}
    retval=tmp_getstatus.get_tmpagent_status()
    #print retval
    obj_ip=tmp_getstatus.getiplist()
    #print obj_ip
    db_val=opsdb.conn_select()
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
    
    for val in db_val:
        if val[0]=='':
            asset_id=val[1]
            #opsdb.update('tmp_agent','dead',asset_id) 
            opsdb.update('tmp_agent','1',asset_id) 

    for ip in tmp_dead:
        for val in db_val:
            if ip in val[0] and ip !='':
                asset_id=val[1]
                #print asset_id
                #opsdb.update('tmp_agent','dead',asset_id)
                opsdb.update('tmp_agent','1',asset_id)

    for ip in tmp_alive:
         for val in db_val:
             if ip in val[0] and ip !='':
                 asset_id=val[1]
                 #print asset_id
                 #opsdb.update('tmp_agent','alive',asset_id)  
                 opsdb.update('tmp_agent','0',asset_id)  
 


def main():
    tsc_update_status()
    tmp_update_status()

if __name__ == '__main__':
    main()
