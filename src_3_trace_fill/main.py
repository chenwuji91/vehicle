#-*- coding: UTF-8 -*-
'''
@author: chenwuji
轨迹填充的主类
'''
import tools
import read
import road
import notify
import square
import os
from rearrange_time_file import *


def process_one_day():
    import glob
    flist = glob.glob('../recovered/1*')
    for eachfile in flist:
        count_num = 0
        data_one_day = read.read_one_day(eachfile)
        basename = os.path.basename(eachfile)
        for eachcar_id in data_one_day:
            eachcar_data = data_one_day[eachcar_id]
            for i in range(len(eachcar_data) - 1):
                eachline = eachcar_data[i]
                nextline = eachcar_data[i + 1]
                time_interval = int(tools.intervalofSeconds(eachline[1], nextline[1]))
                road_len = road.road_length(eachline[0], nextline[0])
                if time_interval < 1800 and time_interval >0 and road_len/time_interval < 30: #表示当前的轨迹和下面的轨迹是连续的 可以开始进行轨迹填充
                    if time_interval == 0:
                        print eachline,',',nextline
                    notify.check_two_record_interval(time_interval, eachline, nextline)  #检查数据合理性 异常退出
                    driving_line = road.driving_line(eachline[0], nextline[0], time_interval)
                    for eachsecond in range(time_interval): #对于行驶时间间隔的每一秒而言
                        current_position = driving_line(eachsecond)  #当前位置
                        lon_num, lat_num = square.getWG_number(current_position[0], current_position[1])  #当前网格
                        current_time = tools.increase_several_seconds(eachline[1], eachsecond)  #当前时间
                        current_speed = eachline[2]
                        count_num += 1
                        tools.makeDir('../filled_routes/' + basename + '/')
                        tools.writeToFile('../filled_routes/' + basename + '/' + str(current_time),
                                          str(eachcar_id) + ',' + str(lon_num) + '-' + str(lat_num))
        # notify.notify_by_email('Finish_running_day:' + str(basename) + '\n' + 'Processed:' + str(count_num))


import exceptions as e
if __name__ == '__main__':
    try:
        process_one_day()
    except Exception,e:
        print 'Error Message:', e.message
        # notify.notify_by_email('Error Message:'+'Runtime Error, '+ str(e.message))
    pass
    # rearrange()
