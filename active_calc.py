import pandas as pd
import numpy as np
import os
import warnings

warnings.filterwarnings('ignore')  # 去除警告信息


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
        output_path = active_context.table_paths['output']

        # 2018/09/14 <bug fixed>
        # 修改数据类型，保证类型正确。不然表格连接时可能漏掉部分数据
        df_dingdan['商品编号'] = df_dingdan['商品编号'].astype(str)
        df_dingdan['订单编号'] = df_dingdan['订单编号'].astype(str)
        df_manjian['编码'] = df_manjian['编码'].astype(str)
        df_dingdan['商品数量'] = df_dingdan['商品数量'].astype('float')
        df_manjian['数量'] = df_manjian['数量'].astype('float')

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

        # 删除活动订单表中套餐数量不为NaN的值
        df_activityorder = df_activityorder[np.isnan(df_activityorder['活动订单表'])]

        output_path = os.path.join(output_path, '满减活动表.xlsx')
        writer = pd.ExcelWriter(output_path)
        df_activityorder.to_excel(writer, u'活动订单表', index=False)
        df_salessum.to_excel(writer, u'总销量订单表', index=False)
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

        # 2018/09/14 <bug fixed>
        # 修改数据类型，保证类型正确。不然表格连接时可能漏掉部分数据
        # 下面是待连接的两列
        df_dingdan['商品编号'] = df_dingdan['商品编号'].astype(str)
        df_tejia['编码'] = df_tejia['编码'].astype(str)
        df_dingdan['商品价格'] = df_dingdan['商品价格'].astype('float')
        df_tejia['活动价'] = df_tejia['活动价'].astype('float')

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
        df_activityorder.to_excel(writer, u'活动订单表', index=False)
        writer.save()
        print("已成功生成特价活动表！")


