# !/usr/bin/python
# -*- coding:utf-8 -*-

""""""
from time import sleep

from selenium.webdriver import ActionChains

from unit.base_page import BasePage

"""
 页面类，主要存放页面的元素定位和简单的操作函数.
 页面类主要是元素定位和页面操作写成函数，以供测试类使用
 集成 BasePage 二次封装通用类
 通常 1个页面为一个类
"""


# 排班管理列表页
class ScheduleManagementList(BasePage):
    # TODO:排班管理列表页
    # --------------------------------------------------------
    # 选择考勤地点触发框
    attendance_path = "xpath=>//section/header/div[1]/div[3]/div/div/input"
    # 港汇广场店
    grand_gateway = attendance_path + "/../../div[*]//span[text()= '%s']" % '港汇广场店'
    # 通用选择按钮路径
    universal_selection_button = "xpath=>//header/div/div/div/button/span[contains(text(),'{0}')]"
    # 要操作的用户(WFM005)
    code_path = "xpath=>//tbody/tr/td/div/span/div/div[1][contains(text(),'{0}')]"
    # 分组状态
    group_state = code_path + "/../../../../..//span/div/span"
    # 开始位置
    start = code_path + "/../../../../..//td[3]"
    # 清除班次开始行
    clear_start = "xpath=>//main/div/div[3]/table/tbody/tr[1]/td[1]/div/span/div[2]/div[1]"
    # 清除班次结束行
    clear_stop = "xpath=>//main/div/div[3]/table/tbody/tr[7]/td[1]/div/span/div[2]/div[1]"
    # 结束位置
    stop = code_path + "/../../../../..//td[5]"
    # 班次状态
    shift_state = code_path + "/../../../../../td[3]/div//div/div[1]"

    # 应用到其他日期后的班次状态
    use_shift_state = "xpath=>//section/section/main/div/div[3]/table/tbody/tr[5]/td[7]/div//div/div[1]"

    # --------------------------------------------------------

    # 选择考勤地点触发
    def attendance_path_input(self):
        self.click(self.attendance_path)
        sleep(1)
        self.click(self.grand_gateway)

    # 选定要操作的用户
    def operate_line(self, code='WFM005'):
        sleep(1)
        self.click(self.code_path.format(code))

    # 选择分组前的分组状态
    def group_status1(self, code='WFM005'):
        text = self.status_text1(self.group_state.format(code))
        return text

    # 选择分组后的分组状态
    def group_status2(self, code='WFM006'):
        text = self.status_text2(self.group_state.format(code))
        return text

    # 选择要操作的数据
    def operate_line1(self, code='WFM006'):
        self.drag_and_drop(self.start.format(code), self.stop.format(code))

    # 选择班次前的班次状态
    def shift_status1(self, code='WFM006'):
        text = self.status_text1(self.shift_state.format(code))
        return text

    # 选择班次后的班次状态
    def shift_status2(self, code='WFM006'):
        text = self.status_text2(self.shift_state.format(code))
        return text

    # 应用到其他日期后的班次状态
    def use_shift_status2(self):
        text = self.status_text2(self.use_shift_state)
        return text

    # 选择分组按钮
    def select_group_btn(self, btn):
        self.click(self.universal_selection_button.format(btn))

    # 选择班次按钮
    def select_shift_btn(self, btn):
        self.click(self.universal_selection_button.format(btn))

    # 复制给其他人按钮
    def copy_other_btn(self, btn):
        self.click(self.universal_selection_button.format(btn))

    # 应用到其他日期按钮
    def apply_date_btn(self, btn):
        self.click(self.universal_selection_button.format(btn))

    # 清除班次按钮
    def clear_shift_btn(self, btn):
        self.click(self.universal_selection_button.format(btn))

    # 复制后的员工班次状态（本人）
    def oneself(self, code='WFM005'):
        text = self.status_text1(self.shift_state.format(code))
        return text

    # 复制后的员工班次状态（其他人）
    def oneother(self, code='WFM001'):
        text = self.status_text2(self.shift_state.format(code))
        return text

    # 清除班次前的班次状态
    def clear_shift_state1(self, code='WFM005'):
        text = self.status_text1(self.shift_state.format(code))
        return text

    # 清除班次前后的班次状态
    def clear_shift_state2(self, code='WFM005'):
        text = self.status_text2(self.shift_state.format(code))
        return text

    # 要清除的行
    def clear_line(self):
        self.drag_and_drop(self.clear_start, self.clear_stop)


# 复制给其他人
class CopyTheOther(BasePage):
    # TODO:排班管理-复制给其他人页
    # --------------------------------------------------------

    # 分组2
    others = "xpath=>//table/tbody/tr[*]/td[3]/div[text()='%s']/../../td[1]/div/label/span/span"
    # 确认按钮
    confirm_button = "xpath=>//div[3]/div/button[1]"

    # --------------------------------------------------------

    # 其他员工选择框
    def other_checkbox(self, code='WFM001'):
        sleep(1)
        self.click(self.others % code)

    # 确认按钮
    def confirm_btn(self):
        self.click(self.confirm_button)

    # ----------测试代码----
    # 确认按钮
    confirm_button1 = "xpath=>//div[3]/div/button[1]/span"

    # 确认按钮
    def confirm_btn1(self):
        self.click(self.confirm_button1)


# 选择分组页
class ChooseGroup(BasePage):
    # TODO:排班管理-选择分组页
    # --------------------------------------------------------

    # 分组2
    group = "xpath=>//form/div/div/div[*]/div/div[3]/div[text()='%s']/../../div[1]/label/span[1]/span"
    # 确认按钮
    confirm_button = "xpath=>//div[3]/div/div[3]/div/button[1]"

    # --------------------------------------------------------

    # 分组选择框
    def group_checkbox(self, gr='小组2'):
        sleep(0.5)
        self.click(self.group % gr)

    # 确认按钮
    def confirm_btn(self):
        self.click(self.confirm_button)


# 选择班次页
class ChangeShift(BasePage):
    # TODO:排班管理-选择班次页
    # ----------------------------------------------------------------------

    # 班次
    shift = "xpath=>//form/div/div/div[*]/div/div[3]/div[text()='%s']/../../div[1]/label/span[1]/span"
    # 确认按钮
    conf_button = "xpath=>//div[1]/div/div[3]/div/button[1]"
    # ----------------------------------------------------------------------

    # 班次选择框
    def shift_checkbox(self, shift_data='早'):
        self.click(self.shift % shift_data)

    # 确认按钮
    def confirm_btn(self):
        self.click(self.conf_button)


# 应用到其他日期
class ApplyDate(BasePage):
    # TODO:排班管理-应用到其他日期页
    # ----------------------------------------------------------------------

    # 开始日期
    start_date = "xpath=>//form/div/div[1]/div/div/div/div/input"
    # 退出输入触发(不唯一，达成目的即可)
    x = "xpath=>//form/div/div[2]"
    # 确认按钮
    conf_button = "xpath=>//section/div/div/div/div[2]/div/div[3]/div/button[1]"

    # ----------------------------------------------------------------------

    # 开始日期输入
    def start_date_input(self, date='2019-05-21'):
        self.send_keys(self.start_date, date)

    # 退出输入触发(不唯一，达成目的即可)
    def input_quit(self):
        self.click(self.x)

    # 确认按钮
    def conf_btn(self):
        self.click(self.conf_button)



