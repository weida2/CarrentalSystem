from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton,  QPlainTextEdit,QMessageBox
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from share import glovar as g
import pymysql
import time, datetime

# 用户管理界面
user = 'root'
pas = '123456'

class user_win():

    def __init__(self):

        # 全局变量
        global username
        username = g.get_value('username')

        # 动态加载ui文件
        self.ui = uic.loadUi("ui/user.ui")

        # 界面控件部分

        # 欢迎
        t = self.condatabase()
        sql = "SELECT * FROM custormerinfo WHERE telephone = %s" % repr(username)
        self.cursor.execute(sql)
        print('进入1')
        each = self.cursor.fetchone()
        # m[0]:id , m[1]:Cname, m[2]:Csex, m[3]:telephone, m[4]:Cpassword, m[5]:money
        welcomename = each[1]
        self.db.close()
        self.ui.welcome_lable.setText('  ' + welcomename + ', 你好！')

        # 查询按钮
        self.ui.showcar_table.setRowCount(50)
        self.ui.showcar_btn.clicked.connect(self.showcar)

        self.ui.selectcar_table.setRowCount(20)
        self.ui.selectcar_btn.clicked.connect(self.selectcar)
        self.ui.edit_selectcar.returnPressed.connect(self.selectcar)

        # 查看我的订单
        self.ui.diary_table.setRowCount(20)
        self.ui.diary_btn.clicked.connect(self.diary)

        # 查看个人中心
        self.ui.private_table.setRowCount(10)
        self.ui.private_btn.clicked.connect(self.private)

        # 账户充值
        t = self.condatabase()
        sql = "SELECT * FROM custormerinfo WHERE telephone = %s" % repr(username)
        self.cursor.execute(sql)
        print('进入1')
        m = self.cursor.fetchone()
        yue = str(m[5])
        # m[0]:id , m[1]:Cname, m[2]:Csex, m[3]:telephone, m[4]:Cpassword, m[5]:money
        self.ui.edit_yue.setText(yue)
        self.db.close()

        self.ui.edit_add.returnPressed.connect(self.add)
        self.ui.add_btn.clicked.connect(self.add)

        # 修改密码
        self.ui.edit_newpas.returnPressed.connect(self.changepas)
        self.ui.changepas_btn.clicked.connect(self.changepas)

        # 借车
        self.ui.edit_getcarday.returnPressed.connect(self.getcar)
        self.ui.getcar_btn.clicked.connect(self.getcar)

        # 还车
        self.ui.edit_backcarinfoid.returnPressed.connect(self.backcar)
        self.ui.backcar_btn.clicked.connect(self.backcar)

    def condatabase(self):
        # 定义打开数据库连接
        try:
            self.db = pymysql.connect(host='localhost', user=user, password=pas,database='carrental')
            # 使用cursor()方法创建一个游标对象 cursor
            self.cursor = self.db.cursor()
            return True
        except:
            return False

    # 查看车辆
    def showcar(self):
        t = self.condatabase()
        print(username)
        sql = "select * from carinfo"
        # 每次清空讯息
        self.ui.showcar_table.clearContents()
        try:
            self.cursor.execute(sql)
            rowdata = self.cursor.fetchall()
            # DATA[0]:id , DATA[1]:card, DATA[2]:cate, DATA[3]:color, DATA[4]:state, DATA[5]:price
            row = len(rowdata)
            column = 6
            for i in range(len(rowdata)):
                each = rowdata[i]
                for j in range(column):
                    newItem = QTableWidgetItem(str(each[j]))
                    self.ui.showcar_table.setItem(i, j, newItem)
                print("车辆编号: %s \t车牌: %s\t车型: %s\t颜色: %s\t状态: %s\t日租金(每天): %s" % (each[0], each[1], each[2], each[3], each[4], each[5]))

        except:
            self.db.rollback()

    # 由车型查询车辆
    def selectcar(self):

        t = self.condatabase()
        cate = self.ui.edit_selectcar.text().strip()
        mol_cate = '%' + cate + '%'
        sql = "SELECT * FROM carinfo WHERE cate like %s" % repr(mol_cate)
        try:
            self.cursor.execute(sql)
            print('进入1')
            rowdata = self.cursor.fetchall()
            # DATA[0]:id , DATA[1]:card, DATA[2]:cate, DATA[3]:color, DATA[4]:state, DATA[5]:price
            row = len(rowdata)
            column = 6
            for i in range(row):
                each = rowdata[i]
                for j in range(column):
                    newItem = QTableWidgetItem(str(each[j]))
                    self.ui.selectcar_table.setItem(i, j, newItem)
                print("车辆编号: %s \t车牌: %s\t车型: %s\t颜色: %s\t状态: %s\t日租金(每天): %s" % (each[0], each[1], each[2], each[3], each[4], each[5]))

        except:
            self.db.rollback()
            QMessageBox.warning(self.ui, '查询失败', '未查询到该车型车辆信息！！！')
            print("未查询到该车型车辆信息！！")
        self.db.close()


    # 查看我的订单
    def diary(self):

        t = self.condatabase()
        sql = "SELECT * FROM diary WHERE cusname = (SELECT Cname FROM custormerinfo WHERE telephone = %s)" % repr(
            username)
        try:
            self.cursor.execute(sql)
            print('进入1')
            data = self.cursor.fetchall()
            # D[0]:Infoid ,data[1]:carid DATA[2]:carcate, DATA[3]:Cusname, DATA[4]:dtime, DATA[5]:btime, DATA[6]:cost, Data[7]:state
            print("**********欢迎使用秋名山租车系统-您的订单信息如下*******************")
            row = len(data)
            column = 8
            for i in range(row):
                each = data[i]
                for j in range(column):
                    newItem = QTableWidgetItem(str(each[j]))
                    self.ui.diary_table.setItem(i, j, newItem)
                print("订单编号: %d \t车辆编号: %d\t租借车辆: %s\t顾客姓名: %s\t租借时间: %s\t归还时间: %s\t订单金额: %s\t订单状态: %s" % (
                                                        each[0], each[1], each[2], each[3], each[4], each[5], each[6], each[7]))

        except:
            self.db.rollback()
            print('查看失败')
        self.db.close()

    # 查看个人中心
    def private(self):

        t = self.condatabase()
        sql = "SELECT * FROM custormerinfo WHERE telephone = %s" % repr(username)
        try:
            self.cursor.execute(sql)
            print('进入1')
            each = self.cursor.fetchone()
            # m[0]:id , m[1]:Cname, m[2]:Csex, m[3]:telephone, m[4]:Cpassword, m[5]:money
            column = 5
            for j in range(column):
                newItem = QTableWidgetItem(str(each[j + 1]))
                self.ui.private_table.setItem(0, j, newItem)
            print("**********欢迎使用秋名山租车系统-您的个人信息如下*******************")
            print("账户姓名: %s\t账户性别: %s\t电话号码: %s\t账户密码: %s\t账户余额: %d" % (each[1], each[2], each[3], each[4], each[5]))
            return True
        except:
            self.db.rollback()
            print('查看失败')
            return False
        self.db.close()

    # 账户充值
    def add(self):
        t = self.condatabase()

        sql = "SELECT * FROM custormerinfo WHERE telephone = %s" % repr(username)
        try:
            self.cursor.execute(sql)
            print('进入1')
            m = self.cursor.fetchone()
            # m[0]:id , m[1]:Cname, m[2]:Csex, m[3]:telephone, m[4]:Cpassword, m[5]:money
            print("您的余额为: %d" % m[5])
            add = int(self.ui.edit_add.text().strip())
            print("正在充值...")
            self.ui.add_output.setText('正在充值...\n')
            time.sleep(1)
            nowyue = str(m[5] + add)
            sql2 = "UPDATE custormerinfo SET money = %d WHERE telephone = %s" % (m[5] + add, repr(username))
            print('进入2')
            self.cursor.execute(sql2)
            self.db.commit()
            QMessageBox.about(self.ui, '操作成功', '充值成功')
            self.ui.add_output.setText('正在充值...\n充值成功...\n')
            self.ui.edit_yue.setText(nowyue)
            print("充值成功！！！")

        except:
            self.db.rollback()
            print('充值失败')
            QMessageBox.warning(self.ui, '操作失败', '充值失败')
            self.ui.add_output.setText('充值失败...\n')
        self.db.close()

    # 修改密码
    def changepas(self):

        t = self.condatabase()
        sql = "SELECT * FROM custormerinfo WHERE telephone = %s" % repr(username)
        try:
            self.cursor.execute(sql)
            print('进入1')
            self.ui.changepas_output.setText('正在修改...')
            m = self.cursor.fetchone()
            # m[0]:id , m[1]:Cname, m[2]:Csex, m[3]:telephone, m[4]:Cpassword, m[5]:money
            old_pas = self.ui.edit_oldpas.text().strip()
            if old_pas != m[4]:
                print("密码错误，请重新输入")
                QMessageBox.warning(self.ui, '操作失败', '输入密码错误,修改失败')
                self.ui.changepas_output.setText('正在修改...\n输入密码错误，修改失败...')
            else:
                new_pas = self.ui.edit_newpas.text().strip()
                sql2 = "UPDATE custormerinfo SET Cpassword = %s WHERE telephone = %s" % (repr(new_pas), repr(username))
                sql3 = "UPDATE admin SET password  = %s WHERE username = %s" % (repr(new_pas), repr(username))
                print('进入2')
                try:
                    self.cursor.execute(sql2)
                    self.cursor.execute(sql3)

                    self.db.commit()
                    QMessageBox.about(self.ui, '操作成功', '修改密码成功')
                    self.ui.changepas_output.setText('正在修改...\n修改成功...')
                    print("修改成功！！")
                except:
                    self.db.rollback()
                    QMessageBox.about(self.ui, '操作失败', '修改密码失败')
                    self.ui.changepas_output.setText('正在修改...\n密码修改失败...')
                    print("修改失败！！")

        except:
            self.db.rollback()
            QMessageBox.about(self.ui, '操作失败', '修改密码失败')
            self.ui.changepas_output.setText('正在修改...\n密码修改失败...')
        self.db.close()

    # 借车
    def getcar(self):

        t = self.condatabase()
        car_id = int(self.ui.edit_getcarid.text().strip())
        print(car_id)
        sql = "SELECT * FROM carinfo WHERE ID_car = %d" % car_id
        try:
            self.ui.getcar_output.setText('正在租借...')
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
            print('进入1')
            # DATA[0]:id , DATA[1]:card, DATA[2]:cate, DATA[3]:color, DATA[4]:state, DATA[5]:price
            if data[4] == '使用中':
                print('您所指定的车辆已经在使用...请重新操作...')
                QMessageBox.about(self.ui, '操作失败', '该车辆已出借')
                self.ui.getcar_output.setText('正在租借...\n租借失败...\n您所指定的车辆已经在使用...请重新操作...')
            else:
                n = int(self.ui.edit_getcarday.text().strip())
                print(n)
                Cost = n * int(data[5])  # 花费钱

                print("您需要支付: %d" % Cost)
                print('请使用支付宝或微信支付...')

                choice = QMessageBox.question(
                    self.ui,
                    '确认',
                    '您需要支付: %d' % Cost)


                if choice == QMessageBox.Yes:
                    print("你选择YES，支付中...")
                    self.ui.getcar_output.setText('正在租借...\n支付中...')
                    time.sleep(1)
                    # 用用户电话号码作为用户的用户名以及连接外码
                    sqll = "SELECT * FROM custormerinfo WHERE telephone = %s" % repr(username)
                    self.cursor.execute(sqll)
                    print('进入2')
                    m = self.cursor.fetchone()
                    # m[0]:id , m[1]:Cname, m[2]:Csex, m[3]:telephone, m[4]:Cpassword, m[5]:money
                    if m[5] < Cost:
                        print('余额不足，支付失败')
                        QMessageBox.warning(self.ui, '操作失败', '余额不足，支付失败')
                        self.ui.getcar_output.setText('正在租借...\n支付中...\n余额不足，支付失败...\n租借失败...')
                    else:
                        yue = m[5] - Cost
                        # 更新用户余额和汽车状态 以及更新订单情况
                        sql2 = "UPDATE custormerinfo set money = %d WHERE telephone = %s" % (yue, repr(username))
                        sql3 = "update carinfo set state = %s where ID_car = %s" % (repr('使用中'), repr(car_id))

                        # 更新订单情况
                        gday = datetime.datetime.now()
                        bday = gday + datetime.timedelta(days=n)

                        g_day = str(gday)
                        b_day = str(bday)

                        sql4 = "INSERT INTO diary(carid, carcate, cusname, dtime, btime, COST, state) values" \
                               '(%d, %s, %s, %s, %s, %s, %s)' % (
                               car_id, repr(data[2]), repr(m[1]), repr(g_day), repr(b_day), repr(Cost), repr('未归还'))
                        try:
                            self.cursor.execute(sql2)
                            self.cursor.execute(sql3)
                            self.cursor.execute(sql4)
                            print('进入3')
                            self.db.commit()
                        except:
                            self.db.rollback()

                        # 在更新完表信息后再提示
                        print('支付成功...当前余额为%d' % yue)
                        QMessageBox.about(self.ui, '操作成功', '支付成功')
                        self.ui.getcar_output.setText('正在租借...\n支付中...\n支付成功...当前余额为: %d\n租借成功...' % yue)


                elif choice == QMessageBox.No:
                    print("支付失败!!")
                    self.ui.getcar_output.setText('正在租借...\n支付失败...\n租借失败...')
        except:
            self.db.rollback()
            print('未查询到该编号车辆信息!!!')
            QMessageBox.warning(self.ui, '操作失败', '租借失败')
            self.ui.getcar_output.setText('正在租借...\n租借失败, 未查询到该编号车辆信息...')
        self.db.close()

    # 还车
    def backcar(self):

        t = self.condatabase()

        id = int(self.ui.edit_backcarinfoid.text().strip())
        sql2 = "SELECT * FROM diary WHERE Infoid = %d" % id
        try:
            self.ui.backcar_output.setText('正在归还...')
            self.cursor.execute(sql2)
            print('进入1')
            data = self.cursor.fetchone()
            # D[0]:Infoid ,data[1]:carid DATA[2]:carcate, DATA[3]:Cusname, DATA[4]:dtime, DATA[5]:btime, DATA[6]:cost, Data[7]:state
            if data[7] == '已归还':
                print("该订单已归还，无需再次处理")
                QMessageBox.about(self.ui, '操作失败', '该订单已归还')
                self.ui.backcar_output.setText('正在归还...\n该订单已归还，无需再次处理...')
            elif data[7] == '未归还':

                # 更新汽车状态
                print('数据处理中...')
                time.sleep(1)
                print('归还中...')
                self.ui.backcar_output.setText('正在归还...\n归还中...')
                time.sleep(1)
                sql3 = "UPDATE carinfo SET state = %s WHERE ID_car = %d" % (repr('空闲'), data[1])

                # 更新订单状态
                sql4 = "UPDATE diary SET state = %s WHERE Infoid = %d" % (repr('已归还'), data[0])

                try:
                    self.cursor.execute(sql3)
                    self.cursor.execute(sql4)
                    print('进入2')
                    self.db.commit()
                    print("汽车归还成功！！！")
                    QMessageBox.about(self.ui, '操作成功', '汽车归还成功')
                    self.ui.backcar_output.setText('正在归还...\n归还中...\n归还成功...')
                except:
                    self.db.rollback()
                    print("汽车归还失败！！！")
                    QMessageBox.warning(self.ui, '操作失败', '汽车归还失败')
                    self.ui.backcar_output.setText('正在归还...\n归还中...\n归还失败...')
        except:
            self.db.rollback()
            print('未查询到该订单信息!!!')
            QMessageBox.warning(self.ui, '操作失败', '未查询到该订单信息')
            self.ui.backcar_output.setText('正在归还...\n未查询到该订单信息...\n归还失败...')
        self.db.close()