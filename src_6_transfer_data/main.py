#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/27 22:05
# @Author  : chenwuji
# @File    : main.py
# @Software: PyCharm Community Edition
# @功能: 根据碰面的结果 实时传输数据

'''
设计思路,程序设定传数据的起始时间和结束时间
每次递增一秒进行数据的传输  每一秒交换一次数据包
在传输的时候, 车辆的起始的数据包从数据库读取  也可以为空  如果为空表示不读取数据
在传输的时候,调用多线程模块 在后台将每一秒的车辆上面的数据包写入到 数据库中  保存数据库的时候  只是人为的设置一定的时间保存一次当前数据包的结果  如果为0则表示只在最后保存一次最终的结果
数据包的传输格式 为元组  (包内容, 在当前车辆上的生存时间, 产生这个数据包的路由[开始产生的车,...,...])
'''
import cPickle as p  #序列化对象 读取路网拓扑
import MySQLdb
import uuid
import random
import copy
import networkx

'''*********************************初始参数*********************************'''
begin_time = 100  #传输的开始时间
end_time = 150  #传输的结束时间
process_day = '2016_03_28'  #传输的日期
#dbconn = MySQLdb.connect(host="localhost",port=3306,user="root", passwd="8887799" ,db="vehicle") #初始化数据库的连接
dbconn = MySQLdb.connect(host="192.168.232.138",port=3306,user="root", passwd="fuckyou321" ,db="vehicle") #初始化数据库的连接
save_interval = 0  # 定时保存的时间间隔
fetch_lines = 100000  #执行sql一次返回的行数的限制,超出此限制报异常,主要考虑实际响应的影响
packet_init_model = 'random'   #数据包初始化的方式 默认为random  如果是'fromDB' 则从数据表读取
table_prefix = 'packet_status_'
build_network = True  # 直接读取network拓扑还是读取到setpair建立拓扑  如果为True则建立网络
packet_TTL = 3  #数据包的生存时间
packet_translate_one_second = 10  #每秒可以传输多少个包


'''*********************************业务逻辑操作*********************************'''
'''获取时间段内的车辆列表'''
def init_vehicle_list():
    sql = 'select distinct(vid) from vehicle_position_' + process_day + ' where timenow >= '+str(begin_time)+' and timenow <= '+str(end_time)+';'
    vehicle_list = query(sql)
    vehicle_data_list = map(lambda x:x[0],vehicle_list)
    vehicle_data_dict = dict(zip(vehicle_data_list,[[] for i in range(len(vehicle_data_list))]))
    return vehicle_data_dict, vehicle_data_list

'''获得某一秒 车辆的位置信息'''
def vehicle_position_one_second(ctime):
    sql = 'select vid,X,Y from vehicle_position_' + process_day + ' where timenow = ' + str(ctime) + ';'
    vehicle_list = query(sql)
    dict_position = {}
    for each_v in vehicle_list:
        dict_position.setdefault(each_v[0],(each_v[1],each_v[2]))
    return dict_position

# '''
# 随机给车辆产生数据包 每个车上的数据包全部随机
# '''
# def packet_init_random_packet(vehicle_data_dict,vehicle_data_list, packet_avg_vehicle = 20, packet_dispatch_mode = 'random', random_factor = 'uuid'):
#     if(packet_dispatch_mode == 'random'):
#         packet_total = len(vehicle_data_dict) * packet_avg_vehicle
#         for i in range(packet_total):
#             eachvehicle = vehicle_data_list[int(random.uniform(0,len(vehicle_data_list) - 0.0001))]
#             vehicle_data_dict[eachvehicle].append(str(uuid.uuid4()))
#             # vehicle_data_dict[eachvehicle].append((str(uuid.uuid4()),[begin_time], [tuple(('None','position'))],[eachvehicle]))
#     elif(packet_dispatch_mode == 'uniform'):
#         for i in range(packet_avg_vehicle):
#             for eachvehicle in vehicle_data_dict:
#                 vehicle_data_dict[eachvehicle].append(str(uuid.uuid4()))
#                 # vehicle_data_dict[eachvehicle].append((str(uuid.uuid4()),[begin_time],[tuple(('None','position'))],[eachvehicle]))  #包的格式(包内容,[每一跳的时间],[每一跳的位置],[每一跳的车])
#     pass

