# -*- coding: utf-8 -*-
import unittest
from time import sleep
import ddt
from framework.browser_engine import BrowserEngine
from pageobjects.catalog_page import DirectoryList
from pageobjects.leave_policy_page import *
from unit.excel import ExcelUtils
from unit.login import login
from unit.operation_fun import OperationMethod

excel_utils = ExcelUtils("leave_policy_info.xlsx", "Sheet1")
xz = excel_utils.dict_data()
excel_utils = ExcelUtils("leave_policy_info.xlsx", "Sheet2")
xg = excel_utils.dict_data()
excel_utils = ExcelUtils("leave_policy_info.xlsx", "Sheet3")
sc = excel_utils.dict_data()


@ddt.ddt
class LeavePolicy(unittest.TestCase):
    def setUp(self):
        browser = BrowserEngine(self)
        self.driver = browser.open_browser(self)  # 读取浏览器类型
        driver = self.driver
        # 调用登录函数，默认username='peter',password='1234567'
        self.lg = login(driver)
        directory = DirectoryList(driver)

        # 考勤设置-休假政策
        directory.two_level_select('考勤设置', '休假政策')

        # 将滚动条拉到最底层
        js1 = "window.scrollTo(0,100)"
        driver.execute_script(js1)

    # 新增(正常)
    @ddt.data(*xz)
    def test01_xinzeng_correct(self, data):
        """休假政策新增"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        XZ = OperationMethod(driver)
        leave_policy = LeavePolicyList(driver)
        add = Add(driver)

        name = data['用例描述']
        code = data['编码'].split('-')
        Chinese = data['中文描述'].split('-')
        trigger_btn = data['触发按钮']
        handle = data['操作']
        expect = data['预期结果']

        # 新增按钮
        leave_policy.operation_btn(trigger_btn)
        # 编码输入
        XZ.input_(code[0], code[1])
        # 中文描述
        XZ.input_(Chinese[0], Chinese[1])
        # 确认
        add.save_btn(handle)
        sleep(1)
        # 断言
        texts = XZ.data_list()

        try:
            # 使用断言
            self.assertIn(expect, texts)
            leave_policy.capture_screen(name + '成功')
            print(name + '成功')

        except AssertionError as e:
            leave_policy.error_screen(name + '失败')
            print(name + '失败')
            raise e
        print("-------------------休假政策test_xinzeng_correct运行完毕-------------------")

    # 修改（正常）
    @ddt.data(*xg)
    def test02_xiugai_correct(self, data):
        """休假政策修改"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        XG = OperationMethod(driver)
        leave_policy = LeavePolicyList(driver)
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
                leave_policy.select_data(element)
                sleep(0.2)
                break

        # 点击修改按钮
        leave_policy.operation_btn(trigger_btn)
        # 中文描述
        XG.input_(Chinese[0], Chinese[1])
        # 繁体描述
        XG.input_(Chinese_traditional[0], Chinese_traditional[1])
        # 确认
        alter.save_btn(handle)
        text = leave_policy.unit_data(code[1])
        try:
            # 使用断言 判断上面添加的编码是否在编码元素列表中
            self.assertEqual(text, expect)
            leave_policy.capture_screen(name + '成功')
            print(name + '成功')
        except AssertionError as e:
            leave_policy.error_screen(name + '失败')
            print(name + '失败')
            raise e
        print("-------------------休假政策test_xiugai_correct运行完毕-------------------")

    # 删除
    @ddt.data(*sc)
    def test03_del_correct(self, data):
        """休假政策删除"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        SC = OperationMethod(driver)
        leave_policy = LeavePolicyList(driver)
        alter = Alter(driver)
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
                leave_policy.select_data(element)
                break

        # 点击修改按钮
        leave_policy.operation_btn('修改')
        # 点击删除按钮
        alter.save_btn(trigger_btn)
        # 选择提示框里的确定按钮
        dele.save_btn(handle)
        # 编码列表
        elements1 = SC.data_list()
        try:
            # 断言
            self.assertNotIn(code[1], elements1)
            leave_policy.capture_screen(name + '成功')
            print(name + '成功')

        except AssertionError as e:
            leave_policy.error_screen(name + '失败')
            print(name + '失败')
            raise e
        print("-------------------休假政策test_del_correct运行完毕-------------------")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    # 构造测试集
    suite = unittest.TestSuite()
    print('添加前：', suite)
    suite.addTest(LeavePolicy("test_xinzeng_correct"))
    suite.addTest(LeavePolicy("test_xinzeng_coding_null"))
    suite.addTest(LeavePolicy("test_xiugai_correct"))
    suite.addTest(LeavePolicy("test_del_correct"))
    print('添加后：', suite)

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
