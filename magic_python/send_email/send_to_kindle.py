# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 13:55:41 2018

@author: lenovo
"""

# kindle 
import smtplib  
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.utils import formataddr

def smtp_attachment():
    """HTML格式邮件"""
    from_address="mircomao@163.com"
    password = "MK320825"

    # smtp 服务器地址
    smtp_address = "smtp.163.com"

    # 目标地址
    to_address = "1830926109@kindle.cn"    # 改成要发送的目的地址
    try:
        msg = MIMEMultipart()
        msg['From']= formataddr(["sender",from_address])   #括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To']= formataddr(["receiver",to_address])   #括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = 'Python SMTP 邮件测试' #邮件的主题，也可以说是标题

        #邮件正文内容
        msg_text = MIMEText('This is a email test send by python.', 'plain', 'utf-8')
        msg.attach(msg_text)

        # 邮件附件
        msg_attachment = MIMEApplication(open(r'D:\PycharmProjects\Project1\games change the world.mobi','rb').read()) 
        msg_attachment.add_header('Content-Disposition', 'attachment', filename='游戏改变世界.mobi')  
        msg.attach(msg_attachment)

        server = smtplib.SMTP(smtp_address, 25)
        server.login(from_address, password)
        server.sendmail(from_address, [to_address], msg.as_string())
        server.quit()
        print('邮件发送成功！')
    except Exception as e:
        print("There is a exception:", e)
        
if __name__ == '__main__':
    smtp_attachment()


