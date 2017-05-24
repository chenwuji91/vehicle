#-*- coding: UTF-8 -*-
'''
@author: chenwuji
异常终止
'''


def check_two_record_interval(time_interval, eachline, nextline):
    if time_interval > 1800:
        print 'Error!'
        print eachline, nextline, 'Stop'
        notify_by_email(str(eachline) +','+ str(nextline) + '  Time_insterval_stop. Unfinished')
        exit(-1)


def notify_by_email(message):
    from email.header import Header
    from email.mime.text import MIMEText
    import smtplib
    from_addr = "notify@notice.chenwuji.top"
    password = "fuckyou321"
    receiver = ['53996386@qq.com', 'yek@mail.ustc.edu.cn', 'sa515002@mail.ustc.edu.cn']
    smtp_server = "smtpdm.aliyun.com"
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['From'] = from_addr
    msg['To'] = ";".join(receiver)
    msg['Subject'] = Header(u'程序运行报告', 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.login(from_addr, password)
    server.sendmail(from_addr, receiver, msg.as_string())
    server.quit()
