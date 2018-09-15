# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
# from main_action import MainAction
import main_action
from PyQt5 import sip  # 为了打包exe文件包含的库


class UiMainWindow(object):
    _Version = '1.3'  # 版本号

    def __init__(self, main_window):
        self.main_window = main_window

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
        self.button_generate_all_data.clicked.connect(self.main_action.on_button_generate_all_data_clicked)
        self.button_zqmanjian.clicked.connect(self.main_action.on_button_zqmanjian_clicked)

    def setup_ui(self):
        self.main_window.setObjectName("main_window")
        self.main_window.resize(613, 338)
        self.centralWidget = QtWidgets.QWidget(self.main_window)
        self.centralWidget.setObjectName("centralWidget")
        self.formLayoutWidget_2 = QtWidgets.QWidget(self.centralWidget)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(40, 42, 491, 112))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget_2)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.button_manjian = QtWidgets.QPushButton(self.formLayoutWidget_2)
        self.button_manjian.setObjectName("button_manjian")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.button_manjian)
        self.label_manjian = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_manjian.setObjectName("label_manjian")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_manjian)
        self.button_tejia = QtWidgets.QPushButton(self.formLayoutWidget_2)
        self.button_tejia.setObjectName("button_tejia")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.button_tejia)
        self.label_tejia = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_tejia.setObjectName("label_tejia")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.label_tejia)
        self.button_dingdan = QtWidgets.QPushButton(self.formLayoutWidget_2)
        self.button_dingdan.setObjectName("button_dingdan")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.button_dingdan)
        self.label_dingdan = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_dingdan.setObjectName("label_dingdan")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_dingdan)
        self.button_zqmanjian = QtWidgets.QPushButton(self.formLayoutWidget_2)
        self.button_zqmanjian.setObjectName("button_zqmanjian")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.button_zqmanjian)
        self.label_zqmanjian = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_zqmanjian.setObjectName("label_zqmanjian")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.label_zqmanjian)
        self.formLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(40, 240, 491, 54))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout_2 = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.button_output = QtWidgets.QPushButton(self.formLayoutWidget)
        self.button_output.setObjectName("button_output")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.button_output)
        self.label_output = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_output.setObjectName("label_output")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_output)
        self.button_generate_all_data = QtWidgets.QPushButton(self.formLayoutWidget)
        self.button_generate_all_data.setObjectName("button_generate_all_data")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.button_generate_all_data)
        self.splitter = QtWidgets.QSplitter(self.centralWidget)
        self.splitter.setGeometry(QtCore.QRect(40, 170, 379, 21))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.label_zqmanjian_threshold = QtWidgets.QLabel(self.splitter)
        self.label_zqmanjian_threshold.setObjectName("label_zqmanjian_threshold")
        self.lineEdit_zqmanjian_threshold = QtWidgets.QLineEdit(self.splitter)
        self.lineEdit_zqmanjian_threshold.setObjectName("lineEdit_zqmanjian_threshold")
        self.label_zqmanjian_cost = QtWidgets.QLabel(self.splitter)
        self.label_zqmanjian_cost.setObjectName("label_zqmanjian_cost")
        self.lineEdit_zqmanjian_cost = QtWidgets.QLineEdit(self.splitter)
        self.lineEdit_zqmanjian_cost.setObjectName("lineEdit_zqmanjian_cost")
        self.main_window.setCentralWidget(self.centralWidget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.main_window)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.main_window.setWindowTitle(_translate("main_window", "数据生成工具 -v{0} ".format(UiMainWindow._Version)))
        self.button_dingdan.setText(_translate("main_window", "导入订单表"))
        self.label_dingdan.setText(_translate("main_window", "文件路径"))
        self.label_manjian.setText(_translate("main_window", "文件路径"))
        self.button_tejia.setText(_translate("main_window", "导入特价表"))
        self.label_tejia.setText(_translate("main_window", "文件路径"))
        self.button_manjian.setText(_translate("main_window", "导入满减表"))
        self.button_output.setText(_translate("main_window", "数据文件输出路径选择"))
        self.label_output.setText(_translate("main_window", "."))
        self.button_generate_all_data.setText(_translate("main_window", "生成数据"))
        self.button_zqmanjian.setText(_translate("MainWindow", "导入打包满减表"))
        self.label_zqmanjian.setText(_translate("MainWindow", "文件路径"))
        self.label_zqmanjian_threshold.setText(_translate("MainWindow", "满减门槛"))
        self.label_zqmanjian_cost.setText(_translate("MainWindow", "满减金额"))
        self.lineEdit_zqmanjian_threshold.setText(_translate("main_window", "0"))
        self.lineEdit_zqmanjian_cost.setText(_translate("main_window", "0"))

    def set_msg_statusbar(self, msg):
        self.main_window.statusBar().showMessage(msg)

    def change_button_status(self, stat):
        self.button_generate_all_data.setEnabled(stat)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
