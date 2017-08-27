#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
import sys
import os
import MySQLdb
#os.environ['PYTHON_EGG_CACHE'] = '/tmp/.python-eggs/'
#os.environ['PYTHON_EGG_DIR']='/tmp/.python-eggs/'
ip=sys.argv[1]
os_info=sys.argv[2]

def execute_sql(sql):
    conn = MySQLdb.connect(host='172.16.8.231',user='mysql',passwd='',db='nmsystem',port=3306)
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return  result

def get_netidcid(ip):
    sql = "select netroomid  from t_pinginfo where name='%s'" % ip
    rows = execute_sql(sql)
    if rows == ():
        print 0
        sys.exit()
    return rows[0][0]

netidcid = get_netidcid(ip)
#print netidcid


def get_agent_config():
    sql = "select ip, net_idc from t_agent_collector_config "
    rows = execute_sql(sql)
    t_pronbe_config = {}
    for row in rows:
        ip = row[0]
        netidcid_list = row[1].split(",")
        for netidcid in netidcid_list:
            t_pronbe_config[netidcid] = ip
    return t_pronbe_config

agent_config =  get_agent_config()
netidcid = str(netidcid)
#print agent_config[netidcid]
print '%s;%s' %(ip, agent_config[netidcid])
