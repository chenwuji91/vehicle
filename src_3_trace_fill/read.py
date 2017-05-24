#-*- coding: UTF-8 -*-
'''
@author: chenwuji
读取文件的主类
'''
import os
#读取一个出租车文件
def read_one_file(filepath):
    car_id = os.path.basename(filepath).split('_')[1].strip('.txt')
    f = open(filepath)
    data_all = []
    for eachline in f:
        eachlist = eachline.strip('\n').strip('\r').split(';')
        fro = eachlist[0]
        to = eachlist[1]
        begin_time = eachlist[3]
        end_time = eachlist[4]
        speed_info = (eachlist[2],eachlist[5])
        data_all.append(fro,to,begin_time,end_time,speed_info)
    return car_id, data_all

def read_one_day(filepath):
    dict_data_all_day = {}
    f = open(filepath)
    current_car_id = ''
    infolist = []
    for eachline in f:
        linelist = eachline.strip('\r').strip('\n').split(',')
        car_id = linelist[0]
        if car_id != current_car_id:
            current_car_id = car_id
            if len(infolist) > 1:
                dict_data_all_day[current_car_id] = infolist
            infolist = []
        infolist.append((linelist[1], linelist[2], linelist[3]))
    if len(infolist) > 1:
        dict_data_all_day[current_car_id] = infolist
    f.close()
    return dict_data_all_day

def readLukou():
    f = open('../data/lukou.txt')
    lukou_dict = {}
    for eachline in f:
        list1 = eachline.strip('\r').strip('\n').split(',')
        lukou_id = int(list1[0])
        x = float(list1[1])
        y = float(list1[2])
        lukou_dict[lukou_id] = (x,y)
    f.close()
    return lukou_dict

def readAdj():
    edge_set = set()
    f = open('../data/adj.txt')
    for eachline in f:
        list1 = eachline.strip('\r').strip('\n').split(',')
        first_id = list1[0]
        other_id = list1[1:]
        while other_id.__contains__(''):
            other_id.remove('')
        while other_id.__contains__('\r'):
            other_id.remove('\r')
        for eachother in other_id:
            edge_set.add((int(first_id), int(eachother)))
            edge_set.add((int(eachother), int(first_id)))
    f.close()
    return edge_set

if __name__ == '__main__':
    one_day_data = read_one_day('../recovered/03')
    pass



