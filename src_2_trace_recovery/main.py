#!usr/bin/env python
# -*- coding: utf-8 -*-

import read as rd
import tools
from datetime import datetime

#将轨迹排序并进行输出   排除掉只有一个点的数据  直接对原始数据按照天来输出
def road_recovery(date1):
    trace_one_day = rd.read_data(date1)
    for eachcar in trace_one_day:
        current_trace = trace_one_day[eachcar]
        record_by_time = sorted(current_trace, key= lambda x:datetime.strptime(x[1], "%Y-%m-%d %H:%M:%S"))
        tools.makeDir('../notRecover/')
        if len(current_trace) > 1:
            print eachcar
            for e in record_by_time:
                tools.writeToFile('../notRecover/'+ date1, eachcar + ',' + e[0] + ',' + str(e[1]))

import filter
import graph
#将轨迹重新整理 按照dijkstra最短路径输出  并过滤掉部分数据
def trace_recovery(date1):
    trace_one_day = rd.read_data(date1)
    today_recovered = {}
    for eachcar in trace_one_day:
        #考虑将每天的路程分成若干段
        today_recovered_one_car = []
        #分段计数
        split_count = 0
        current_trace = trace_one_day[eachcar]
        #获得排序之后的结果
        record_by_time = sorted(current_trace, key=lambda x: datetime.strptime(x[1], "%Y-%m-%d %H:%M:%S"))
        #过滤出租车
        filter.remove_taxi(record_by_time)
        #开始恢复中间轨迹
        for i in range(len(record_by_time) - 1):
            c = record_by_time[i]
            n = record_by_time[i + 1]
            time_intervals = tools.intervalofSeconds(c[1], n[1])

            #如果时间间隔过长 保存之前的一段 开始存储新的一段
            if time_intervals > 1800: #and len(today_recovered_one_car) > 0:
                today_recovered_one_car.append(n)  #将路段闭合
                tools.writeToFile('../recovered/'+ date1, str(eachcar) + ',' + str(c[0]) + ',' + str(c[1]) + ',' + 'null')

                today_recovered[(eachcar, split_count)] = today_recovered_one_car
                today_recovered_one_car = []
                split_count += 1
                continue
            #如果时间间隔过长  同时目前毛线都没有恢复出来 直接继续往后走
            # elif time_intervals > 1800:
            #     print '毛都没有'
            #     continue

            nearest_path = graph.nearestPath(c[0], n[0])
            nearest_path_len = graph.nearestPathLen(c[0], n[0])
            #单位:米/秒
            avg_speed = nearest_path_len/float(time_intervals + 0.00000001)
            if avg_speed < 1:
                print '缓慢爬行?'
                continue
            current_total_dis = 0
            for k in range(len(nearest_path) - 1):   #路段没有闭合
                eachpoint = nearest_path[k]
                current_time = tools.increase_several_seconds(c[1], current_total_dis/avg_speed)
                today_recovered_one_car.append((eachpoint, current_time))
                tools.makeDir('../recovered/')
                tools.writeToFile('../recovered/'+ date1, str(eachcar) + ',' + str(eachpoint) + ',' + str(current_time) + ',' + str(avg_speed))
                current_total_dis += graph.edge_distance(eachpoint, nearest_path[k + 1])

            if i == len(record_by_time) - 2:
                eachpoint = nearest_path[len(nearest_path) - 1]
                current_time = tools.increase_several_seconds(c[1], current_total_dis / avg_speed)
                today_recovered_one_car.append((eachpoint, current_time))
                tools.makeDir('../recovered/')
                tools.writeToFile('../recovered/' + date1,
                                  str(eachcar) + ',' + str(eachpoint) + ',' + str(current_time) + ',' + str(avg_speed))


if __name__ == '__main__':
    recovery_list = ['03','04','05','06','07','08','09','10','11','12']
    for eachdate in recovery_list:
        trace_recovery(eachdate)
        road_recovery(eachdate)
