# -*- coding: utf-8 -*-
# @Time    : 2017/4/16 22:05
# @Author  : chenwuji
# @File    : main.py
# @Software: PyCharm Community Edition
# @功能: 底层网格优化   更改网格的编排模式
import math

# bigWGLineDis = 50
# littleWGLineDis = 5
# littleWGColNum = bigWGLineDis / littleWGLineDis
# littleWGLineNum = littleWGColNum
lon_left = 120.6354828592534
lon_right = 120.85635657413037
lat_upper = 31.376368052001823
lat_below = 31.253404335545934
step = 0.000001
lon_step = 526 * step / 10    #这个就是每个网格的东西跨度 跨度是50米   然后除以10  就是5米一个网格了
lat_step = 450 * step / 10    #这个就是每个网格的南北跨度 跨度是50米  然后除以10  就是5米一个网格了
eve_num_of_line = (int)(math.ceil((lon_right - lon_left) / lon_step))
eve_num_of_col = (int)(math.ceil((lat_upper - lat_below) / lat_step))


def getWG_number(lon, lat):
    lon_gap = lon - lon_left
    lat_gap = lat - lat_below
    lon_num = (int)(lon_gap / lon_step)
    lat_num = (int)(lat_gap / lat_step)
    if lon_num == eve_num_of_col:
        lon_num = eve_num_of_col - 1
    if lat_num == eve_num_of_line:
        lat_num = eve_num_of_line - 1
    return lon_num,lat_num


def getWG_centerLonLat(WGNUM):
    longiNum = int(WGNUM.split('-')[0])
    latiNum = int(WGNUM.split('-')[1])
    resLon = lon_left + longiNum * lon_step + 0.5 * lon_step
    resLat = lat_below + latiNum * lat_step + 0.5 * lat_step
    return resLon, resLat

#计算类
from math import radians, cos, sin, asin, sqrt
def calculate(lon1, lat1, lon2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数）
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # 地球平均半径，单位为公里
    return c * r * 1000

# print getWG_number(120.85635657413037, 31.376368052001823)  #最右上角 4199 2732
# print getWG_number(120.6354828592534, 31.253404335545934)  #左下角 0 0
# print getWG_centerLonLat('4199-2732')
# print calculate(120.85635657413037, 31.376368052001823,120.8563765592534, 31.376366835545934)
# print get_littleWG_number(120.7354828592534, 31.353404335545934)
# print getWG_centerLonLat(93430, 21)
# print get_aroud(600)
# print getWG_number(120.711141468, 31.345746018)
# print get_littleWG_number(120.713141468, 31.348746018)
