#!/usr/bin/env python3
#-*- coding=utf-8 -*-

import requests
import time
import random
import re
import configparser
import logging
import logging.handlers
import lxml.etree as etree
import threading
import Queue
import os.path
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

DOUBAN_HEADERS = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Referer':'http://www.douban.com/search?cat=1019&q=%E5%AE%B3%E7%BE%9E',
'Accept-Language':'zh-CN,zh;q=0.8',
'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36',
'Accept-Encoding':'gzip, deflate',
'Host':'www.douban.com',
'Connection':'Keep-Alive'
}
IMAGE_HEADERS = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36'
}
CNFG_FILE = 'douban_crawler.cfg'
LOG_FILE = 'douban_crawler.log'
MAX_LOG_SIZE = 1024 * 1024*50 #1MB
LOG_BACKUP_COUNT = 3

logger = logging.getLogger('crawler')
logger.setLevel(logging.DEBUG)
fh = logging.handlers.RotatingFileHandler(LOG_FILE,
maxBytes=MAX_LOG_SIZE,
backupCount=LOG_BACKUP_COUNT,
encoding='utf-8')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter(
"%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(fh)
logger.addHandler(ch)
DEBUG = logger.debug
INFO = logger.info
WARNING = logger.warning
ERROR = logger.error


class Parser_Douban_Group(threading.Thread):
    def __init__(self, url, queue,t_name = 'Parser Group'):
        threading.Thread.__init__(self,name=t_name)
        self.data = queue
        self.url = url
        self.s = requests.Session()

    def run(self):
        #解析网页
        INFO("{0} started!".format(self.getName()))
        co = 0
        htm = open_douban_page(self.url,self.s)
        try:
            parser = etree.HTMLParser(recover=True)
            text_dom = etree.fromstring(htm, parser)
        except Exception as e:
            ERROR('Parse douban page error: {0}'.format(e))
            #DEBUG('Page: {0}'.format(htm))
        else:
            group_name = ''.join(text_dom.xpath("//div[@id='group-info']/h1//text()")).strip()
            INFO('Group name: {0}'.format(group_name))
            div_node = text_dom.xpath("//tr[@class='']")

            for x in div_node:
                co = co + 1
                item = {}
                url = ''.join(x.xpath("child::td[@class='title']/a/attribute::href"))
                title = ''.join(x.xpath("child::td[@class='title']/a//text()"))
                auth = ''.join(x.xpath("child::td[@nowrap='nowrap']/a[@class='']//text()"))
                reply = ''.join(x.xpath("child::td[@class='']//text()"))
                time = ''.join(x.xpath("child::td[@class='time']//text()"))
                item['title'] = title
                item['url'] = url
                item['auth'] = auth
                item['reply'] = reply
                item['time'] = time
                #将数据依次存入队列
                self.data.put(item, block=True)
                DEBUG('{0} Put({1}) - ({2} ...)'.format(self.getName(), co,item['title'][:20]))
        #存入结束标志
        self.data.put({})
        INFO("{0} finished! put {1} topic to queue.".format(self.getName(), co))

class Parser_Douban_Topic(threading.Thread):
    def __init__(self, topic_queue, content_queue, t_name = 'Parser Topic'):
        threading.Thread.__init__(self,name=t_name)
        self.topic_queue = topic_queue
        self.content_queue = content_queue
        self.s = requests.Session()

    def run(self):
        #解析网页
        INFO("{0} started!".format(self.getName()))
        co = 0
        coo = 0
        while True:
            try:
                #读取队列，最长等待5分钟
                val = self.topic_queue.get(True,300)
                if val:
                    co = co + 1
                    DEBUG('{0} Get({1}) - ({2} ...)'.format(self.getName(), co, val['title'][:20]))
                    htm = open_douban_page(val['url'],self.s)
                    try:
                        parser = etree.HTMLParser(recover=True)
                        text_dom = etree.fromstring(htm, parser)
                    except Exception as e:
                        ERROR('Parse douban page error: {0}'.format(e))
                        #DEBUG('Page: {0}'.format(htm))
                    else:
                        topic_name = ''.join(text_dom.xpath("//div[@id='content']/h1//text()")).replace('\n','').strip()
                        DEBUG('Topic name: {0}'.format(topic_name))
                        div_node = text_dom.xpath("//div[@class='topic-content']")
                        img_list = div_node[0].xpath("descendant::img/attribute::src")
                        for x in img_list:
                            coo = coo + 1

                            item = {}
                            #url = ''.join(x.xpath("descendant::img/attribute::src"))
                            item['title'] = topic_name + str(coo)
                            item['url'] = x
                            #将数据依次存入队列
                            self.content_queue.put(item)
                            DEBUG('{0} Put({1}) - ({2} ...)'.format(self.getName(), coo,item['title'][:20]))
                else:
                    self.topic_queue.put({})
                    INFO("{0} finished! get {1} topic from queue.".format(self.getName(), co))
                    break
            except Exception as e:
                ERROR("{0} timeout! {1}".format(self.getName(), e))
                break
        #存入结束标志
        self.content_queue.put({})
        INFO("{0} finished! put {1} image to queue.".format(self.getName(), coo))

class Save_Douban_Group(threading.Thread):
    def __init__(self, queue, folder_name = 'image', t_name = 'Storage'):
        threading.Thread.__init__(self,name=t_name)
        self.data = queue
        self.folder = folder_name
        self.s = requests.Session()

    def run(self):
        INFO("{0} started!".format(self.getName()))
        co = 0
        coo = 0
        while True:
            try:
                #读取队列，最长等待5分钟
                val = self.data.get(True,300)
                if val:
                    co = co + 1
                    #fp.write('<{0}>.{1} - {2}\r{3}\r{4}\r\n'.format(
                    #co,val['title'],val['time'],val['url'],val['abr']))
                    DEBUG('{0} Get({1}) - ({2} ...)'.format(self.getName(), co,val['title'][:20]))
                    img_dt = open_douban_page(val['url'], self.s, ret_raw = True)
                    img_nm = val['url'].split('/')[-1]
                    if img_dt:
                        fn = '{0}/{1}'.format(self.folder, img_nm)
                        if not os.path.exists(fn):
                            fp = open(fn, 'wb')
                            fp.write(img_dt)
                            fp.close()
                            coo = coo + 1
                else:
                    self.data.put({})    #仍然存入结束标识
                    break
            except Exception as e:
                ERROR("{0} timeout! {1}".format(self.getName(), e))
                #break
        #fp.close()
        INFO("{0} finished! save image({1}/{2}).".format(self.getName(), coo, co))

def open_douban_page(group_url, s, retries=3, ret_raw = False):
    #读取网页
    ret = ''
    try:
        cookies = dict(bid="RmFNKKPAd0s")
        if ret_raw:
            r = s.get(group_url, headers=IMAGE_HEADERS, stream=True)
        else:
            r = s.get(group_url, headers=DOUBAN_HEADERS, cookies=cookies)
        #print(r.cookies)
        r.raise_for_status()
        time.sleep(random.uniform(0.3, 1.5))
    except requests.ConnectionError as e:
        ERROR('Connect douban error({0}): {1}'.format(retries,e))
        retries = retries - 1
        if retries > 0:
            time.sleep(0.5)
            ret = open_douban_page(group_url, s, retries)
    except Exception as e:
        ERROR('Open douban url({0}) error: {1}'.format(group_url, e))
    else:
        #INFO('Open douban page finished! - {0}'.format(r.url))
        DEBUG('Request url: {0}'.format(group_url))
        if ret_raw:
            ret = r.raw.read()
        else:
            ret = r.text
    return ret



def crawler_douban(group_url, folder_name, task_name):
    q_topic = Queue.Queue()
    q_content = Queue.Queue()

    parser_group_obj = []
    parser_topic_obj = []
    storage_pic_obj = []

    for i in range(1,2):
        parser_group_obj.append(Parser_Douban_Group(group_url, q_topic, '{0} {1}'.format(task_name, i)))

    for i in range(1,2):
        parser_topic_obj.append(Parser_Douban_Topic(q_topic, q_content, 'Parser Topic {0}'.format(i)))

    for i in range(1,3):
        storage_pic_obj.append(Save_Douban_Group(q_content, folder_name, 'Storage {0}'.format(i)))

    for obj in parser_group_obj:
        obj.start()

    for obj in parser_topic_obj:
        obj.start()

    for obj in storage_pic_obj:
        obj.start()

    for obj in parser_group_obj:
        obj.join()

    for obj in parser_topic_obj:
        obj.join()

    for obj in storage_pic_obj:
        obj.join()

    del q_topic
    del q_content

if __name__ == '__main__':
    haixiu_hangzhou_url = 'https://www.douban.com/group/meituikong/'
    haixiu_url = 'https://www.douban.com/group/haixiuzu/'
    wuhan_url = 'https://www.douban.com/group/WHlove/'
    co =0
    while True:
        co = co + 1
        time.sleep(2.0)
        crawler_douban(wuhan_url, 'E:\douban', 'Parser HaiXiu Group ({0})'.format(co))

    input('Press any key to exit!')