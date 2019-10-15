# !/usr/bin/python
# -*- coding:utf-8 -*-

from time import sleep
import unittest

from parameterized import parameterized
from selenium.webdriver import ActionChains
from selenium.webdriver.android import webdriver

from Test_data.test_data import *
from framework.browser_engine import BrowserEngine
from pageobjects.catalog_page import DirectoryList
from pageobjects.leave_reason_page import VacationTypeList, VacationTypeAdd
from logs.logger import Logger

# 实现类
from unit.login import login

logger = Logger(logger="WFMSearch").getlog()


class LeaveType(unittest.TestCase):
    def setUp(self):
        browser = BrowserEngine(self)
        self.driver = browser.open_browser(self)  # 读取浏览器类型

        driver = self.driver
        directory = DirectoryList(driver)

        # login.login(self, 'peter', 1234567)
        # 调用登录函数，默认username='peter',password='1234567'
        login(driver)
        sleep(1)

        # sleep(1)
        directory.three_level_select('考勤设置', '考勤列表', '休假类型')

        # 将滚动条拉到最底层
        js1 = "window.scrollTo(0,100)"
        driver.execute_script(js1)
        sleep(1)

    def tearDown(self):
        self.driver.quit()

    # 新增(正常)
    def test01_create_correct(self):
        """休假类型新增"""
        driver = self.driver
        listpage = VacationTypeList(driver)
        newpage = VacationTypeAdd(driver)
        try:
            # 获取新增前的编码元素列表
            coding_list1 = listpage.coding_list1()
            # print(coding_list1)
            listpage.add_btn()  # 点击新增按钮

            newpage.coding_input("peter_aoto_test")  # 调用方法，向编码框输入内容
            newpage.chinese_description_input('peter的测试数据')  # 调用方法，点击页面按钮
            newpage.unit_selection_trigger_input()     # 单位选择触发
            sleep(1)
            newpage.unit_selection_day_()   # 单位选取(天)
            newpage.gender_match_trigger_input()  # 性别匹配触发
            sleep(1)
            newpage.gender_match_man_()  # 性别匹配(男)
            newpage.save_btn()  # 点击保存按钮
            sleep(1)
            # 获取新增后的编码元素列表
            coding_list2 = listpage.coding_list2()
            # print(coding_list2)

            # 断言
            try:
                # 使用断言，判断新增后的编码列表是不是和新增前不一样
                self.assertNotEqual(coding_list2, coding_list1)
                logger.info('休假类型新增成功')
                logger.info("Test Pass")
                print('休假类型新增成功')
                # 截图
                newpage.capture_screen('休假类型新增成功')
            except AssertionError as e:
                logger.error("休假类型新增失败")
                logger.error("Test Fail:断言失败")
                print('休假类型新增失败')
                raise e
        except Exception as e:
            logger.error("Test Fail:%s" % e)
            # 截图
            newpage.error_screen('休假类型新增失败')
            raise e


if __name__ == '__main__':
    unittest.main()
