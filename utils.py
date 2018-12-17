# -*- coding: utf-8 -*-
import sys
import settings
from datetime import date, datetime,timedelta
import time
import logging
import logging.config
 # 数据集配置   支持mysql 和oracle
def get_db_conn():
    if settings.dbTypeName.lower() == "oracle":
        import cx_Oracle
        user = settings.stat_conn["user"]
        password = settings.stat_conn["password"]
        db = settings.stat_conn["host"] + ":" + str(settings.stat_conn["port"]) + "/" + settings.stat_conn["db"]
        conn = cx_Oracle.connect(user, password, db)
    elif settings.dbTypeName.lower() == "mysql":
        import pymysql
        conn = pymysql.connect(**settings.stat_conn)
    else:
        # 默认数据库连接为mysql
        import pymysql
        conn = pymysql.connect(**settings.stat_conn)
    return conn

def get_dw2_conn():
    if settings.dbTypeName.lower() == "oracle":
        import cx_Oracle
        user = settings.dw2_conn["user"]
        password = settings.dw2_conn["password"]
        db = settings.dw2_conn["host"] + ":" + str(settings.dw2_conn["port"]) + "/" + settings.dw2_conn["db"]
        conn = cx_Oracle.connect(user, password, db)
    elif settings.dbTypeName.lower() == "mysql":
        import pymysql
        conn = pymysql.connect(**settings.stat_conn)

    else:
        # 默认数据库连接为mysql
        import pymysql
        conn = pymysql.connect(**settings.stat_conn)
    return conn

def get_mh_mysql_conn():
    import pymysql
    conn = pymysql.connect(**settings.mh_conn_mysql)
    return  conn
#获取当天时间
def get_today():

    return date.today().strftime("%Y%m%d")

def get_yesterday():
    today =date.today()
    yesterday =  today - timedelta(days=1)

    return yesterday.strftime("%Y%m%d")

def query_for_list(cur, sql, param=None):
    # 返回全部查询结果
    # @return list[dict]格式
    logger = logging.getLogger("main.tools.utils")
    result_list = []
    try:
        if param:
            cur.execute(sql, param)
        else:
            cur.execute(sql)
        columns = [val[0].lower() for val in cur.description]
        results = cur.fetchall()
        for result in results:
            result_dict = dict(zip(columns, result))
            result_list.append(result_dict)
    except Exception, e:
        logger.error("select error [%s]:[%s]:[%s]" %(sql, param, str(e)))
        result_list = None
    return result_list


def auto_insert_sql(objs, table=None, charset='UTF-8'):
    """
    自动生成insert SQL语句，如果obj为对象列表，则根据第一个对象生成SQL语句。
    @objs 对象或对象列表
    @table 数据表名
    @charset 数据库编码
    @return (SQL语句，转换后的对象或对象列表)
    """
    is_batch = isinstance(objs, list)
    if not objs:
        return (None, []) if is_batch else (None, None)
    obj = objs[0] if is_batch else objs
    obj_li = objs if is_batch else [objs]
    # 解析表名
    if not table:
        table = obj.__class__.__name__
    # 解析字段 和 转换数据
    cols = []
    row_li = []
    if hasattr(obj, '__iter__'):  # dict
        # 解析字段
        for k in obj:
            cols.append(k)
        # 转换数据
        for obj in obj_li:
            row = {}
            for k in cols:
                v = obj[k]
                row[k] = v.encode(charset) if isinstance(v, unicode) else v
            row_li.append(row)
    elif hasattr(obj, '__dict__'):  # object
        for i, (k, v) in enumerate(obj.__dict__.items()):
            cols.append(k)
        for obj in obj_li:
            row = {}
            for k in cols:
                v = getattr(obj, k)
                row[k] = v.encode(charset) if isinstance(v, unicode) else v
            row_li.append(row)
    elif hasattr(obj, 'ListFields'):  # Google Protocol Buffer
        for field, v in obj.ListFields():
            cols.append(field.name)
        for obj in obj_li:
            row = {}
            for k in cols:
                v = getattr(obj, k) if obj.HasField(k) else None
                row[k] = v.encode(charset) if isinstance(v, unicode) else v
            row_li.append(row)
    else:
        raise Exception("couldn't parse object: %s" % obj)
    # 生成SQL语句
    if not cols:
        raise Exception("no colume found in object: %s" % obj)
    sql_prefix = ['insert into ', table, ' (']
    sql_suffix = [') values(']
    for i, k in enumerate(cols):
        sql_prefix.append(', %s' % k if i > 0 else k)
        sql_suffix.append(', :%s' % k if i > 0 else ':%s' % k)
    sql_suffix.append(')')
    sql_prefix.extend(sql_suffix)
    sql = ''.join(sql_prefix)
    # --------------------------------------------------
    return (sql, row_li) if is_batch else (sql, row_li[0])