'''
将当前状态下的全局数据包保存到数据库
'''
def save_packet_to_db(vehicle_data_dict):
    # for i in range(0,len(vehicle_data_dict),1000):   #每次提交1000条数据
    submit_list = []
    for eachkey in vehicle_data_dict:
        submit_list.append((eachkey,','.join(vehicle_data_dict[eachkey])))  #只保存车的数据包 忽略时间
    table_name = process_day + '_' + str(begin_time) + '_' + str(end_time) + '_init_' + packet_init_model
    max_len = max(map(lambda x:len(x[1]), submit_list))
    dropTable(table_prefix + table_name)  #删除之前的传输表
    table_name = createTable(table_name, max_len)
    insertDatas(table_name, tuple(submit_list))

def save_packet_to_obj(vehicle_id_dict, vehicle_time_dict, vehicle_position_dict, vehicle_hop_vehicle):
    makeDir('../packet_transmit/')
    filename = '../packet_transmit/' + process_day+'_' + str(begin_time) + '_' + str(end_time) + '_init_' + packet_init_model
    toFileWithPickle(filename + '.id', vehicle_id_dict)
    toFileWithPickle(filename + '.time', vehicle_time_dict)
    toFileWithPickle(filename + '.position', vehicle_position_dict)
    toFileWithPickle(filename + '.hop', vehicle_hop_vehicle)


'''*********************************结束业务逻辑操作*********************************'''
'''******************************数据传输方法******************************'''
# '''传递数据的主函数'''
# def packet_exchange_with_network(vehicle_data_dict):
#     for ctime in range(begin_time, end_time + 1):
#         cnetwork = read_network(ctime)
#         if build_network:
#             cnetwork = constract_network(cnetwork)
#         '''继续考虑算法的内容'''
#         min_tree = networkx.minimum_spanning_tree(cnetwork)
#         print min_tree


'''传递数据的主函数  传递过程中只是进行单跳传输  且每秒只进行一次的单跳传输'''
def packet_exchange_one_hop(vehicle_id_dict, vehicle_time_dict, vehicle_position_dict, vehicle_hop_vehicle):
    # vehicle_id_dict = vehicle_data_dict  #开始时刻传入的包的数据  [包id1, id2, id3 ...]
    # vehicle_time_dict = {}  #记录每个车  [获得时间1,获得时间2,获得时间3 ...]
    # vehicle_position_dict = {}  #记录每个车  [获得位置1,获得位置2,获得位置3...]
    # vehicle_hop_vehicle = {}   #数据来源  [获得车辆1, 获得车辆2, 获得车辆3 ...]
    # assert len(vehicle_data_dict) == len(vehicle_time_dict) == len(vehicle_position_dict) == len(vehicle_hop_vehicle),'init data error'
    for ctime in range(begin_time, end_time + 1):  #开始的时候字典只保存id数据 其他数据不保存
        print 'processing:',ctime
        cnetwork = read_network(ctime)    #获得了所有的碰面对
        #在这里奉行一个原则,先传输之前的,再感知.先把之前的数据包传输结束之后,再把碰面对的数据加到这个里面
        vehicle_position = vehicle_position_one_second(ctime)
        for eachpair in cnetwork:
            vehicle1 = eachpair[0]  #车1的id
            vehicle2 = eachpair[1]  #车2的id
            position = (vehicle_position[vehicle1], vehicle_position[vehicle2])
            __transfer_data_from_one_vehicle_to_another(vehicle_id_dict[vehicle1], vehicle_id_dict[vehicle2],vehicle_time_dict[vehicle1],
                                                        vehicle_time_dict[vehicle2],vehicle_position_dict[vehicle1], vehicle_position_dict[vehicle2],
                                                        vehicle_hop_vehicle[vehicle1],vehicle_hop_vehicle[vehicle2],
                                                        ctime, position, vehicle2, vehicle1)  #不限制
            __new_packet_generate(vehicle_id_dict[vehicle1],vehicle_time_dict[vehicle1],vehicle_position_dict[vehicle1],vehicle_hop_vehicle[vehicle1], ctime, position, vehicle2, vehicle1)

'''一个车到另外一个车的数据传输''' #将前面一个的数据包传给后面一个
def __transfer_data_from_one_vehicle_to_another(id1_fro,id2_to,time1,time2,position1,position2,hop1,hop2, ctime, position, vid_to, vid_fro, packet_limit = -1): #传输的时候只考虑单向的传输 从一个车到另外一个车  -1表示不限制每秒传输个数  可以记录一下实际传输的个数  可以单独新建一个车的字典 记录什么车向什么车发送了多少包
    for i in range(len(id1_fro)):
        if time1[i] == ctime:
            break
        if not id2_to.__contains__(id1_fro[i]):
            id2_to.append(id1_fro[i])
            time2.append(ctime)
            position2.append(position[1])  #保存接收的地点
            hop2.append(vid_to)


