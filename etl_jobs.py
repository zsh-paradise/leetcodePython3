# -*- coding: utf-8 -*-
import cx_Oracle as cx_Oracle
from datetime import datetime

from utils import  get_db_conn,get_today,get_dw2_conn
import threading
import Queue
import xml.dom.minidom
import time
import os
import logging
import logging.config
import settings
from etl_class import OdsWork,DwWork,Dw2Work
from utils import  get_dw2_conn


def etl_jobs():
    odsErrorJobs=[]
    dwErrorJobs=[]
    dw2ErrorJobs=[]
    q = Queue.Queue(-1)
    q1 = Queue.Queue(-1)
    q2 = Queue.Queue(-1)
    logger = logging.getLogger("main")
    logger.info(u"python后台定时任务启动...")

    #每天清空线程
    with q.mutex:
        q.queue.clear()
    with q1.mutex:
        q.queue.clear()
    with q2.mutex:
        q2.queue.clear()
    DOMTree = xml.dom.minidom.parse("config.xml")
    root = DOMTree.documentElement
    tagODS = root.getElementsByTagName("ODS")
    tagP1 = root.getElementsByTagName("DW")
    tagSpecial = root.getElementsByTagName("DW2")
    #读取数据库，放到队列里
    #cursor =get_dw2_conn.cursor()
    #cursor.execute('select 1 from dual ');
    #results = cursor.fetchall()
    #for result in results:
        #q.put(result)


    for ods in tagODS:
        #print ods.firstChild.data
        q.put(ods.firstChild.data)

    for tagp1 in tagP1:
        #print ods.firstChild.data
        q1.put(tagp1.firstChild.data)

    for tagp2 in tagSpecial:
        #print ods.firstChild.data
        q2.put(tagp2.firstChild.data)

    while q.not_empty:
        for i in range(settings.thread_num):
            odsName = q.get()
            thread = threading.Thread(target=OdsWork.Work(odsName))
            thread.start()
            thread.join()
            time.sleep(0.1)
            logging.info(u"ods"+odsName+u"已经完成")
            if OdsWork.get_error_result():
                odsErrorJobs.append(OdsWork.get_error_result())

    #这里也可以发邮件
    logging.info(u"------------------------------------ods层出错的为"+str(odsErrorJobs)+"------------------------------------------------------------")
    if q.empty():
        while q1.not_empty():
            for i in range(settings.thread_num):
                dwName = q1.get()
                thread = threading.Thread(target=DwWork.Work(dwName))
                thread.start()
                thread.join()
                time.sleep(0.1)
                if DwWork.get_result():
                    #把缺少依赖的放进去继续执行
                    q1.put(DwWork.get_result())
                if DwWork.get_error_result():
                    #把执行错的放到dict中最后出入到日志中。
                    dwErrorJobs.append(DwWork.get_error_result())
        logging.info(u"------------------------------------dw出错的为"+str(dwErrorJobs)+"------------------------------------------------------------")
        while q2.not_empty():
            for i in range(settings.thread_num):
                thread = threading.Thread(target=Dw2Work.Work(q2.get()))
                thread.start()
                thread.join()
                time.sleep(0.1)
                if DwWork.get_result():
                    #把缺少依赖的放进去继续执行
                    q2.put(Dw2Work.get_result())
                if DwWork.get_error_result():
                    #把执行错的放到dict中最后出入到日志中。
                    dw2ErrorJobs.append(Dw2Work.get_error_result())
        logging.info(u"------------------------------------dw2出错的为"+str(dw2ErrorJobs)+"------------------------------------------------------------")



def start():
    while True:

        if datetime.now().strftime("%H")  in ("00"):
            #开始处理精度文件
            etl_jobs()
        #日志表每天会插入很大数据，所以需要做个定时任务，每天清理8天前的日志信息（8天是我定的）
        #sp_delet_logs_dm 定时删除数据存储过程，只在浙江有。建议推广
        if datetime.now().strftime("%H") in ("20"):
            cursor2 =get_dw2_conn.cursor()
            ms = cursor2.callproc("sp_delet_logs_dm")


if __name__ == "__main__":
    logging.config.fileConfig("main_log.conf")
    logging.info("--------------------------ETL任务开始------------------")
    start()
