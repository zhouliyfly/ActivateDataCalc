import pandas as pd
import os


# 活动类
class Active(object):
    """活动基类

    Attributes:
    """

    def calculate_active_data(self, active_context):
        pass


# 满减活动
class ManJian(Active):
    """计算满减活动表

    Attributes:
    """

    def calculate_active_data(self, active_context):
        """

        Args:
            active_context: 活动上下文类，记录表格原文件路径和表格数据
        """
        df_dingdan = active_context.tables['dingdan']
        df_manjian = active_context.tables['manjian']
        output_path = active_context.table_paths['output_path']

        df_order = df_dingdan[[u'订单编号', u'下单时间', u'商品编号', u'商品价格', u'商品数量']]
        df_order[u'下单时间'] = pd.to_datetime(df_order[u'下单时间'])
        df_activity = df_manjian[[u'开始时间', u'结束时间', u'编码', u'数量', u'满减']]
        df_activity[u'开始时间'] = pd.to_datetime(df_activity[u'开始时间'])
        df_activity[u'结束时间'] = pd.to_datetime(df_activity[u'结束时间'])

        df_merge = pd.merge(df_order, df_activity, left_on=u'商品编号', right_on=u'编码')
        df_mer_time = df_merge[(df_merge[u'下单时间'] >= df_merge[u'开始时间']) & (df_merge[u'下单时间'] <= df_merge[u'结束时间'])]
        df_salessum = pd.merge(df_dingdan, df_mer_time, on=[u'订单编号', u'商品编号'])
        df_mer_activity = df_mer_time[df_mer_time[u'商品数量'] >= df_mer_time[u'数量']]
        df_tmp = df_mer_activity.loc[:, [u'订单编号', u'商品编号', u'数量', u'满减']]
        df_activityorder = pd.merge(df_dingdan, df_tmp, on=[u'订单编号', u'商品编号'])
        df_activityorder['费用'] = (df_activityorder['商品数量'] / df_activityorder['数量']) // 1 \
                                 * df_activityorder['满减']

        output_path = os.path.join(output_path, '满减活动表.xlsx')
        writer = pd.ExcelWriter(output_path)
        df_activityorder.to_excel(writer, u'活动订单表')
        df_salessum.to_excel(writer, u'总销量订单表')
        writer.save()
        print("已成功生成满减活动表！")


# 特价活动
class TeJia(Active):
    def calculate_active_data(self, active_context):
        """

        Args:
            active_context:活动上下文类，记录表格原文件路径和表格数据
        """
        df_dingdan = active_context.tables['dingdan']
        df_tejia = active_context.tables['tejia']
        output_path = active_context.table_paths['output']

        df_activity = df_tejia[[u'编码', u'药帮忙价', u'活动价']]
        df_order = df_dingdan[[u'订单编号', u'下单时间', u'商品编号', u'商品价格', u'商品数量']]
        df_merge = pd.merge(df_order, df_activity, left_on=u'商品编号', right_on=u'编码')
        df_mer_activity = df_merge[df_merge[u'商品价格'] == df_merge[u'活动价']]
        df_tmp = df_mer_activity.loc[:, [u'订单编号', u'商品编号', u'药帮忙价']]
        df_activityorder = pd.merge(df_dingdan, df_tmp, on=[u'订单编号', u'商品编号'])
        df_activityorder['费用'] = (df_activityorder['药帮忙价'] - df_activityorder['商品价格']) \
                                 * df_activityorder['商品数量']

        output_path = os.path.join(output_path, '特价活动表.xlsx')
        writer = pd.ExcelWriter(output_path)
        df_activityorder.to_excel(writer, u'活动订单表')
        writer.save()
        print("已成功生成特价活动表！")

#############################
# 工厂类
#############################
class IActiveFactory(object):
    def create_active(self):
        pass


# 满减活动工厂
class ManJianFactory(IActiveFactory):
    def create_active(self):
        """

        Returns:返回满减活动类

        """
        return ManJian()


# 特价活动工厂
class TeJiaFactory(IActiveFactory):
    def create_active(self):
        """

        Returns:返回特价活动类

        """
        return TeJia()


# 上下文类
class ActiveContext(object):
    def __init__(self, table_paths):
        """

        Args:
            table_paths (object): 字典类型。记录数据文件路径
        """
        self.active_factory = []
        self.table_paths = table_paths
        self.tables = dict()
        self.set_parametes()

    def set_parametes(self):
        """根据用户选择项生成对应活动类

        Returns:
            object:
        """
        if self.table_paths['manjian'] != "":
            self.active_factory.append(ManJianFactory())
        if self.table_paths['tejia'] != "":
            self.active_factory.append(TeJiaFactory())

    def read_table(self):
        """读取数据文件

        Returns:文件读取成功返回True，否则返回False

        """
        print("读取订单表...")
        try:
            self.tables['dingdan'] = pd.read_excel(self.table_paths['dingdan'])
        except:
            print('读取订单表出错')
            return False
        else:
            print("订单表读取成功")

        try:
            if self.table_paths['manjian'] != "":
                self.tables['manjian'] = pd.read_excel(self.table_paths['manjian'])
            if self.table_paths['tejia'] != "":
                self.tables['tejia'] = pd.read_excel(self.table_paths['tejia'])
        except:
            print('读取满减表或特价表出错')
            return False
        else:
            print("满减表或特价表读取成功")

        return True

    def active_calc(self):
        """计算并生成活动表

        Returns:
            object:活动表计算成功返回True，否则返回False
        """
        status = False
        # 表格读取成功后进行活动计算
        if self.read_table():
            try:
                for fac in self.active_factory:
                    act = fac.create_active()
                    act.calculate_active_data(self)
                    status = True
            except:
                print("活动计算出错")

        return status
