# !/usr/bin/python
# -*- coding:utf-8 -*-

""""""
from time import sleep

from unit.base_page import BasePage

"""
 页面类，主要存放页面的元素定位和简单的操作函数.
 页面类主要是元素定位和页面操作写成函数，以供测试类使用
 集成 BasePage 二次封装通用类
 通常 1个页面为一个类
"""


# 员工政策分配列表页
class StaffPolicyAllocationList(BasePage):

    # TODO:员工政策分配列表页
    # --------------------------------------------------------
    # 用户编码列表
    code_list = "//section/main/div/div[3]/table/tbody/tr[*]/td[3]/div"
    # 拼接指定用户编码
    user_code = code_list + "[text()='%s']"
    # 指定用户的考勤体系状态
    attendance_system_status = user_code + "/../../td[6]"

    # 修改按钮
    edit_button = "xpath=>//section/footer/div/div[1]/div/button[1]"
    # 删除按钮
    delete_button = "xpath=>//section/footer/div/div[1]/div/button[2]"
    # --------------------------------------------------------

    # 获取用户编码列表
    def get_code_lists(self):
        driver = self.driver
        code_lists = driver.find_elements_by_xpath(self.code_list)
        return code_lists

    # 获取操作前的考勤体系状态
    def attendance_status1(self, code):
        driver = self.driver
        status1 = driver.find_element_by_xpath(self.attendance_system_status % code)
        return status1.text

    # 获取操作后的考勤体系状态
    def attendance_status2(self, code):
        driver = self.driver
        status2 = driver.find_element_by_xpath(self.attendance_system_status % code)
        return status2.text

    # 选定要操作的行
    def operate_line(self, code):
        self.click("xpath=>" + self.user_code % code)

    # 修改按钮
    def edit_btn(self):
        self.click(self.edit_button)

    # 删除按钮
    def del_btn(self):
        self.click(self.delete_button)


# 员工政策分配修改页
class StaffPolicyAllocationEdit(BasePage):

    # TODO:员工政策分配修改页
    # ----------------------------------------------------------------------
    # 通用触发
    Global_input = "xpath=>//form/div/div/div/div/label[contains(text(),'{0}')]/following-sibling::div[1]//div/input"
    # Global_input = "xpath=>//form/div/div[%d]/div/div/div/div/div[1]/input"
    # 通用选择
    Global_select = "xpath=>//form/div/div/div/div/label[contains(text(),'{0}')]" \
                    "/following-sibling::div[1]//span[text()='{1}']"

    # # 确认按钮
    confirm_button = "xpath=>//section/section/div/div/div/div/div[3]/div/button/span[contains(text(),'{0}')]"
    # ------------------------------------------------------------------------

    # 通用选择器
    def universal_selector(self, inputs, select):

        self.click(self.Global_input.format(inputs))
        sleep(1)
        self.click(self.Global_select.format(inputs, select))

    # 确认or取消
    def confirm_btn(self, btn):
        button = self.confirm_button.format(btn)
        self.click(button)
        sleep(2)
