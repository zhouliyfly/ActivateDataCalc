# -*- coding: utf-8 -*-

"""
Module implementing action.
"""
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtWidgets
import active_calc


class MainAction(QMainWindow):
    def __init__(self, ui_main):
        super().__init__()
        self.ui_main = ui_main
        # 初始化路径
        # 输出路径默认为当前目录
        self.table_paths = dict()
        self.table_paths['dingdan'] = ""
        self.table_paths['manjian'] = ""
        self.table_paths['tejia'] = ""
        self.table_paths['zhuanqumanjian'] = ""
        self.table_paths['jietimanjian'] = ""
        self.table_paths['output'] = "."
        self.manjian_threshold = 0
        self.manjian_cost = 0

    def on_button_dingdan_clicked(self):
        self.table_paths['dingdan'], _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                               '打开文件', './',
                                                                               "Excel 文件(*.xls;*.xlsx)")
        self.ui_main.label_dingdan.setText(self.table_paths['dingdan'])

    def on_button_tejia_clicked(self):
        self.table_paths['tejia'], _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                             "打开文件", "./",
                                                                             "Excel 文件(*.xls;*.xlsx)")
        self.ui_main.label_tejia.setText(self.table_paths['tejia'])

    def on_button_manjian_clicked(self):
        self.table_paths['manjian'], _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                               "打开文件", "./",
                                                                               "Excel 文件(*.xls;*.xlsx)")
        self.ui_main.label_manjian.setText(self.table_paths['manjian'])

    def on_button_output_clicked(self):
        self.table_paths['output'] = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                                                "打开文件夹", "./")
        if self.table_paths['output'] == "":
            self.table_paths['output'] = "."

        self.ui_main.label_output.setText(self.table_paths['output'])

    def on_button_zqmanjian_clicked(self):
        self.table_paths['zhuanqumanjian'], _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                                      "打开文件", "./",
                                                                                      "Excel 文件(*.xls;*.xlsx)")
        self.ui_main.label_zqmanjian.setText(self.table_paths['zhuanqumanjian'])

    def on_button_jietimanjian_clicked(self):
        self.table_paths['jietimanjian'], _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                                    "打开文件", "./",
                                                                                    "Excel 文件(*.xls;*.xlsx)")
        self.ui_main.label_jietimanjian.setText(self.table_paths['jietimanjian'])

    def on_button_generate_all_data_clicked(self):
        # 获取输入框数据（暂时放在这里，下个版本需要挪走这部分数据）
        self.manjian_threshold = self.ui_main.lineEdit_zqmanjian_threshold.text()
        self.manjian_cost = self.ui_main.lineEdit_zqmanjian_cost.text()

        # 启动线程计算数据
        self.ui_main.button_generate_all_data.setEnabled(False)  # 生成数据按钮暂时禁用
        self.ui_main.thread.start()  # 开启线程执行数据计算

    def calc_all_data(self, trigger):
        print("开始生成数据...")
        trigger.emit("开始生成数据...")

        if self.table_paths['dingdan'] == "":
            print("找不到订单表！")
            trigger.emit("找不到订单表！")
        elif self.table_paths['manjian'] == "" and \
                self.table_paths['tejia'] == "" and \
                self.table_paths['zhuanqumanjian'] == "" and \
                self.table_paths['jietimanjian'] == "":
            print("找不到活动表！")
            trigger.emit("找不到活动表！")
        else:
            # 每次点击“生成数据”都会重新读取表格数据进行计算。acontext是临时局部变量，
            # 若是想要读取表格数据和计算活动分开，需要分拆这两个步骤。并将获取的表格数据保存为类成员变量
            acontext = active_calc.ActiveContext(self)
            status = acontext.active_calc()

            # 此处待优化
            if status:
                trigger.emit("已成功生成活动表！")
            else:
                trigger.emit("数据生成失败！")


class WorkThread(QThread):
    trigger = pyqtSignal([str], [bool])

    def __init__(self, ui_main):
        super().__init__()
        self.ui_main = ui_main

    def run(self):
        self.ui_main.main_action.calc_all_data(self.trigger)
        self.trigger[bool].emit(True)
