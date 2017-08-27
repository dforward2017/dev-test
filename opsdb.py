#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import MySQLdb
import sys
def conn_select():
    # 打开数据库连接
    db = MySQLdb.connect(host="172.16.5.100",user="checkpass",passwd="checkpass@2017###",port=4001,db="iyunwei",charset="utf8")

    # 使用cursor()方法获取操作游标 
    cursor = db.cursor(MySQLdb.cursors.DictCursor)

    # SQL 查询语句
    #sql = "select asset_id,inner_ip from t_server_info limit 10"
    #sql = "select asset_id,inner_ip from t_server_info where business_module not like '%%%s%%' and business_module not like '%%%s%%' limit 10" % (u'IDC模块化',u'实验室专业设备')
    sql = "select asset_id,inner_ip from t_server_info where business_module not like %s and business_module not like %s limit 2" 
    #print sql
    try:
       # 执行SQL语句
       cursor.execute(sql,('%IDC模块化%','%实验室专业设备%'))
       # 获取所有记录列表
       L_ip=[]
       L_asset=[]
       results = cursor.fetchall()
       #print(type(results),results)
       for key in results:
            temp=key['inner_ip']
            L_ip.append(temp)
       for key in results:
            temp1=key['asset_id']
            L_asset.append(temp1) 
      # print(results)
       val= zip(L_ip,L_asset)
       #print val
       #sys.exit()
       return val

    except:
       print "Error: unable to fecth data"

    # 关闭数据库连接
    db.close()

def write(status,ip):
    #db1 = MySQLdb.connect(host="localhost",user="root",passwd="",db="basic_agent")
    db1 = MySQLdb.connect(host="172.16.5.100",user="checkpass",passwd="checkpass@2017###",port=4001,db="iyunwei",charset="utf8")
    cursor = db1.cursor()
    sql = "insert into t_basic_agent_status(assetid,ip) values('%s','%s')" % (status,ip)
    try:
          # 执行sql语句
          #cursor.executemany("insert into t_basic_agent_status(assetid,ip) values(%s,%s)",sql) 
          cursor.execute(sql)
          # 提交到数据库执行
          db1.commit()
    except:
          # Rollback in case there is any error
          db1.rollback()
       
       # 关闭数据库连接
          db1.close()

def update(agent,status,assetid):
    # 打开数据库连接
    #db = MySQLdb.connect(host="localhost",user="root",passwd="",db="basic_agent",charset="utf8")
    db = MySQLdb.connect(host="172.16.5.100",user="checkpass",passwd="checkpass@2017###",port=4001,db="iyunwei",charset="utf8")

    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()

    # SQL 更新语句
    sql = "update t_basic_agent_status set tsc_agent='%s' where assetid='%s'" % (status,assetid)
    sql1 = "update t_basic_agent_status set tmp_agent='%s' where assetid='%s'" % (status,assetid)
    try:
         # 执行SQL语句
         if agent == 'tsc_agent':
             cursor.execute(sql)
         elif agent == 'tmp_agent':
             cursor.execute(sql1)
         else:
             pass
         # 提交到数据库执行
         db.commit()
    except:
       # 发生错误时回滚
         db.rollback()

       # 关闭数据库连接
         db.close()


def main():
    sql1=conn_select()
    #print sql1
   # write(sql1)

    
if __name__ == '__main__':  
    main() 
