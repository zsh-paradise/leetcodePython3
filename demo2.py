# -*- coding: utf-8 -*-
import cx_Oracle as cx_Oracle
from utils import  get_db_conn,get_today
import threading
import Queue
import xml.dom.minidom
import time
import os
import logging
import logging.config

q = Queue.Queue(-1)
q1 = Queue.Queue(-1)
q2 = Queue.Queue(-1)
DOMTree = xml.dom.minidom.parse("config.xml")
root = DOMTree.documentElement
tagODS = root.getElementsByTagName("ODS")
tagP1 = root.getElementsByTagName("pl1")
tagP2 = root.getElementsByTagName("pl2")
#存储过程的输入输出参数
today = get_today();

for ods in tagODS:
    #print ods.firstChild.data
    q.put(ods.firstChild.data)


for tagp1 in tagP1:
    #print ods.firstChild.data
    q1.put(tagp1.firstChild.data)

for tagp2 in tagP2:
    #print ods.firstChild.data
    q2.put(tagp2.firstChild.data)


def consume(threadName):
    logger = logging.getLogger("main")
    logger.info("---------------------------------------------")
    while(not q.empty()):
        odsname = q.get()
        logger.info("thread id:%s  ;queue value : %s" % (threadName, odsname))
        ret = os.system("~/Kettle/pan.sh -file=/home/etl/test-krr/ktr/test/"+odsname+".ktr -param:NEWNAME="+odsname+"_"+today+" >> /home/etl/test-krr/ktr/test/logs/"+
                  odsname+".log")
        if (ret == 0):
            os.system("echo "+odsname+".ktr  successfully executed >> /home/etl/test-krr/ktr/test/logs/result")
            logger.info(odsname+".ktr  successfully executed")
        else:
            os.system("echo " + odsname + ".ktr  fail executed >> /home/etl/test-krr/ktr/test/logs/result")
            logger.info(odsname+".ktr  fail executed")
        #time.sleep(2)
    if(q.empty()):
        while(not q1.empty()):
            p1name = q1.get()
            cursor =get_db_conn.cursor()
            msg = cursor.var(cx_Oracle.STRING)
            cursor.callproc(p1name, [today, msg])

    if msg =="1":
        q1.put(p1name)
        logging.info(p1name+u" 存储过程相关依赖没有采集完成,等待采集 ")
    elif msg =="2":
        logging.info(p1name+"successfully executed")
    else:
        logging.info(p1name+u" 存储过程采集错误 ")




t1 = threading.Thread(target=consume,args=("Thread-1",))
t2 = threading.Thread(target=consume,args=("Thread-2",))
t3 = threading.Thread(target=consume,args=("Thread-3",))
t4 = threading.Thread(target=consume,args=("Thread-4",))
t1.start()
t2.start()
t3.start()
t4.start()
t1.join()
t2.join()
t3.join()
t4.join()