# 阶梯满减活动
class JieTi(Active):
    """计算阶梯满减活动表

    Attributes:
    """

    def calc(self, ser, df, df_num):
        res = 0.0
        # 活动区间数
        level_nums = df_num[ser['商品编号'], ser['开始时间'], ser['结束时间']]
        # 区间阈值
        policy_list = df.loc[ser['商品编号'], ser['开始时间'], ser['结束时间']]

        # 满数量
        if ser['满减条件'] == '满数量':
            for i in range(level_nums):
                if ser['商品数量'] >= policy_list.iloc[i]['满数量/金额']:
                    res = (ser['商品数量'] // policy_list.iloc[i]['满数量/金额']) * policy_list.iloc[i]['减金额']
                    break
        # 满金额
        else:
            for i in range(level_nums):
                if ser['商品总额'] >= policy_list.iloc[i]['满数量/金额']:
                    res = (ser['商品总额'] // policy_list.iloc[i]['满数量/金额']) * policy_list.iloc[i]['减金额']
                    break
        return res

    def calculate_active_data(self, active_context):
        """

        Args:
            active_context: 活动上下文类，记录表格原文件路径和表格数据
        """
        df_dingdan = active_context.tables['dingdan']
        df_jietimanjian = active_context.tables['jietimanjian']
        output_path = active_context.table_paths['output']

        # 转换数据类型，保证类型正确
        df_dingdan['商品编号'] = df_dingdan['商品编号'].astype(str)
        df_dingdan['订单编号'] = df_dingdan['订单编号'].astype(str)
        df_dingdan['商品数量'] = df_dingdan['商品数量'].astype('float')
        df_dingdan['商品总额'] = df_dingdan['商品总额'].astype('float')
        df_dingdan['下单时间'] = pd.to_datetime(df_dingdan['下单时间'])
        df_jietimanjian['商品编号'] = df_jietimanjian['商品编号'].astype(str)
        df_jietimanjian['开始时间'] = pd.to_datetime(df_jietimanjian['开始时间'])
        df_jietimanjian['结束时间'] = pd.to_datetime(df_jietimanjian['结束时间'])
        df_jietimanjian['满数量/金额'] = df_jietimanjian['满数量/金额'].astype('float')
        df_jietimanjian['减金额'] = df_jietimanjian['减金额'].astype('float')

        # 提取订单表中满足状态的数据
        valid_status = ['订单审核中', '配送中', '已完成', '出库中', '已送达']
        df_dingdan = df_dingdan[df_dingdan['状态'].isin(valid_status)]

        # 1.根据模板表统计各商品阶梯数（分组计数）
        df_jietimanjian_num = df_jietimanjian.groupby(['商品编号', '开始时间', '结束时间']).size()

        # 2.模板表按商品分组排序（降序）
        df_jietimanjian = df_jietimanjian.groupby(['商品编号', '开始时间', '结束时间']).apply(
            lambda df: df.sort_values(by='满数量/金额', ascending=False))
        # 删除多余的索引
        df_jietimanjian = df_jietimanjian.reset_index(3).drop('level_3', axis=1)

        # 3.筛选目标商品
        df_tmp = df_jietimanjian.drop_duplicates(['商品编号', '开始时间', '结束时间'])
        df_dingdan_obj1 = pd.merge(df_dingdan, df_tmp, on='商品编号')

        # 4.依据时间范围筛选
        df_dingdan_obj2 = df_dingdan_obj1[(df_dingdan_obj1['下单时间'] >= df_dingdan_obj1['开始时间'])
                                          & (df_dingdan_obj1['下单时间'] <= df_dingdan_obj1['结束时间'])]

        # 5.计算
        df_dingdan_obj = df_dingdan_obj2.copy()
        df_dingdan_obj['费用'] = df_dingdan_obj.apply(self.calc,
                                                    df=df_jietimanjian,
                                                    df_num=df_jietimanjian_num,
                                                    axis=1)
        # 删除冗余列
        column = list(df_jietimanjian.columns)
        column.remove('商品编号')
        df_dingdan_obj = df_dingdan_obj.drop(column, axis=1)
        df_dingdan_obj = df_dingdan_obj[df_dingdan_obj['费用'] > 0]

        output_path = os.path.join(output_path, '阶梯满减活动表.xlsx')
        writer = pd.ExcelWriter(output_path)
        df_dingdan_obj2.to_excel(writer, u'总销量订单表', index=False)
        df_dingdan_obj.to_excel(writer, u'阶梯满减活动表', index=False)
        writer.save()
        print("已成功生成阶梯满减活动表！")


# 专区满减活动
class ZhuanQuManJian(Active):

    def calculate_active_data(self, active_context):
        """

        Args:
        active_context: 活动上下文类，记录表格原文件路径和表格数据

        """

        df_dingdan = active_context.tables['dingdan']
        df_zhuanqumanjian = active_context.tables['zhuanqumanjian']
        output_path = active_context.table_paths['output']
        manjian_threshold = int(active_context.main_action.manjian_threshold)
        manjian_cost = int(active_context.main_action.manjian_cost)

        # 类型转换，确保类型正确
        df_dingdan['商品编号'] = df_dingdan['商品编号'].astype(str)
        df_zhuanqumanjian['商品编号'] = df_zhuanqumanjian['商品编号'].astype(str)
        df_dingdan['下单时间'] = pd.to_datetime(df_dingdan['下单时间'])
        df_zhuanqumanjian['开始时间'] = pd.to_datetime(df_zhuanqumanjian['开始时间'])
        df_zhuanqumanjian['结束时间'] = pd.to_datetime(df_zhuanqumanjian['结束时间'])

        # 获取活动开始时间和活动结束时间
        active_time_start = df_zhuanqumanjian['开始时间'][0]
        active_time_end = df_zhuanqumanjian['结束时间'][0]

        # 提取活动表商品编号
        df_zhuanqumanjian = pd.DataFrame(df_zhuanqumanjian['商品编号'])

        # 提取订单表中满足状态的数据
        valid_status = ['订单审核中', '配送中', '已完成', '出库中', '已送达']
        df_dingdan = df_dingdan[df_dingdan['状态'].isin(valid_status)]

        # 筛选活动时间内的订单数据
        df_dingdan = df_dingdan[(df_dingdan['下单时间'] >= active_time_start) &
                                (df_dingdan['下单时间'] <= active_time_end)]

        # 选取包含活动商品的订单数据
        df_active = pd.merge(df_dingdan, df_zhuanqumanjian, on='商品编号')

        # 计算达到活动门槛的订单数据
        df_reach_threshold = df_active.groupby('订单编号').filter(lambda g: g['商品总额'].sum() >= manjian_threshold)

        # 计算活动时间内达到门槛订单数据的统计值
        order_counts, pharmacy_num_counts, order_money_amount, active_sales_volume, avtive_sales, active_cost = \
            self.calc_desc_data(df_reach_threshold, manjian_threshold, manjian_cost)

        summary_data_active = {'活动订单数': [order_counts], '活动下单用户数': [pharmacy_num_counts],
                               '活动订单总额': [order_money_amount], '活动销量': [active_sales_volume],
                               '活动销售额': [avtive_sales], '活动费用': [active_cost]}

        df_out1 = pd.DataFrame(summary_data_active)

        # 计算未设门槛数据数据统计值（活动中非门槛数据）
        order_counts, pharmacy_num_counts, order_money_amount, active_sales_volume, avtive_sales, active_cost = \
            self.calc_desc_data(df_active, manjian_threshold, manjian_cost)

        summary_data = {'订单数': [order_counts], '下单用户数': [pharmacy_num_counts],
                        '订单总额': [order_money_amount], '销量': [active_sales_volume],
                        '销售额': [avtive_sales]}

        df_out2 = pd.DataFrame(summary_data)

        # 合并两张统计表并输出
        df_out = pd.concat([df_out1, df_out2], axis=1)
        output_path = os.path.join(output_path, '打包满减活动表.xlsx')
        writer = pd.ExcelWriter(output_path)
        df_active.to_excel(writer, '总销量订单表', index=False)
        df_reach_threshold.to_excel(writer, '活动订单表', index=False)
        df_out.to_excel(writer, '专区满减活动订单表', index=False)
        writer.save()
        print("已成功生成专区满减活动表！")

    def calc_desc_data(self, df, manjian_threshold, manjian_cost):
        df_tmp = df.groupby('订单编号')['商品总额'].sum()

        # 活动费用
        active_cost = ((df_tmp / manjian_threshold) // 1 * manjian_cost).sum()

        # 活动订单数
        order_counts = df.drop_duplicates('订单编号')['订单编号'].count()

        # 活动下单用户数
        pharmacy_num_counts = df.drop_duplicates('药店编号')['药店编号'].count()

        # 活动订单总额
        order_money_amount = df['优惠金额'].sum() + df['总金额'].sum()

        # 活动销量
        active_sales_volume = df['商品数量'].sum()

        # 活动销售额
        avtive_sales = df['商品总额'].sum()

        return order_counts, pharmacy_num_counts, order_money_amount, active_sales_volume, avtive_sales, active_cost


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


# 阶梯满减活动工厂
class JietiManJianFactory(IActiveFactory):
    def create_active(self):
        """

        Returns:返回满减活动类

        """
        return JieTi()


# 特价活动工厂
class TeJiaFactory(IActiveFactory):
    def create_active(self):
        """

        Returns:返回特价活动类

        """
        return TeJia()


# 专区满减活动工厂
class ZhuanQuManJianFactory(IActiveFactory):
    def create_active(self):
        """

        Returns:返回专区满减活动类

        """
        return ZhuanQuManJian()


# 上下文类
class ActiveContext(object):
    def __init__(self, main_action):
        """

        Args:
            main_action (object):
        """
        self.active_factory = []
        self.main_action = main_action
        self.table_paths = self.main_action.table_paths
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
        if self.table_paths['zhuanqumanjian'] != "":
            self.active_factory.append(ZhuanQuManJianFactory())
        if self.table_paths['jietimanjian'] != "":
            self.active_factory.append(JietiManJianFactory())

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
            if self.table_paths['zhuanqumanjian'] != "":
                self.tables['zhuanqumanjian'] = pd.read_excel(self.table_paths['zhuanqumanjian'])
            if self.table_paths['jietimanjian'] != "":
                self.tables['jietimanjian'] = pd.read_excel(self.table_paths['jietimanjian'])
        except:
            print('读取活动表出错')
            return False
        else:
            print("活动表读取成功")

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
