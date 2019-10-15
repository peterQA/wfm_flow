# -*- coding: utf-8 -*-
import unittest
from time import sleep

import ddt
from parameterized import parameterized
from selenium.webdriver.common.action_chains import ActionChains


# 新增
# from Test_data.test_data import test01_alter_correct_info
from framework.browser_engine import BrowserEngine
from pageobjects.catalog_page import *
from pageobjects.staff_policy_allocation_page import *
from unit.excel import ExcelUtils
from unit.login import login

excel_utils = ExcelUtils("staff_policy_allocation_info.xlsx", "result1")
test_alter_correct_info = excel_utils.dict_data()


@ddt.ddt
class StaffPolicyAllocation(unittest.TestCase):
    def setUp(self):
        self.module_name = '员工政策分配'
        browser = BrowserEngine(self)
        self.driver = browser.open_browser(self)  # 读取浏览器类型
        driver = self.driver
        directory = DirectoryList(driver)

        # 调用登录函数，默认username='peter',password='1234567'
        self.lg = login(driver)
        sleep(0.5)
        # print('当前页url是：',url)
        # 考勤处理-员工政策分配
        directory.two_level_select("考勤处理", '员工政策分配')

    def tearDown(self):
        self.driver.quit()

    # 修改（正常）
    @ddt.data(*test_alter_correct_info)
    def test_alter(self, data):
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        Listpage = StaffPolicyAllocationList(driver)
        Editpage = StaffPolicyAllocationEdit(driver)
        username = data['员工id']
        attendance = data['考勤体系'].split('-')
        leave = data['休假政策'].split('-')
        overtime = data['加班政策'].split('-')
        status = data['状态'].split('-')
        btn = data['操作']
        expect = data['预期结果']

        # 筛选出所有编码元素
        element_list = [i.text for i in Listpage.get_code_lists()]
        if username in element_list:
            for element in Listpage.get_code_lists():
                if element.text == username:
                    Listpage.operate_line(username)  # 选定要操作的行
                    break

            # 点击修改按钮
            Listpage.edit_btn()
            # 考勤体系选择
            Editpage.universal_selector(attendance[0], attendance[1])
            # 休假政策选择
            Editpage.universal_selector(leave[0], leave[1])
            # 加班政策选择
            Editpage.universal_selector(overtime[0], overtime[1])
            # 状态选择
            Editpage.universal_selector(status[0], status[1])
            # 确认
            Editpage.confirm_btn(btn)
            # 提取修改后的考勤体系状态
            text = Listpage.attendance_status2(username)
            # 断言
            try:
                self.assertEqual(text, expect)
                self.lg.capture_screen('员工政策分配修改成功')
                print('员工政策分配修改成功')
            except AssertionError as e:
                self.lg.error_screen('员工政策分配未修改')

                print('员工政策分配未修改')
                raise e
        else:
            print('没有要修改的数据')

        print("-------------------员工政策分配test01_alter_correct运行完毕-------------------")


if __name__ == "__main__":
    unittest.main()
    # # 构造测试集
    # suite = unittest.TestSuite()
    # print('添加前：', suite)
    # # suite.addTest(StaffPolicyAllocation("test01_create_correct"))
    # # suite.addTest(StaffPolicyAllocation("test02_create_coding_null"))
    # suite.addTest(StaffPolicyAllocation("test_alter"))
    # # suite.addTest(StaffPolicyAllocation("test04_del_correct"))
    # print('添加后：', suite)
    #
    # # 执行测试
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
