# -*- coding: utf-8 -*-

# 数据库配置
# dbTypeName 数据库类型 oracle | mysql
# stat_conn 统计库连接配置
#慧教云数据库
dbTypeName = "oracle"
stat_conn = {
    "host": "127.0.6.141",
    "port": 1521,
    "db": "orcl",
    "user": "dw",
    "password": "pass4dw",
}

dw2_conn = {
    "host": "127.0.6.147",
    "port": 1522,
    "db": "orcl",
    "user": "dw2",
    "password": "pass4dw2",
    "charset": "utf8"
}

mh_conn_mysql ={
    "host": "127.0.50.51",
    "port": 4040,
    "db": "portal",
    "user": "portal",
    "password": "portal_www",
    "charset": "utf8"
}

# 采集间隔时间,单位秒
gather_interval = 60*60
# 默认计时方案
default_time_sys_id = 1
#附件文件地址  "C://Users//Administrator//Desktop//123.docx"
appendix_address = ""
#收信人地址
addressee =""
#设置线程数
thread_num =8
