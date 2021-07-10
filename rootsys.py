from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton,  QPlainTextEdit,QMessageBox
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QIcon
from share import glovar
from PyQt5.QtWidgets import *
import pymysql
import time, random

# 后台管理界面
user = 'root'
pas = '123456'

class root_win():

    def __init__(self):

        # 动态加载ui文件
        self.ui = uic.loadUi("ui/root.ui")

        # 界面控件部分

        # 查询部分按钮
        self.ui.showcar_table.setRowCount(50)
        self.ui.diary_table.setRowCount(50)
        self.ui.showuser_table.setRowCount(20)
        self.ui.showcar_btn.clicked.connect(self.showcar)
        self.ui.showdiary_btn.clicked.connect(self.diary)
        self.ui.showuser_btn.clicked.connect(self.showcustormer)

        # 查询车辆按钮
        self.ui.selectcarid_btn.clicked.connect(self.selectcar)
        self.ui.edit_selectcarid.returnPressed.connect(self.selectcar)
        self.ui.selectcar_table.setRowCount(10)

        # 删除车辆按钮
        self.ui.delectcar_btn.clicked.connect(self.delectecar)
        self.ui.edit_delectcarid.returnPressed.connect(self.delectecar)

        # 修改车辆按钮
        self.ui.updatecar_btn.clicked.connect(self.updatecar)
        self.ui.edit_updaterent.returnPressed.connect(self.updatecar)

        # 添加车辆按钮
        self.ui.catebox.addItems(['','雪铁龙新爱丽舍', '别克昂科拉', '宝马3系', '宝马5系', '比亚迪秦', '别克凯越',
                                   '别克君越', '上汽大通G10', '大众帕萨特', '雪佛兰迈锐宝', '奥迪A6', '丰田雷凌'])

        self.ui.colorbox.addItems(['','黑色', '白色', '蓝色', '红色'])
        self.ui.addcar_btn.clicked.connect(self.addcar)
        self.ui.createcarid_btn.clicked.connect(self.createcarid)

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

        sql = "select * from carinfo"
        # 每次清空讯息
        self.ui.showcar_table.clearContents()
        try:
            self.cursor.execute(sql)
            rowdata = self.cursor.fetchall()
            # DATA[0]:id , DATA[1]:card, DATA[2]:cate, DATA[3]:color, DATA[4]:state, DATA[5]:price
            row = len(rowdata)
            column = 6
            for i in range(row):
                each = rowdata[i]
                for j in range(column):
                    newItem = QTableWidgetItem(str(each[j]))
                    self.ui.showcar_table.setItem(i, j, newItem)
                print("车辆编号: %s \t车牌: %s\t车型: %s\t颜色: %s\t状态: %s\t日租金(每天): %s" % (each[0], each[1], each[2], each[3], each[4], each[5]))

        except:
            self.db.rollback()

    # 查看订单
    def diary(self):
        t = self.condatabase()
        sql = "SELECT * FROM diary"
        try:
            self.cursor.execute(sql)
            rowdata = self.cursor.fetchall()
            # D[0]:Infoid , DATA[1]:carcate, DATA[2]:Cusname, DATA[3]:dtime, DATA[4]:btime, DATA[5]:cost, Data[6]:state
            row = len(rowdata)
            column = 8
            for i in range(row):
                each = rowdata[i]
                for j in range(column):
                    newItem = QTableWidgetItem(str(each[j]))
                    self.ui.diary_table.setItem(i, j, newItem)
                print("订单编号: %d \t车辆编号: %d\t租借车辆: %s\t顾客姓名: %s\t租借时间: %s\t归还时间: %s\t订单金额: %s\t订单状态: %s" % (each[0], each[1], each[2], each[3], each[4], each[5], each[6], each[7]))

        except:
            self.db.rollback()
        self.db.close()

    # 查看用户
    def showcustormer(self):
        t = self.condatabase()

        sql = "SELECT * FROM custormerinfo"
        try:
            self.cursor.execute(sql)
            rowdata = self.cursor.fetchall()
            # m[0]:id , m[1]:Cname, m[2]:Csex, m[3]:telephone, m[4]:Cpassword, m[5]:money
            row = len(rowdata)
            column = 6
            for i in range(row):
                each = rowdata[i]
                for j in range(column):
                    newItem = QTableWidgetItem(str(each[j]))
                    self.ui.showuser_table.setItem(i, j, newItem)
                print("用户id: %d\t用户姓名: %s\t用户性别: %s\t电话号码: %s\t账户密码: %s\t账户余额: %d" % (each[0], each[1], each[2], each[3], each[4], each[5]))

        except:
            self.db.rollback()
        self.db.close()

    # 查询车辆
    def selectcar(self):
        ID_car = int(self.ui.edit_selectcarid.text().strip())

        print(ID_car)

        t = self.condatabase()

        sql = 'select * from carinfo where ID_car = %d' % ID_car
        try:
            self.cursor.execute(sql)
            each = self.cursor.fetchone()
            # DATA[0]:id , DATA[1]:card, DATA[2]:cate, DATA[3]:color, DATA[4]:state, DATA[5]:price
            column = 6
            for j in range(column):
                newItem = QTableWidgetItem(str(each[j]))
                self.ui.selectcar_table.setItem(0, j, newItem)
            print("车辆编号: %s \t车牌: %s\t车名: %s\t颜色: %s\t状态: %s\t日租金: %s" % (each[0], each[1], each[2], each[3], each[4], each[5]))
            return True

        except:
            self.db.rollback()
            QMessageBox.about(self.ui, '查询失败', '未查询到该编号车辆信息！！！')
            print("未查询到该编号车辆信息！！")
            return False

        self.db.close()

    # 删除车辆
    def delectecar(self):
        t = self.condatabase()
        ID_car = int(self.ui.edit_delectcarid.text().strip())
        print(ID_car)
        sql = "select * from carinfo WHERE ID_car = %d" % ID_car
        self.ui.delectcar_output.setText('''删除车辆中...\n''')
        try:
            self.cursor.execute(sql)
            print('进入1')
            data = self.cursor.fetchone()
          #  each = data
           # print("车辆编号: %s \t车牌: %s\t车名: %s\t颜色: %s\t状态: %s\t日租金: %s" % (each[0], each[1], each[2], each[3], each[4], each[5]))

          #  print('进入1.5')

            print('进入2')
            time.sleep(1)
            # DATA[0]:id_car , DATA[1]:card, DATA[2]:cate, DATA[3]:color, DATA[4]:state, DATA[5]:price
            if data[4] == '使用中':
                QMessageBox.warning(self.ui, '操作失败', '该车辆正在使用中，无法删除！！！')
                self.ui.delectcar_output.setText('''删除车辆中...\n该车辆正在使用中，删除失败...\n''')
                print("该车辆正在使用中，无法删除")
            else:
                sql2 = "delete from carinfo where ID_car = %d" % ID_car
                self.cursor.execute(sql2)
                self.db.commit()  # 原数据库实现删除 提交数据
                QMessageBox.about(self.ui, '操作成功', '成功删除该车辆信息')
                self.ui.delectcar_output.setText('删除车辆中...\n删除成功...\n')
                print('删除成功！！！')
        except:
            self.db.rollback()
            QMessageBox.warning(self.ui, '操作失败', '不存在该编号车辆信息！！！')
            self.ui.delectcar_output.setText('删除车辆中...\n不存在当前车辆信息，删除失败...\n')
            print('不存在当前车辆信息!!!')

        self.db.close()

    # 更新车辆
    def updatecar(self):
        t = self.condatabase()
        ID_car = int(self.ui.edit_updatecarid.text().strip())
        sql = "select * from carinfo WHERE ID_car = %d" % ID_car
        self.ui.updatecar_output.setText('''修改车辆中...\n''')
        try:
            self.cursor.execute(sql)
            print('进入1')
            data = self.cursor.fetchone()
            print('进入2')
            time.sleep(1)
            # DATA[0]:id_car , DATA[1]:card, DATA[2]:cate, DATA[3]:color, DATA[4]:state, DATA[5]:price
            if data[4] == '使用中':
                QMessageBox.warning(self.ui, '操作失败', '该车辆正在使用中，无法修改！！！')
                #time.sleep(1)
                self.ui.updatecar_output.setText('''修改车辆中...\n该车辆正在使用中，修改失败...\n''')
                print("该车辆正在使用中，无法删除")
            else:
                price = self.ui.edit_updaterent.text().strip()
                sql2 = "UPDATE carinfo SET price = %s WHERE ID_car = %s" % (repr(price), repr(ID_car))
                try:
                    self.cursor.execute(sql2)
                    self.db.commit()
                    QMessageBox.about(self.ui, '操作成功', '成功修改该车辆信息')
                    #time.sleep(1)
                    self.ui.updatecar_output.setText('''修改车辆中...\n修改成功...\n''')
                    print('更新车辆信息成功!!!')
                except:
                    self.db.rollback()
                    QMessageBox.warning(self.ui, '操作失败', '修改该车辆信息失败')
                    #time.sleep(1)
                    self.ui.updatecar_output.setText('''修改车辆中...\n金额修改失败...\n''')
                    print('更新车辆信息失败！！！')
        except:
            self.db.rollback()
            QMessageBox.warning(self.ui, '操作失败', '不存在该编号车辆信息！！！')
            #time.sleep(1)
            self.ui.updatecar_output.setText('''修改车辆中...\n不存在当前车辆信息，修改失败...\n''')
            print('不存在当前车辆信息!!!')
        self.db.close()

    # 增加车辆
    def addcar(self):
        t = self.condatabase()
        cate = self.ui.catebox.currentText()
        color = self.ui.colorbox.currentText()
        state = '空闲'
        price = str(self.ui.pricebox.value())
        sql = "insert into carinfo(card, cate, color, state, price) values " \
              "(%s, %s, %s, %s, %s)" % (repr(card), repr(cate), repr(color), repr(state), repr(price))
        self.ui.addcar_output.setText('''添加车辆中...\n''')
        try:
            self.cursor.execute(sql)
            print('进入1')
            time.sleep(1)
            self.db.commit()
            QMessageBox.about(self.ui, '操作成功', '添加车辆成功')
            # time.sleep(1)
            self.ui.addcar_output.setText('''添加车辆中...\n添加成功...\n''')
            print('添加车辆信息成功!!!')
        except:
            self.db.rollback()
            QMessageBox.warning(self.ui, '操作失败', '添加车辆失败')
            # time.sleep(1)
            self.ui.addcar_output.setText('''添加车辆中...\n添加失败...\n''')
        self.db.close()

    # 生成车牌
    def createcarid(self):
        global card
        card = self.car_num()
        self.ui.edit_createcarid.setText(card)

    # 获取车牌函数
    # 随机生成一个车牌号码
    def car_num(self):
        char0 = ["京", "津", "沪", "渝", "冀", "豫", "云", "辽", "黑", "湘", "皖", "鲁", "新", "苏", "浙", "赣", "鄂", "桂", "甘", "晋",
                 "蒙",
                 "陕", "吉", "闽", "赣", "粤", "青", "藏", "川", "宁", "琼"]  # 省份简称
        char1 = 'ABCDEFGHJKLMNPQRSTUVWXYZ'  # 车牌号中没有I和O
        char2 = '0123456789ABCDEFGHJKLMNPQRSTUVWXYZ'

        id_1 = random.choice(char0)  # 车牌号第一位     省份简称
        id_2 = ''.join(random.sample(char1, 1))  # 车牌号第二位

        while True:
            id_3 = ''.join(random.sample(char2, 5))
            v = id_3.isalpha()  # 所有字符都是字母时返回 true
            if v == True:
                continue
            else:
                car_id = id_1 + id_2 + id_3
                # print car_id
                break

        return car_id
