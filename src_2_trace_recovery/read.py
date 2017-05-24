#!usr/bin/env python
# -*- coding: utf-8 -*-

def read_carmera():
    name_dict = {}
    f = open('../data/camera.txt')
    for eachline in f:
        list2 = eachline.split('\r')[0].split('\n')[0].split(' ')
        no = list2[0]
        # print list2
        name = list2[1]
        name_dict.setdefault(name, no)
        name_dict.setdefault(name.split('/')[1] + '/' + name.split('/')[0], no)
    f.close()
    return name_dict

def read_data(date):
    trace_dict = {}
    name_dict = read_carmera()
    f = open('../data_sort_by_date/2016-03-' + date + '.csv')
    for eachline in f:
        eachline = eachline.strip('\xef\xbb\xbf')
        list1 = eachline.split('\r')[0].split('\n')[0].split(',')
        id = list1[0]
        name = list1[1].split('-')[0] + '/' + list1[1].split('-')[1]
        if not name_dict.__contains__(name):
            continue
        road_intersection = name_dict[name]
        time = list1[5]
        if trace_dict.__contains__(id):
            tmp_info = trace_dict[id]
            tmp_info.append((road_intersection,time,list1[1],list1[2],list1[3],list1[4],list1[6]))
        else:
            tmp_info = []
            tmp_info.append((road_intersection,time,list1[1],list1[2],list1[3],list1[4],list1[6]))
            trace_dict.setdefault(id, tmp_info)
    f.close()
    return trace_dict



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
    readAdj()
    pass

