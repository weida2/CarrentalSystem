from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton,  QPlainTextEdit,QMessageBox
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QIcon
from usersys import *
from rootsys import *
from share import glovar as g
import pymysql

db = None
cursor = None
user = 'root'
pas = '123456'

class Status():

    def __init__(self):

        # 全局变量 初始化
        g._init()
        cate = None



        # 从文件中加载UI定义
        self.ui = uic.loadUi("ui/login.ui")

        # 按钮功能
        self.ui.buttonGroup.buttonClicked.connect(self.handlebuttonGroup) # 选择用户登录还是管理员

        self.ui.login_button.clicked.connect(self.login) # 登录按钮登录
        self.ui.edit_password.returnPressed.connect(self.login)
        # 账号 密码


    # 实现登录 选择 登录 用户 或者 管理员
    def login(self):
        choose = self.handlebuttonGroup()


        #while True:
        # 账号 密码

        username = self.ui.edit_username.text().strip()
        password = self.ui.edit_password.text().strip()

        glovar.set_value('username', username)



        db = pymysql.connect(host='localhost', user=user, password=pas, database='carrental')
        cursor = db.cursor()
        sql = "select * from admin"
        try:
            cursor.execute(sql)
            data = cursor.fetchall()
            for each in data:
                if each[1] == username:
                    if each[2] == password:
                        if username == 'root' and choose == '管理员':
                            self.ui.root_win = root_win()
                            self.ui.root_win.ui.show()
                            self.ui.close()
                            return
                        elif username != 'root' and choose == '用户':
                            g.set_value('username', username)
                            self.ui.user_win = user_win()
                            self.ui.user_win.ui.show()
                            self.ui.close()
                            return

            QMessageBox.warning(self.ui, '登陆失败', '用户名或密码输入不正确，请重新输入')

        except:
            db.rollback()
        db.close()


    # 登录用户 还是 管理员
    def handlebuttonGroup(self):
        sudo = self.ui.buttonGroup.checkedButton().text()
        return sudo




