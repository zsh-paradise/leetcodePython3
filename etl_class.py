# -*- coding: utf-8 -*-
# @author  zsh
# @date  2017/11/22
import cx_Oracle
import os
import logging
import logging.config
import settings
from utils import get_today,get_db_conn,get_dw2_conn
import time

#构建ods消费任务
class OdsWork():
    def __init__(self):
        self._result  =None
        self._errorResult = None
    def Work(self,ktrName):
        today =  get_today();

        try:
            logging.info(u"正在处理ods抽取任务，执行的krs名称是"+ktrName)
            #建议就把调度程序放到Kettle放到对应的文件夹下面。这样写死路径，在部署文档中标注清楚
            os.system("~/Kettle/pan.sh -file=/home/python/ktr/"+ktrName+".ktr -param:NEWNAME="+ktrName+"_"+today)
        except Exception as e :
            logging.error(e)
            self._errorResult=ktrName
    def get_error_result(self):
        return self._errorResult

#构建dw消费任务
class DwWork():
    def __init__(self):
        self._result  =None
        self._errorResult = None
    def Work(self,dwName):

        cursor1 =get_db_conn.cursor()
        today =  get_today();
        msg = cursor1.var(cx_Oracle.STRING)
        ms = cursor1.callproc(dwName, [today, msg])
        if ms[1] =="1":
            self._result=dwName
            logging.info(u" 存储过程相关依赖没有采集完成,等待采集,存储过程名称 "+dwName)
        elif ms[1] =="3":
            logging.error(u" 存储过程采集错误")
            self._errorResult=dwName
        else:
            logging.info(u"successfully executed 执行成功")
    def get_result(self):
        return self._result
    def get_error_result(self):
        return self._errorResult

#构建dw2消费任务
class Dw2Work():
    def __init__(self):
        self._result  =None
        self._errorResult = None
    def Work(self,dw2Name):

        cursor2 =get_dw2_conn.cursor()
        today =  get_today();
        msg = cursor2.var(cx_Oracle.STRING)
        ms = cursor2.callproc(dw2Name, [today, msg])
        if ms[1] =="1":
            self._result=dw2Name
            logging.info(u" 存储过程相关依赖没有采集完成,等待采集,存储过程名称 "+dw2Name)
        elif ms[1] =="3":
            logging.error(u" 存储过程采集错误")
            self._errorResult=dw2Name
        else:
            logging.info(u"successfully executed 执行成功")
    def get_result(self):
        return self._result
    def get_error_result(self):
        return self._errorResult
