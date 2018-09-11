import active_calc
from PyQt5 import QtWidgets


class MyAction(object):
    def __init__(self, ui_window):
        self.ui_obj = ui_window
        # 初始化路径
        # 输出路径默认为当前目录
        self.table_paths = dict()
        self.table_paths['dingdan'] = ""
        self.table_paths['manjian'] = ""
        self.table_paths['tejia'] = ""
        self.table_paths['output'] = "."

    def ui_action(self):
        self.ui_obj.label_status.setText(" ")
        sender = self.ui_obj.QWidget.sender()
        if sender.text() == "导入订单表":
            self.table_paths['dingdan'], _ = QtWidgets.QFileDialog.getOpenFileName(self.ui_obj.QWidget,
                                                                                   '打开文件', './',
                                                                                   "Excel 文件(*.xls;*.xlsx)")
            self.ui_obj.label_dingdan.setText(self.table_paths['dingdan'])
            print(self.table_paths['dingdan'])
        elif sender.text() == "导入特价表":
            self.table_paths['tejia'], _ = QtWidgets.QFileDialog.getOpenFileName(self.ui_obj.QWidget,
                                                                                 "打开文件", "./",
                                                                                 "Excel 文件(*.xls;*.xlsx)")
            self.ui_obj.label_tejia.setText(self.table_paths['tejia'])
            print(self.table_paths['tejia'])
        elif sender.text() == "导入满减表":
            self.table_paths['manjian'], _ = QtWidgets.QFileDialog.getOpenFileName(self.ui_obj.QWidget,
                                                                                   "打开文件", "./",
                                                                                   "Excel 文件(*.xls;*.xlsx)")
            self.ui_obj.label_manjian.setText(self.table_paths['manjian'])
            print(self.table_paths['manjian'])
        elif sender.text() == "数据文件输出路径选择":
            self.table_paths['output'] = QtWidgets.QFileDialog.getExistingDirectory(self.ui_obj.QWidget,
                                                                                    "打开文件夹", "./")
            if self.table_paths['output'] == "":
                self.table_paths['output'] = "."

            self.ui_obj.label_output.setText(self.table_paths['output'])
            print(self.table_paths['output'])
        elif sender.text() == "生成数据":
            self.calc_data()
        else:
            pass

    def calc_data(self):
        print("开始生成数据...")

        if self.table_paths['dingdan'] == "":
            print("找不到订单表！")
            self.ui_obj.label_status.setText("找不到订单表！")
        elif self.table_paths['manjian'] == "" and self.table_paths['tejia'] == "":
            print("找不到满减表或特价表！")
            self.ui_obj.label_status.setText("找不到满减表或特价表！")
        else:
            # 每次点击“生成数据”都会重新读取表格数据进行计算。acontext是临时局部变量，
            # 若是想要读取表格数据和计算活动分开，需要分拆这两个步骤。并将获取的表格数据保存为类成员变量
            acontext = active_calc.ActiveContext(self.table_paths)
            status = acontext.active_calc()

            # 此处待优化
            if status:
                self.ui_obj.label_status.setText("已成功生成活动表！")
