# -*- coding: utf-8 -*-
import unittest
from time import sleep

import ddt

from framework.browser_engine import BrowserEngine
from pageobjects.catalog_page import DirectoryList
from pageobjects.attendance_period_management_page import *
from unit.excel import ExcelUtils
from unit.login import login
from unit.operation_fun import OperationMethod
from logs.logger import Logger
logger = Logger(logger="WFMSearch").getlog()


excel_utils = ExcelUtils("attendance_period_management_info.xlsx", "Sheet1")
xg = excel_utils.dict_data()
excel_utils = ExcelUtils("attendance_period_management_info.xlsx", "Sheet2")
gz = excel_utils.dict_data()


# 考勤期段管理
@ddt.ddt
class AttendancePeriodManagement(unittest.TestCase):
    def setUp(self):
        browser = BrowserEngine(self)
        self.driver = browser.open_browser(self)  # 读取浏览器类型
        driver = self.driver
        # 调用登录函数，默认username='peter',password='1234567'
        self.lg = login(driver)
        directory = DirectoryList(driver)
        # 考勤设置-考勤体系-新建考勤体系
        directory.three_level_select("考勤设置", '考勤体系', '考勤期段管理')
        # 选择考勤体系
        driver.find_element_by_xpath("//section/section/header/div/div/..//input").click()
        # 大陆门店考勤
        driver.find_element_by_xpath("//section/section/header/div/div/..//span[contains(text(),'香港门店考勤')]").click()

    # 修改
    @ddt.data(*xg)
    def test01_alter(self, data):
        """考勤期段管理修改"""
        name = data['用例描述']
        st_date = data['开始时间']
        en_date = data['结束时间']
        trigger_btn = data['触发按钮']
        handle = data['操作']
        remark = data['备注'].split('-')
        expect = data['预期结果']
        if data["skip"] == 'True':
            self.skipTest("跳过示例{0}".format(name))
        driver = self.driver
        attendance_period = AttendancePeriodManagementList(driver)
        alter = Alter(driver)
        XG = OperationMethod(driver)

        # 选中要操作的开始时间
        attendance_period.select_data(st_date, en_date)
        # 点击修改按钮
        attendance_period.operation_btn(trigger_btn)
        # 备注
        XG.input_(remark[0], remark[1])
        # 保存
        alter.save_btn(handle)
        sleep(0.2)
        text = attendance_period.unit_data(st_date)
        print(text)
        try:
            # 使用断言
            self.assertEqual(text, expect)
            attendance_period.capture_screen(name + '成功')
            print(name + '成功')
        except AssertionError as e:
            attendance_period.error_screen(name + '失败')
            print(name + '失败')
            raise e

        print("-------------------考勤期段管理test_xiugai_correct运行完毕-------------------")

    # 考勤过账
    @ddt.data(*gz)
    def test02_attendance_posting(self, data):
        """考勤期段管理-考勤过账"""
        driver = self.driver
        attendance_period = AttendancePeriodManagementList(driver)
        carry_to = CarryTo(driver)

        name = data['用例描述']
        st_date = data['开始时间']
        en_date = data['结束时间']
        trigger_btn = data['触发按钮']
        handle = data['操作']
        expect = data['预期结果']

        # 状态排序
        attendance_period.sort()

        # 点击考勤过账
        attendance_period.operation_btn(trigger_btn)

        # 点击提示框里的确认
        carry_to.save_btn(handle)
        sleep(0.2)
        # text = attendance_period.carry_to_status(st_date, en_date)
        text2 = driver.find_element_by_xpath("//table/tbody/tr[2]/td[4]/div").text

        # 断言
        try:
            # 断言
            self.assertNotIn(text2, expect)
            attendance_period.capture_screen(name + '成功')
            logger.info("Test Pass")
            print(name + '成功')

        except AssertionError as e:
            attendance_period.error_screen(name + '失败')
            logger.error("Test Fail:断言失败")
            print(name + '失败')
            raise e
        print("-------------------考勤期段管理test_attendance_posting运行完毕-------------------")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
