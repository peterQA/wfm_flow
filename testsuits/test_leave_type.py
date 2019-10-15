# -*- coding: utf-8 -*-
import unittest
from time import sleep



# 新增
import ddt

from framework.browser_engine import BrowserEngine
from pageobjects.catalog_page import DirectoryList
from pageobjects.leave_type_page import *
from unit.base_page import BasePage
from unit.excel import ExcelUtils
from unit.login import login
from unit.operation_fun import OperationMethod

excel_utils = ExcelUtils("leave_type_info.xlsx", "Sheet1")
xz = excel_utils.dict_data()
excel_utils = ExcelUtils("leave_type_info.xlsx", "Sheet2")
xg = excel_utils.dict_data()
excel_utils = ExcelUtils("leave_type_info.xlsx", "Sheet3")
sc = excel_utils.dict_data()


@ddt.ddt
class Leave(unittest.TestCase, BasePage):
    def setUp(self):
        browser = BrowserEngine(self)
        self.driver = browser.open_browser(self)  # 读取浏览器类型
        sleep(1)
        driver = self.driver
        directory = DirectoryList(driver)
        # 调用登录函数，默认username='peter',password='1234567'
        self.lg = login(driver)
        # 考勤设置-考勤列表-加班类型
        directory.three_level_select("考勤设置", "考勤列表", "休假类型")
        # 将滚动条拉到最底层
        js1 = "window.scrollTo(0,100)"
        driver.execute_script(js1)
        sleep(1)

    # 新增(正常)
    @ddt.data(*xz)
    def test01_create_correct(self, data):
        """休假类型新增"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        XZ = OperationMethod(driver)
        leave_type = LeaveTypeList(driver)
        add = Add(driver)
        name = data['用例描述']
        code = data['编码'].split('-')
        Chinese = data['中文描述'].split('-')
        trigger_btn = data['触发按钮']
        unit = data['单位'].split('-')
        handle = data['操作']
        use_vacation_types_first = data['优先使用休假类型'].split('-')
        expect = data['预期结果']

        # 新增按钮
        leave_type.operation_btn(trigger_btn)
        # 编码输入
        XZ.input_(code[0], code[1])
        # 中文描述
        XZ.input_(Chinese[0], Chinese[1])

        # 单位选取（天）
        XZ.input_select(unit[0], unit[1])
        # # 将滚动条拉到最底层
        # js1 = "window.scrollTo(0,1000)"
        # driver.execute_script(js1)
        self.scroll_page_to_buttom()
        # 优先使用休假类型(年假)
        XZ.input_select(use_vacation_types_first[0], use_vacation_types_first[1])
        sleep(1)
        # 保存
        add.save_btn(handle)
        sleep(1)
        texts = XZ.data_list()
        print(texts)
        try:
            # 使用断言
            self.assertIn(expect, texts)
            leave_type.capture_screen(name + '成功')
            print(name + '成功')

        except AssertionError as e:
            leave_type.error_screen(name + '失败')
            print(name + '失败')
            raise e
        print("-------------------休假类型test_xinzeng_correct运行完毕-------------------")

    # 修改（正常）
    @ddt.data(*xg)
    def test02_alter_correct(self, data):
        """休假类型修改"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        XG = OperationMethod(driver)
        leave_type = LeaveTypeList(driver)
        alter = Alter(driver)
        name = data['用例描述']
        code = data['编码'].split('-')
        trigger_btn = data['触发按钮']
        handle = data['操作']
        unit = data['单位'].split('-')
        expect = data['预期结果']
        # 筛选出所有编码元素
        elements = XG.data_list()
        for element in elements:
            if element == code[1]:
                leave_type.select_data(element)
                sleep(1)
                break
        # 点击修改按钮
        leave_type.operation_btn(trigger_btn)
        # 单位选取（小时）
        XG.input_select(unit[0], unit[1])
        # 保存
        alter.save_btn(handle)
        text = leave_type.unit_data(code[1])
        try:
            # 使用断言 判断上面添加的编码是否在编码元素列表中
            self.assertEqual(text, expect)
            leave_type.capture_screen(name + '成功')
            print(name + '成功')
        except AssertionError as e:
            leave_type.error_screen(name + '失败')
            print(name + '失败')
            raise e

        print("-------------------休假类型test_xiugai_correct运行完毕-------------------")

    @ddt.data(*sc)
    # 删除
    def test03_del_correct(self, data):
        """休假类型删除"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        leave_type = LeaveTypeList(driver)
        SC = OperationMethod(driver)
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
                leave_type.select_data(element)
                break
        # 点击删除按钮
        leave_type.operation_btn(trigger_btn)
        # 选择提示框里的确认按钮
        dele.save_btn(handle)
        # 编码列表
        elements1 = SC.data_list()
        try:
            # 断言
            self.assertNotIn(code[1], elements1)
            leave_type.capture_screen(name + '成功')
            print(name + '成功')

        except AssertionError as e:
            leave_type.error_screen(name + '失败')
            print(name + '失败')
            raise e
        print("-------------------休假类型test_del_correct运行完毕-------------------")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
