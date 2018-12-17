# -*- coding: utf-8 -*-
import mimetypes
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from utils import get_today
import settings

def sendETLEmail(p):

    _user = "2395022397@qq.com"
    _pwd = "nmtvjrlabeyeecdi"
    _to  = "sunjingjing@whty.com.cn"
    file_name = settings.addressee #附件名（带路径）
    #如名字所示Multipart就是分多个部分
    msg = MIMEMultipart()
    msg["Subject"] = "ETL调度未跑完的任务"
    msg["From"]  = _user
    msg["To"]   = _to
    today = get_today()
    #---这是文字部分---
    line1 ="您好："
    line2 = "今天"+str(today)+"的统计内容，数据详情请看附件"
    line3 ="武汉天喻教育大数据组"
    part = MIMEText("<font><font  size=3 color='#ff0000' >采集报警:</font><br >%s<br>%s<br float:right>%s<br></font>" %(line1, line2 ,line3), "html", "utf-8" )
    msg.attach(part)

    #---这是附件部分---
    #xlsx类型附件
    ## 读入文件内容并格式化 [方式1]－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
    data = open(file_name, 'rb')
    ctype,encoding = mimetypes.guess_type(file_name)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    maintype,subtype = ctype.split('/',1)
    file_msg = smtplib.email.MIMEBase.MIMEBase(maintype, subtype)
    file_msg.set_payload(data.read())
    data.close( )
    smtplib.email.Encoders.encode_base64(file_msg)#把附件编码
    basename = os.path.basename(file_name)
    file_msg.add_header('Content-Disposition','attachment', filename = basename)#修改邮件头
    msg.attach(file_msg)

    s = smtplib.SMTP_SSL("smtp.qq.com")#连接smtp邮件服务器,端口默认是25
    s.login(_user, _pwd)#登陆服务器
    s.sendmail(_user, _to, msg.as_string())#发送邮s件
    s.close()