def __new_packet_generate(id_list, time_list, position_list, hop_list,ctime, position, vehicle2, vehicle1):
    id1 = vehicle2 +'-' + vehicle1 + '-' + str(ctime)
    id_list.append(id1)
    time_list.append(ctime)
    position_list.append(position[1])
    hop_list.append(vehicle1)


'''建立网络拓扑'''
def constract_network(pair_set):
    G = networkx.Graph()  # 建立一个空的无向图G
    for eachpair in pair_set:
        G.add_edge(eachpair[0],eachpair[1])
    return G
'''******************************结束数据传输方法******************************'''

'''
读取对应的网络拓扑数据
'''
def read_network(time_of_network):
    filepath = '../connection/' + process_day.replace('_','-') + '/' + process_day.replace('_','-') + ' ' + time_retranslate(time_of_network) + '.set.data'
    dataFile = file(filepath,'r')
    obj = p.load(dataFile)
    return obj

import cPickle as p
def toFileWithPickle(filename, obj1):
    f = file(filename + '.data', "w")
    p.dump(obj1,f)
    f.close()

import os
# 创建目录,如果路径不存在创建文件夹
def makeDir(outpathDir):
    if os.path.exists(outpathDir)==False:
        print 'Create DIr'
        os.makedirs(outpathDir)

'''工具 把时间转换成标准时间'''
def time_retranslate(time_of_network):
    hour = time_of_network / 3600
    min = time_of_network % 3600 / 60
    seconds = time_of_network % 3600 % 60
    if hour < 10:
        hour = '0' + str(hour)
    if min < 10:
        min = '0' + str(min)
    if seconds < 10:
        seconds = '0' + str(seconds)
    return str(hour) + ':' + str(min) + ':' + str(seconds)


'''*********************************数据库DB操作*********************************'''
def queryData():
    sql = "select * from lifeba_users"
    rows = query(sql)
    return rows

def query(sql):
    '''查询sql'''
    conn=dbconn.cursor()
    conn.execute(sql)
    rows = conn.fetchmany(fetch_lines)
    assert len(rows) < fetch_lines,'Incomplete query!'
    return rows

def createTable(table_name, max_packet_len):
    '''创建表'''
    Text = 'TEXT'
    if max_packet_len > 65534:
        Text = 'MEDIUMTEXT'
    if max_packet_len > 16777214:
        Text = 'LONGTEXT'
    conn=dbconn.cursor()
    sql = '''
    CREATE TABLE if not exists `'''+ table_prefix + table_name+'''` (
      `vid` varchar(9) NOT NULL,
      `packet` '''+Text+'''('''+ str(max_packet_len + 1) +''') NOT NULL,
      PRIMARY KEY  (`vid`)
    ) ENGINE=MyISAM;
    '''
    conn.execute(sql)
    return 'packet_status_' + table_name

def insertDatas(table_name, data_tuple):
    sql = 'insert into '+table_name+'(vid,packet) values(%s, %s)'
    executemany(sql, data_tuple)

def executemany(sql, tmp):
    '''插入多条数据'''
    conn=dbconn.cursor()
    conn.executemany(sql, tmp)

def dropTable(table_name):
    '''删除表'''
    conn=dbconn.cursor()
    conn.execute('''
    DROP TABLE IF EXISTS `''' + table_name + '''`
    ''')

'''*********************************主函数*********************************'''
if __name__ == '__main__':
    vehicle_id_dict, vehicle_data_list = init_vehicle_list()
    # packet_init_random_packet(vehicle_data_dict,vehicle_data_list,) # packet_dispatch_mode='uniform'
    # packet_exchange_with_network(vehicle_data_dict)
    vehicle_id_dict, vehicle_time_dict, vehicle_position_dict, vehicle_hop_vehicle = vehicle_id_dict, copy.deepcopy(vehicle_id_dict), copy.deepcopy(vehicle_id_dict), copy.deepcopy(vehicle_id_dict)
    packet_exchange_one_hop(vehicle_id_dict, vehicle_time_dict, vehicle_position_dict, vehicle_hop_vehicle)
    save_packet_to_obj(vehicle_id_dict, vehicle_time_dict, vehicle_position_dict, vehicle_hop_vehicle)
    save_packet_to_db(vehicle_id_dict)
    pass
    dbconn.close()
