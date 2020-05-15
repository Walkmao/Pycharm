# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formataddr

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon

class Send2Kindle(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        maingrid = QGridLayout()
        fromLB = QLabel('邮箱：')
        self.fromLnE = QLineEdit()
        pwdLB = QLabel('密码：')
        self.pwdLnE = QLineEdit()
        self.pwdLnE.setEchoMode(QLineEdit.Password)
        kdlLB = QLabel('Kindle地址:')
        self.kdlLnE = QLineEdit()
        self.chooseBtn = QPushButton('选择文件')
        self.pushBtn = QPushButton('推送')
        self.infoTxt = QTextEdit()
        self.infoTxt.setFixedHeight(200)

        self.chooseBtn.clicked.connect(self.chooseBooks)
        self.pushBtn.clicked.connect(self.pushBooks)

        maingrid.addWidget(fromLB, 0, 0)
        maingrid.addWidget(self.fromLnE, 0, 1)
        maingrid.addWidget(pwdLB, 1, 0)
        maingrid.addWidget(self.pwdLnE, 1, 1)
        maingrid.addWidget(kdlLB, 2, 0)
        maingrid.addWidget(self.kdlLnE, 2, 1)
        maingrid.addWidget(self.chooseBtn, 3, 0)
        maingrid.addWidget(self.pushBtn, 3, 1)
        maingrid.addWidget(self.infoTxt, 4, 0, 1, 2)

        self.setLayout(maingrid)
        self.setGeometry(300, 300, 350, 150)
        self.setWindowTitle('S2K')
        self.setWindowIcon(QIcon('s2k.ico'))
        self.showNormal()

    def chooseBooks(self):
        self.file = QFileDialog.getOpenFileNames(self, "Open File","D:","books (*.mobi *.epub)")    # 筛选文件后缀；可以多选
        self.infoTxt.append('您选中了{}本书：{}'.format(len(self.file[0]), str(self.file[0])))   # 获取选中文件的

    def pushBooks(self):
        try:
            self.msg = MIMEMultipart()
            self.msg['From']= formataddr(["sender",self.fromLnE.text()])   #括号里的对应发件人邮箱昵称、发件人邮箱账号
            self.msg['To']= formataddr(["receiver",self.kdlLnE.text()])   #括号里的对应收件人邮箱昵称、收件人邮箱账号
            self.msg['Subject'] = 'Python SMTP 邮件测试' #邮件的主题，也可以说是标题        

            #邮件正文内容
            msg_text = MIMEText('This is a email test send by python.', 'plain', 'utf-8')
            self.msg.attach(msg_text)

            # 截取并拼接smtp服务器地址
            from_address = self.fromLnE.text()
            smtp_address = 'smtp.' + from_address[(from_address.index('@') + 1) : len(from_address)]

            # 构造带附件的邮件
            files = self.file[0]
            for f in files:
                file_name = QFileInfo(f).fileName() # 提取文件名

                part = MIMEApplication(open(f,'rb').read())  
                part.add_header('Content-Disposition', 'attachment', filename=file_name)  
                self.msg.attach(part)

            s = smtplib.SMTP(smtp_address, 25)
            self.infoTxt.append('正在登陆邮箱...')
            s.login(self.fromLnE.text(),self.pwdLnE.text())
            self.infoTxt.append('登陆成功，即将发送文件...')
            s.sendmail(self.fromLnE.text(), [self.kdlLnE.text()], self.msg.as_string())
            self.infoTxt.append('发送成功。')
            s.quit()

        except Exception as e:
            self.infoTxt.append("There is a exception:{}".format(str(e)))
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Send2Kindle()
    sys.exit(app.exec_())

