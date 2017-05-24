#-*- coding: UTF-8 -*-
'''
@author: chenwuji
读取原始文件  将脚本保存为按照天的文件
'''
import tools
alldata = {}
map_dict = {}
global_count = 1

def read_data(filename):
    f = open(filename)
    for eachline in f:
        if(len(eachline.split('values (')) < 2):
            continue
        eachline = eachline.decode('GBK').encode('UTF-8')
        # print eachline
        basic_list1 = eachline.split('\n')[0].split('\t')[0].split('values (')[1].split('to_timestamp')[0].split(',')
        pass
        intersection_name = basic_list1[0].split('\'')[1]
        lane_num = basic_list1[1]
        if len(basic_list1[2].split('\'')) > 1:
            direction = basic_list1[2].split('\'')[1]
        else:
            direction = basic_list1[2]
        id = basic_list1[3].split('\'')[1]
        if id == '-':
            pass
        if map_dict.__contains__(id):
            id = map_dict[id]
        else:

            map_dict[id] = global_count
            id = global_count
            global global_count
            global_count = global_count + 1

        vehicle_color = basic_list1[4].split('\'')[1]
        time = eachline.split('to_timestamp(\'')[1].split('.')[0]
        speed = int(eachline.split('HH24:MI:SS.ff\'),\'')[1].split('\'')[0])
        tools.writeToFile('data_sort_by_date/' + time.split(' ')[0] + '.csv', str(id) + ',' + intersection_name + ',' +lane_num
                          + ',' +direction + ',' +vehicle_color + ',' + time + ',' + str(speed))



if __name__ == '__main__':
    filename = 'data/20160301-10.sql'
    read_data(filename)
    filename = 'data/20160311-20.sql'
    read_data(filename)
    filename = 'data/20160320-31.sql'
    read_data(filename)
    tools.toFileWithPickle('mapping_dict', map_dict)
