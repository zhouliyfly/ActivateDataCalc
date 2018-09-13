# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
# from main_action import MainAction
import main_action
from PyQt5 import sip  # 为了打包exe文件包含的库


class UiMainWindow(object):
    def __init__(self, mian_window):
        self.main_window = mian_window

        # 初始化UI
        self.setup_ui()

        # 创建活动处理对象
        self.main_action = main_action.MainAction(self)

        # 创建线程
        self.thread = main_action.WorkThread(self)
        self.thread.trigger[str].connect(self.set_msg_statusbar)
        self.thread.trigger[bool].connect(self.change_button_status)

        # 初始化按键响应
        self.button_dingdan.clicked.connect(self.main_action.on_button_dingdan_clicked)
        self.button_tejia.clicked.connect(self.main_action.on_button_tejia_clicked)
        self.button_manjian.clicked.connect(self.main_action.on_button_manjian_clicked)
        self.button_output.clicked.connect(self.main_action.on_button_output_clicked)
        self.generate_data_button.clicked.connect(self.main_action.on_generate_data_button_clicked)

    def setup_ui(self):
        self.main_window.setObjectName("main_window")
        self.main_window.resize(558, 296)
        self.centralWidget = QtWidgets.QWidget(self.main_window)
        self.centralWidget.setObjectName("centralWidget")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(40, 40, 491, 121))
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
        self.label_manjian = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_manjian.setObjectName("label_manjian")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_manjian)
        self.button_tejia = QtWidgets.QPushButton(self.formLayoutWidget)
        self.button_tejia.setObjectName("button_tejia")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.button_tejia)
        self.label_tejia = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_tejia.setObjectName("label_tejia")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.label_tejia)
        self.button_manjian = QtWidgets.QPushButton(self.formLayoutWidget)
        self.button_manjian.setObjectName("button_manjian")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.button_manjian)
        self.button_output = QtWidgets.QPushButton(self.formLayoutWidget)
        self.button_output.setObjectName("button_output")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.button_output)
        self.label_output = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_output.setObjectName("label_output")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.label_output)
        self.generate_data_button = QtWidgets.QPushButton(self.centralWidget)
        self.generate_data_button.setGeometry(QtCore.QRect(40, 210, 75, 23))
        self.generate_data_button.setObjectName("generate_data_button")
        self.main_window.setCentralWidget(self.centralWidget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.main_window)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.main_window.setWindowTitle(_translate("main_window", "数据生成工具"))
        self.button_dingdan.setText(_translate("main_window", "导入订单表"))
        self.label_dingdan.setText(_translate("main_window", "文件路径"))
        self.label_manjian.setText(_translate("main_window", "文件路径"))
        self.button_tejia.setText(_translate("main_window", "导入特价表"))
        self.label_tejia.setText(_translate("main_window", "文件路径"))
        self.button_manjian.setText(_translate("main_window", "导入满减表"))
        self.button_output.setText(_translate("main_window", "数据文件输出路径选择"))
        self.label_output.setText(_translate("main_window", "."))
        self.generate_data_button.setText(_translate("main_window", "生成数据"))

    def set_msg_statusbar(self, msg):
        self.main_window.statusBar().showMessage(msg)

    def change_button_status(self, stat):
        self.generate_data_button.setEnabled(stat)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
