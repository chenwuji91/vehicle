# -*- coding : UTF-8 -*-
import math

lon_left = 120.6354828592534
lon_right = 120.85635657413037
lat_upper = 31.376368052001823
lat_below = 31.253404335545934
step = 0.000001
lon_step = 526 * step
lat_step = 450 * step
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
    # print lon_gap
    # print lat_gap
    # print lon_num
    # print lat_num
    return lat_num * eve_num_of_line + lon_num


# print getWG_number(120.6354828592534 + lon_step, 31.253404335545934)
def get_west(now_WG_number):
    line_num = now_WG_number / eve_num_of_line
    col_num = now_WG_number % eve_num_of_line
    if col_num - 1 < 0:
        return -1
    else:
        return line_num * eve_num_of_line + col_num - 1


def get_east(now_WG_number):
    line_num = now_WG_number / eve_num_of_line
    col_num = now_WG_number % eve_num_of_line
    if col_num + 1 >= eve_num_of_line:
        return -1
    else:
        return line_num * eve_num_of_line + col_num + 1


def get_north(now_WG_number):
    line_num = now_WG_number / eve_num_of_line
    col_num = now_WG_number % eve_num_of_line
    if line_num + 1 >= eve_num_of_col:
        return -1
    else:
        return (line_num + 1) * eve_num_of_line + col_num


def get_south(now_WG_number):
    line_num = now_WG_number / eve_num_of_line
    col_num = now_WG_number % eve_num_of_line
    if line_num - 1 < 0:
        return -1
    else:
        return (line_num - 1) * eve_num_of_line + col_num


def get_northwest(now_WG_number):
    if get_north(now_WG_number) == -1:
        return -1
    else:
        return get_west(get_north(now_WG_number))


def get_northeast(now_WG_number):
    if get_north(now_WG_number) == -1:
        return -1
    else:
        return get_north(get_east(now_WG_number))


def get_southwest(now_WG_number):
    if get_south(now_WG_number) == -1:
        return -1
    else:
        return get_south(get_west(now_WG_number))


def get_southeast(now_WG_number):
    if get_south(now_WG_number) == -1:
        return -1
    else:
        return get_south(get_east(now_WG_number))


def get_aroud(now_WG_number):
    aroud_number = []
    line_num = now_WG_number / eve_num_of_line
    print line_num
    col_num = now_WG_number % eve_num_of_line
    print col_num
    if line_num >= eve_num_of_line or col_num >= eve_num_of_col \
            or line_num < 0 or col_num < 0:
        print 111
        return aroud_number
    else:
        aroud_number.append(now_WG_number)
        if get_east(now_WG_number) != -1:
            aroud_number.append(get_east(now_WG_number))
        if get_west(now_WG_number) != -1:
            aroud_number.append(get_west(now_WG_number))
        if get_south(now_WG_number) != -1:
            aroud_number.append(get_south(now_WG_number))
        if get_north(now_WG_number) != -1:
            aroud_number.append(get_north(now_WG_number))
        if get_northwest(now_WG_number) != -1:
            aroud_number.append(get_northwest(now_WG_number))
        if get_northeast(now_WG_number) != -1:
            aroud_number.append(get_northeast(now_WG_number))
        if get_southwest(now_WG_number) != -1:
            aroud_number.append(get_southwest(now_WG_number))
        if get_southeast(now_WG_number) != -1:
            aroud_number.append(get_southeast(now_WG_number))
        return aroud_number


# print get_aroud(600)
