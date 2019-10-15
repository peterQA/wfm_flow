# -*- coding: utf-8 -*-
import unittest
from time import sleep

import ddt
from framework.browser_engine import BrowserEngine
from pageobjects.catalog_page import DirectoryList
from pageobjects.user_group_management_page import *
from unit.excel import ExcelUtils
from unit.login import login
from unit.operation_fun import OperationMethod

excel_utils = ExcelUtils("user_group_management_info.xlsx", "Sheet1")
xz = excel_utils.dict_data()
excel_utils = ExcelUtils("user_group_management_info.xlsx", "Sheet2")
xg = excel_utils.dict_data()
excel_utils = ExcelUtils("user_group_management_info.xlsx", "Sheet3")
sc = excel_utils.dict_data()


# 新建考勤体系
@ddt.ddt
class NewClockingInSystem(unittest.TestCase):
    def setUp(self):
        browser = BrowserEngine(self)
        self.driver = browser.open_browser(self)  # 读取浏览器类型
        driver = self.driver
        # 调用登录函数，默认username='peter',password='1234567'
        self.lg = login(driver)
        directory = DirectoryList(driver)

        # 系统管理-权限管理-用户组管理
        directory.three_level_select("系统管理", '权限管理', '用户组管理')

    def tearDown(self):
        self.driver.quit()

    # 新增(正常)
    @ddt.data(*xz)
    def test01_create(self, data):
        """用户组管理新增"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        XZ = OperationMethod(driver)
        new_clocking_in = UserGroupManagementList(driver)
        add = Add(driver)

        name = data['用例描述']
        code = data['编码'].split('-')
        Chinese = data['中文描述'].split('-')
        district = data['地区选择'].split('-')
        start_date = data['考勤年度开始日期'].split('-')
        take_effect_date = data['考勤体系生效日期'].split('-')

        trigger_btn = data['触发按钮']
        handle = data['操作']
        expect = data['预期结果']
        # 新增按钮
        new_clocking_in.operation_btn('')
        driver.find_element_by_xpath("/html/body/ul/li[contains(text(),'{0}')]".format('超级管理员')).click()

        # 编码输入
        XZ.input_(code[0], code[1])

        # 中文描述
        XZ.input_(Chinese[0], Chinese[1])

        # 将滚动条拉到最底层
        js1 = "window.scrollTo(0,100)"
        driver.execute_script(js1)
        #
        # # 考勤年度开始日期
        # XZ.input_(start_date[0], start_date[1])
        # # 考勤体系生效日期
        # XZ.input_(take_effect_date[0], take_effect_date[1])
        # 保存
        add.save_btn(handle)
        sleep(0.5)

        # 断言
        texts = XZ.data_list()
        try:
            # 使用断言
            self.assertIn(expect, texts)
            new_clocking_in.capture_screen(name + '成功')
            print(name + '成功')

        except AssertionError as e:
            new_clocking_in.error_screen(name + '失败')
            print(name + '失败')
            raise e
        print("-------------------用户组管理test_create运行完毕-------------------")

    # 修改（正常）
    @ddt.data(*xg)
    def test02_alter_correct(self, data):
        """考勤体系修改"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        XG = OperationMethod(driver)
        new_clocking_in = UserGroupManagementList(driver)
        alter = Alter(driver)

        name = data['用例描述']
        code = data['编码'].split('-')
        trigger_btn = data['触发按钮']
        handle = data['操作']
        Chinese = data['中文描述'].split('-')
        Chinese_traditional = data['繁体描述'].split('-')
        expect = data['预期结果']
        # 筛选出所有编码元素
        elements = XG.data_list()
        for element in elements:
            if element == code[1]:
                new_clocking_in.select_data(element)
                sleep(0.2)
                break

        # 点击修改按钮
        new_clocking_in.operation_btn(trigger_btn)
        sleep(1)
        # 中文描述
        XG.input_(Chinese[0], Chinese[1])
        # 繁体描述
        XG.input_(Chinese_traditional[0], Chinese_traditional[1])
        # 保存
        alter.save_btn(handle)
        sleep(1)
        text = new_clocking_in.unit_data(code[1])
        try:
            # 使用断言 判断上面添加的编码是否在编码元素列表中
            self.assertEqual(text, expect)
            new_clocking_in.capture_screen(name + '成功')
            print(name + '成功')
        except AssertionError as e:
            new_clocking_in.error_screen(name + '失败')
            print(name + '失败')
            raise e
        print("-------------------用户组管理test02_alter_correct运行完毕-------------------")

    # 删除
    @ddt.data(*sc)
    def test03_del_correct(self, data):
        """考勤体系删除"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        SC = OperationMethod(driver)
        new_clocking_in = UserGroupManagementList(driver)
        dele = Del(driver)

        name = data['用例描述']
        code = data['编码'].split('-')
        trigger_btn = data['触发按钮']
        handle = data['操作']
        # 筛选出所有编码元素
        elements = SC.data_list()
        print(elements)
        for element in elements:
            if element == code[1]:
                # 选中要操作的元素
                new_clocking_in.select_data(element)
                break

        # 点击删除按钮
        new_clocking_in.operation_btn(trigger_btn)
        # 选择提示框里的确定按钮
        dele.save_btn(handle)
        # 编码列表
        elements1 = SC.data_list()
        try:
            # 断言
            self.assertNotIn(code[1], elements1)
            new_clocking_in.capture_screen(name + '成功')
            print(name + '成功')

        except AssertionError as e:
            new_clocking_in.error_screen(name + '失败')
            print(name + '失败')
            raise e

        print("-------------------用户组管理test03_del_correct运行完毕-------------------")


if __name__ == "__main__":
    unittest.main()



