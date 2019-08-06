# -*- coding:utf-8 -*-

'''
逻辑：使用EMAIL来创建邮件内容msg，在使用STMP服务器server发送邮件
'''

import smtplib                          
from email.mime.text import MIMEText
from email.utils import formataddr

def smtp_text():
    #发件箱和密码（需开启验证授权）
    from_address="mircomao@163.com"
    password = "MK29941"

    #smtp服务器地址
    smtp_address = "smtp.163.com"

    #目标地址
    to_address = "1830926109@qq.com"

    try:
        #邮件内容
        '''
        msg_content = """<p>Python HTML格式邮件发送测试...</p>
        <p><a href="http://www.baidu.com">这是一个指向百度的链接</a></p>"""
        msg = MIMEText(msg_content, 'html', 'utf-8')
        
        '''
        msg = MIMEText('This is a test by python','plain','utf-8')  #MIMEText(text,type,charset)
        msg['From'] = formataddr(["sender", from_address])   #括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["receiver", to_address])     #括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] ='Python SMTP'                        #邮件的主题，也可以说是标题

        server = smtplib.SMTP(smtp_address, 25)  #server=smtplib.SMTP( [host, port,local_hostname)
        server.login(from_address, password)
        server.sendmail(from_address, [to_address], msg.as_string())  #对象发送邮件 SMTP.sendmail(from_addr, to_addrs, msg[, mail_options, rcpt_options])
        server.quit()
        print('success!')
    except Exception as e:
        print("There is a exception:", e)

if __name__ == '__main__':
    smtp_text()

