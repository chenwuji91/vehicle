#-*- coding: UTF-8 -*-
'''
@author: chenwuji
路网类
'''
import read
import tools

lukou_data = read.readLukou()
def get_location(road_id):
    return lukou_data[int(road_id)]

def road_length(road_id1, road_id2):
    position1 = get_location(road_id1)
    position2 = get_location(road_id2)
    distance = tools.calculate(position1[0], position1[1], position2[0], position2[1])
    return distance

def driving_line(road_id1, road_id2, time_interval):
    current_location = get_location(road_id1)
    next_location = get_location(road_id2)
    lati_increase_pre_second = (next_location[0] - current_location[0])/(time_interval + 0.00000001)
    longi_increase_pre_second = (next_location[1] - current_location[1])/(time_interval + 0.00000001)
    return lambda t:(current_location[0] + lati_increase_pre_second * t,current_location[1] + longi_increase_pre_second * t)





if __name__ == '__main__':
    print road_length('2386','3133')