# !/usr/bin/python
# -*- coding:utf-8 -*-

""""""

from unit.base_page import BasePage
from enum import Enum, unique

"""
 页面类，主要存放页面简单的操作函数.
 页面类主要是将页面操作写成函数，以供测试类使用
 集成 BasePage 二次封装通用类
 通常 1个页面为一个类
"""


@unique
class Color(Enum):
    two_staff_policy_allocation_path = 1
    orange = 2
    yellow = 3
    green = 4
    blue = 5
    indigo = 6
    purple = 7


# 目录列表页
class DirectoryList(BasePage):
    # TODO:目录列表页
    # --------------------------------------------------------
    # 一级目录
    one_level = 'xpath=>//section/aside/div/ul/li/div/div[contains(text(),"{0}")]'
    # 二级目录(无三级目录)
    two_level = one_level + '/../../ul/div/div/div/li/div[contains(text(),"{1}")]'
    # 二级目录(有三级目录)
    two_level_three = one_level + '/../../ul/div/div/div/li/div/span/div[contains(text(),"{1}")]'
    # 三级目录
    three_level = 'xpath=>//div[contains(@class,"DropDownMenuItem")][contains(text(),"{0}")]'

    # --------------------------------------------------------

    # 选取一级目录
    def one_level_select(self, onelevel):
        self.click(self.one_level.format(onelevel))

    # 选取二级目录
    def two_select(self, onelevel, twolevel):
        self.click(self.two_level.format(onelevel, twolevel))

    # 选取一级目录下的二级目录
    def two_level_select(self, onelevel, twolevel):
        # self.click(self.one_time_tracking_path)
        self.one_level_select(onelevel)

        self.two_select(onelevel, twolevel)

    # 选取三级目录
    def three_level_select(self, onelevel, twolevel, threelevel):

        self.one_level_select(onelevel)
        # self.click(self.two_level_there % ('考勤处理', '休假加班查看'))
        self.move_to_element(self.two_level_three.format(onelevel, twolevel))
        self.click(self.three_level.format(threelevel))
