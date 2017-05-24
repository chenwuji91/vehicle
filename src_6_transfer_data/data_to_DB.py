#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 28/03/2017 13:22
# @Author  : chenwuji
# @File    : data_to_DB.py
# @Software: PyCharm Community Edition

from datetime import datetime
import os
import csv
import MySQLdb
dbconn = MySQLdb.connect(host="localhost",port=3306,user="root", passwd="8887799" ,db="vehicle",charset="utf8")

def process_file(filename = '../data/2016-03-03'):
    folder_name = os.path.basename(filename).replace('-','_')
    table_name = createTable(folder_name)
    csvfile = csv.reader(file(filename), delimiter=';')
    for eachline in csvfile:
        current_time = eachline[0]
        time_current = secondsOfToday(current_time)
        data_list = map(lambda x: (time_current,x.split(',')[0],x.split(',')[1].split('-')[0],x.split(',')[1].split('-')[1]), eachline[1:])
        insertDatas(table_name, tuple(data_list))

def createTable(table_name):
    '''创建表'''
    conn=dbconn.cursor()
    sql = '''
    CREATE TABLE if not exists `vehicle_position_'''+table_name+'''` (
      `timenow` int(11) NOT NULL,
      `vid` varchar(9) NOT NULL,
      `X` varchar(5) NOT NULL,
      `Y` varchar(5) NOT NULL,
      PRIMARY KEY  (`timenow`,`vid`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8;
    '''
    conn.execute(sql)
    return 'vehicle_position_' + table_name

def insertDatas(table_name, data_tuple):
    sql = 'insert into '+table_name+'(timenow,vid,X,Y) values(%s, %s, %s, %s)'
    executemany(sql, data_tuple)

def executemany(sql, tmp):
    '''插入多条数据'''
    conn=dbconn.cursor()
    conn.executemany(sql, tmp)

def execute(sql):
    '''执行sql'''
    conn=dbconn.cursor()
    conn.execute(sql)

def secondsOfToday(d1):
    d2 = d1.split(' ')[0] + ' ' + '00:00:00'
    dd1 = datetime.strptime(d1, "%Y-%m-%d %H:%M:%S")
    dd2 = datetime.strptime(d2, "%Y-%m-%d %H:%M:%S")
    return (dd1-dd2).seconds


if __name__ == '__main__':
    import sys
    sys.argv = ['','28']
    process_file('../data/2016-03-'+sys.argv[1])
    pass
    dbconn.close()
