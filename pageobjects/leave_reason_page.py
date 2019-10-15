# !/usr/bin/python
# -*- coding:utf-8 -*-

from unit.base_page import BasePage

"""
 页面类，主要存放页面简单的操作函数.
 页面类主要是将页面操作写成函数，以供测试类使用
 集成 BasePage 二次封装通用类
 通常 1个页面为一个类
"""


# 休假类型列表页
class VacationTypeList(BasePage):
    # TODO：休假类型列表页
    # --------------------------------------------------------
    # 编码列表
    coding_list = '//section/main/div/div[3]/table/tbody/tr[*]/td[1]/div'
    # 新增按钮
    add_button = "xpath=>//footer/div/button[1]"
    # 修改按钮
    edit_button = "xpath=>//footer/div/button[2]"
    # 删除按钮
    delete_button = "xpath=>//footer/div/button[3]"

    # --------------------------------------------------------

    # 获取操作前的编码列表
    def coding_list1(self):
        driver = self.driver
        code_list1 = driver.find_elements_by_xpath(self.coding_list)
        return code_list1

    # 获取操作后的编码列表
    def coding_list2(self):
        driver = self.driver
        code_list2 = driver.find_elements_by_xpath(self.coding_list)
        return code_list2

    # 新增按钮点击
    def add_btn(self):
        self.click(self.add_button)  # 传递新增按钮 xpath

    # 修改按钮
    def edit_btn(self):
        self.click(self.edit_button)

    # 删除按钮
    def del_but(self):
        self.click(self.delete_button)


# 休假类型新增页
class VacationTypeAdd(BasePage):
    # TODO:休假类型新增页
    # --------------------------------------------------------
    # 编码输入框
    code_input_box = "css_selector=>input.el-input__inner"
    # 中文描述
    chinese_description = "xpath=>//form/div[2]/div/div/input"
    # 英文描述
    english_description = ""
    # 繁体描述
    traditional_chinese_description = ""
    # 单位选取触发框
    unit_selection_trigger = "xpath=>//form/div[6]/div/div/div/span/span/i"
    # 单位选取天
    unit_selection_day = 'xpath=>//*[@id="peter_Sign_date_child"]/*[text()="天"]'
    # 性别匹配触发
    gender_match_trigger = 'xpath=>//*[@id="peter_sign_gender"]/div/div/div/span/span/i'
    # 性别匹配男
    gender_match_man = "xpath=>//*[@id='peter_sign_gender']//*/span[text()='男']"
    # 保存
    save = 'xpath=>//div[3]/div/button[1]'

    # --------------------------------------------------------

    # 编码输入
    def coding_input(self, text):
        self.send_keys(self.code_input_box, text)  # 传递编码框 xpath 和 内容

    # 中文描述输入
    def chinese_description_input(self, text):
        self.send_keys(self.chinese_description, text)  # 传递中文描述框css_selector 和 内容

    # 单位选取触发框
    def unit_selection_trigger_input(self):
        self.click(self.unit_selection_trigger)  # 单位选取触发 xpath

    # 单位选取(天)
    def unit_selection_day_(self):
        self.click(self.unit_selection_day)  # 单位选取天 xpath

    # 性别匹配触发框
    def gender_match_trigger_input(self):
        self.click(self.gender_match_trigger)  # 性别匹配触发 xpath

    # 性别匹配(男)
    def gender_match_man_(self):
        self.click(self.gender_match_man)  # 性别匹配选取男 xpath

    # 保存按钮点击
    def save_btn(self):
        self.click(self.save)  # 保存按钮 xpath

    # --------------------------------------------------------

