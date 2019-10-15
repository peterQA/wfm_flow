# -*- coding: utf-8 -*-
import unittest
from time import sleep

import ddt

from framework.browser_engine import BrowserEngine
from pageobjects.catalog_page import DirectoryList
from pageobjects.examine_custom_page import *
from unit.excel import ExcelUtils
from unit.login import login

from unit.operation_fun import OperationMethod

excel_utils = ExcelUtils("examine_custom_info.xlsx", "Sheet1")
xz = excel_utils.dict_data()
excel_utils = ExcelUtils("examine_custom_info.xlsx", "Sheet2")
xg = excel_utils.dict_data()
excel_utils = ExcelUtils("examine_custom_info.xlsx", "Sheet3")
sc = excel_utils.dict_data()


# 审查自定义项
@ddt.ddt
class ExamineCustom(unittest.TestCase):
    def setUp(self):
        browser = BrowserEngine(self)
        self.driver = browser.open_browser(self)  # 读取浏览器类型
        sleep(1)
        driver = self.driver
        directory = DirectoryList(driver)
        # 调用登录函数，默认username='peter',password='1234567'
        self.lg = login(driver)
        # 考勤设置-考勤列表-加班类型
        directory.two_level_select('考勤设置', '审查自定义项')
        # 将滚动条拉到最底层
        js1 = "window.scrollTo(0,100)"
        driver.execute_script(js1)
        sleep(1)

    # 新增(正常)
    @ddt.data(*xz)
    def test01_create_correct(self, data):
        """审查自定义新增"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        examine_custom = ExamineCustomList(driver)
        XZ = OperationMethod(driver)
        add = Add(driver)
        name = data['用例描述']
        code = data['编码'].split('-')
        Chinese = data['中文描述'].split('-')
        field = data['字段类型'].split('-')
        monad = data['单位'].split('-')
        trigger_btn = data['触发按钮']
        handle = data['操作']
        expect = data['预期结果']

        # 新增按钮
        examine_custom.operation_btn(trigger_btn)
        # 编码输入
        XZ.input_(code[0], code[1])
        # 字段类型
        XZ.input_select(field[0], field[1])
        # 单位（次）
        XZ.input_select(monad[0], monad[1])
        # 保存
        add.save_btn(handle)
        sleep(0.5)
        texts = XZ.data_list()

        print(texts)

        # 断言
        try:
            # 使用断言
            self.assertIn(expect, texts)
            examine_custom.capture_screen(name + '成功')
            print(name + '成功')

        except AssertionError as e:
            examine_custom.error_screen(name + '失败')
            print(name + '失败')

            raise e

        print("-------------------审查自定义项test_xinzeng_correct运行完毕-------------------")

    # 修改（正常）
    @ddt.data(*xg)
    def test02_alter_correct(self, data):
        """审查自定义项修改"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        XG = OperationMethod(driver)
        examine_custom = ExamineCustomList(driver)
        alter = Alter(driver)

        name = data['用例描述']
        code = data['编码'].split('-')
        trigger_btn = data['触发按钮']
        Chinese = data['中文描述'].split('-')
        handle = data['操作']
        expect = data['预期结果']

        # 筛选出所有编码元素
        elements = XG.data_list()
        for element in elements:
            if element == code[1]:
                examine_custom.select_data(element)
                break
        # 点击修改按钮
        examine_custom.operation_btn(trigger_btn)
        # 中文描述
        XG.input_(Chinese[0], Chinese[1])
        # 保存
        alter.save_btn(handle)
        # 获取描述信息
        text = examine_custom.unit_data(code[1])
        try:
            # 使用断言
            self.assertEqual(text, expect)
            examine_custom.capture_screen(name + '成功')
            print(name + '成功')
        except AssertionError as e:
            examine_custom.error_screen(name + '失败')
            print(name + '失败')
            raise e
        print("-------------------审查自定义项test_xiugai_correct运行完毕-------------------")

    # 删除
    @ddt.data(*sc)
    def test03_del_correct(self, data):
        """审查自定义项删除"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        examine_custom = ExamineCustomList(driver)
        XG = OperationMethod(driver)
        alter = Alter(driver)
        dele = Del(driver)
        name = data['用例描述']
        code = data['编码'].split('-')
        trigger_btn = data['触发按钮']
        handle = data['操作']
        # 筛选出所有编码元素
        elements = XG.data_list()
        print(elements)
        for element in elements:
            if element == code[1]:
                # 选中要操作的元素
                examine_custom.select_data(element)
                break
        # 点击修改按钮
        examine_custom.operation_btn(trigger_btn)
        # 点击删除按钮
        alter.del_btn()
        # 选择提示框里的确定按钮
        dele.operation_btn(handle)
        sleep(0.5)
        # 编码列表
        elements1 = XG.data_list()
        try:
            # 断言
            self.assertNotIn(code[1], elements1)
            examine_custom.capture_screen(name + '成功')
            print(name + '成功')

        except AssertionError as e:
            examine_custom.error_screen(name + '失败')
            print(name + '失败')
            raise e
        print("-------------------审查自定义项test_del_correct运行完毕-------------------")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
