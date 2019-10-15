# -*- coding: utf-8 -*-
import unittest
from time import sleep

import ddt

from framework.browser_engine import BrowserEngine
from pageobjects.catalog_page import DirectoryList
from pageobjects.shift_type_page import ShiftTypeList, Add, Alter, Del
from unit.excel import ExcelUtils
from unit.login import login
from unit.operation_fun import OperationMethod

excel_utils = ExcelUtils("shift_type_info.xlsx", "Sheet1")
xz = excel_utils.dict_data()
excel_utils = ExcelUtils("shift_type_info.xlsx", "Sheet2")
xg = excel_utils.dict_data()
excel_utils = ExcelUtils("shift_type_info.xlsx", "Sheet3")
sc = excel_utils.dict_data()


# 轮班类型
@ddt.ddt
class Shift(unittest.TestCase):
    def setUp(self):
        browser = BrowserEngine(self)
        self.driver = browser.open_browser(self)  # 读取浏览器类型
        sleep(1)
        driver = self.driver
        directory = DirectoryList(driver)
        # 调用登录函数，默认username='peter',password='1234567'
        self.lg = login(driver)
        # 考勤设置-考勤列表-加班类型
        directory.three_level_select("考勤设置", "考勤列表", "轮班类型")
        # 将滚动条拉到最底层
        js1 = "window.scrollTo(0,100)"
        driver.execute_script(js1)
        sleep(1)

    # 新增(正常)
    @ddt.data(*xz)
    def test01_create_correct(self,data):
        """轮班类型的新增"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        XZ = OperationMethod(driver)
        shift_type = ShiftTypeList(driver)
        add = Add(driver)
        name = data['用例描述']
        code = data['编码'].split('-')
        Chinese = data['中文描述'].split('-')
        trigger_btn = data['触发按钮']
        handle = data['操作']
        expect = data['预期结果']
        # 新增按钮
        shift_type.operation_btn(trigger_btn)
        # 编码输入
        XZ.input_(code[0], code[1])
        # 中文描述
        XZ.input_(Chinese[0], Chinese[1])
        # 保存
        add.save_btn(handle)
        texts = XZ.data_list()
        print(texts)
        # 断言
        try:
            # 使用断言
            self.assertIn(expect, texts)
            shift_type.capture_screen(name + '成功')
            print(name + '成功')

        except AssertionError as e:
            shift_type.error_screen(name + '失败')
            print(name + '失败')
            raise e
        print('---------------------轮班类型test_xinzeng_correct运行完毕---------------------')

    # 修改（正常）
    @ddt.data(*xg)
    def test02_alter_correct(self, data):
        """轮班类型的修改"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        XG = OperationMethod(driver)
        shift_type = ShiftTypeList(driver)
        alter = Alter(driver)
        name = data['用例描述']
        code = data['编码'].split('-')
        trigger_btn = data['触发按钮']
        Chinese = data['中文描述'].split('-')
        zh_hk = data['繁体描述'].split('-')
        handle = data['操作']
        expect = data['预期结果']

        # 筛选出所有编码元素
        elements = XG.data_list()
        for element in elements:
            if element == code[1]:
                shift_type.select_data(element)
                sleep(1)
                break

        # 点击修改按钮
        # driver.find_element_by_xpath('//footer/div/button[2]').click()
        shift_type.operation_btn(trigger_btn)
        # 中文描述
        XG.input_(Chinese[0], Chinese[1])

        # 繁体描述
        XG.input_(zh_hk[0], zh_hk[1])
        # 保存
        alter.save_btn(handle)
        # 获取描述信息
        text = shift_type.unit_data(code[1])
        try:
            # 使用断言
            self.assertEqual(text, expect)
            shift_type.capture_screen(name + '成功')
            print(name + '成功')
        except AssertionError as e:
            shift_type.error_screen(name + '失败')
            print(name + '失败')
            raise e

        print('---------------------轮班类型test_xiugai_correct运行完毕---------------------')

    # 删除
    @ddt.data(*sc)
    def test03_del_correct(self, data):
        """轮班类型的删除"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        shift_type = ShiftTypeList(driver)
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
                shift_type.select_data(element)
                break

        # 点击删除按钮
        shift_type.operation_btn(trigger_btn)
        # 选择提示框里的确认按钮
        dele.save_btn(handle)
        # 编码列表
        elements1 = SC.data_list()

        try:
            # 断言
            self.assertNotIn(code[1], elements1)
            shift_type.capture_screen(name + '成功')
            print(name + '成功')

        except AssertionError as e:
            shift_type.error_screen(name + '失败')
            print(name + '失败')
            raise e
        print('---------------------轮班类型test_del_correct运行完毕---------------------')

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()

