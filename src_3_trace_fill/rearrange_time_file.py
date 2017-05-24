#-*- coding: UTF-8 -*-
'''
@author: chenwuji
重新组织文件存储形式
'''


def rearrange():
    import glob
    import os
    import tools
    from datetime import datetime
    flist = glob.glob('../filled_routes/*')  #显示当前目录下的所有日期文件夹
    for eachfolder in flist:
        fl2 = glob.glob(eachfolder + '/*')
        sorted_date_file = sorted(fl2, key = lambda x:datetime.strptime(os.path.basename(x), "%Y-%m-%d %H:%M:%S"))
        for eachfile in sorted_date_file:
            f = open(eachfile)
            fdata = os.path.basename(eachfile)
            for eachline in f:
                fdata = fdata + ';'  + eachline.strip('\n').strip('\r')
            tools.writeToFile(fdata[0:10], fdata)
            f.close()





