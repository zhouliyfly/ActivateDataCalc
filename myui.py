# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myui.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QColorDialog, QFontDialog, QTextEdit, QFileDialog
from script import read_table_and_cacl
from PyQt5 import sip


class Ui_Form(object):
    def setupUi(self, Form):
        self.QWidget = Form  # 自己用，很多地方需要QWidget参数
        self.table_paths = dict()
        Form.setObjectName("Form")
        Form.resize(500, 291)
        self.formLayoutWidget = QtWidgets.QWidget(Form)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 50, 450, 103))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")

        self.button_dingdan = QtWidgets.QPushButton(self.formLayoutWidget)
        self.button_dingdan.setObjectName("button_dingdan")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.button_dingdan)
        self.label_dingdan = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_dingdan.setObjectName("label_dingdan")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_dingdan)

        self.button_manjian = QtWidgets.QPushButton(self.formLayoutWidget)
        self.button_manjian.setObjectName("button_manjian")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.button_manjian)
        self.label_manjian = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_manjian.setObjectName("label_manjian")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_manjian)

        self.button_tejia = QtWidgets.QPushButton(self.formLayoutWidget)
        self.button_tejia.setObjectName("button_tejia")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.button_tejia)
        self.label_tejia = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_tejia.setObjectName("label_tejia")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.label_tejia)

        self.button_output = QtWidgets.QPushButton(self.formLayoutWidget)
        self.button_output.setObjectName("button_output")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.button_output)
        self.label_output = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_output.setObjectName("label_output")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.label_output)

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(30, 210, 75, 23))
        self.pushButton.setObjectName("pushButton")
        # self.textBrowser = QtWidgets.QTextBrowser(Form)
        # self.textBrowser.setEnabled(True)
        # self.textBrowser.setGeometry(QtCore.QRect(220, 200, 161, 81))
        # self.textBrowser.setObjectName("textBrowser")
        self.label_status = QtWidgets.QLabel(Form)
        self.label_status.setGeometry(QtCore.QRect(280, 260, 131, 20))
        self.label_status.setObjectName("label_status")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "数据生成小工具"))
        self.button_dingdan.setText(_translate("Form", "导入订单表"))
        self.label_dingdan.setText(_translate("Form", "文件路径"))
        self.label_tejia.setText(_translate("Form", "文件路径"))
        self.button_tejia.setText(_translate("Form", "导入特价表"))
        self.label_manjian.setText(_translate("Form", "文件路径"))
        self.button_manjian.setText(_translate("Form", "导入满减表"))

        self.label_output.setText(_translate("Form", "./"))
        self.button_output.setText(_translate("Form", "数据文件输出路径选择"))
        self.pushButton.setText(_translate("Form", "生成数据"))

        # 初始化路径
        # 输出路径默认为当前目录
        self.table_output = "."
        self.table_dingdan = ""
        self.table_tejia = ""
        self.table_manjian = ""
        self.table_paths['dingdan'] = self.table_dingdan
        self.table_paths['manjian'] = self.table_manjian
        self.table_paths['tejia'] = self.table_tejia
        self.table_paths['output'] = self.table_output

        self.button_dingdan.clicked.connect(self.ui_action)
        self.button_tejia.clicked.connect(self.ui_action)
        self.button_manjian.clicked.connect(self.ui_action)
        self.button_output.clicked.connect(self.ui_action)
        self.pushButton.clicked.connect(self.ui_action)

    def ui_action(self):
        self.label_status.setText(" ")
        sender = self.QWidget.sender()
        if sender.text() == "导入订单表":
            self.table_dingdan, _ = QFileDialog.getOpenFileName(self.QWidget, '打开文件', './', "Excel 文件(*.xls;*.xlsx)")
            self.label_dingdan.setText(self.table_dingdan)
            self.table_paths['dingdan'] = self.table_dingdan
            print(self.table_dingdan)
        elif sender.text() == "导入特价表":
            self.table_tejia, _ = QFileDialog.getOpenFileName(self.QWidget, '打开文件', './', "Excel 文件(*.xls;*.xlsx)")
            self.label_tejia.setText(self.table_tejia)
            self.table_paths['tejia'] = self.table_tejia
            print(self.table_tejia)
        elif sender.text() == "导入满减表":
            self.table_manjian, _ = QFileDialog.getOpenFileName(self.QWidget, '打开文件', './', "Excel 文件(*.xls;*.xlsx)")
            self.label_manjian.setText(self.table_manjian)
            self.table_paths['manjian'] = self.table_manjian
            print(self.table_manjian)
        elif sender.text() == "数据文件输出路径选择":
            self.table_output = QFileDialog.getExistingDirectory(self.QWidget, '打开文件夹', './')
            if self.table_output == "":
                self.table_output = "."
            self.label_output.setText(self.table_output)
            self.table_paths['output'] = self.table_output
            print(self.table_output)
        elif sender.text() == "生成数据":
            print("开始生成数据")

            if self.table_paths['dingdan'] == "":
                print("找不到订单表！")
                self.label_status.setText("找不到订单表！")
            elif self.table_paths['manjian'] == "" and self.table_paths['tejia'] == "":
                print("找不到满减表或特价表！")
                self.label_status.setText("找不到满减表或特价表！")
            else:
                print(self.table_paths)
                sign1, sign2 = read_table_and_cacl(self.table_paths)
                if sign1 == 1 and sign2 == 1:
                    self.label_status.setText("已成功生成满减活动表和特价活动表！")
                elif sign1 == 1:
                    self.label_status.setText("已成功生成满减活动表！")
                elif sign2 == 1:
                    self.label_status.setText("已成功生成特价活动表！")
                else:
                    pass
        else:
            pass


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
