# -*- coding: utf-8 -*-
import unittest
from time import sleep

import ddt

from framework.browser_engine import BrowserEngine
from pageobjects.attendance_site_page import *
from pageobjects.catalog_page import DirectoryList
from unit.excel import ExcelUtils
from unit.login import login
from unit.operation_fun import OperationMethod

excel_utils = ExcelUtils("attendance_site_info.xlsx", "Sheet1")
sz = excel_utils.dict_data()
excel_utils = ExcelUtils("attendance_site_info.xlsx", "Sheet2")
qx = excel_utils.dict_data()


# 考勤地点
@ddt.ddt
class AttendanceSite(unittest.TestCase):
    def setUp(self):
        browser = BrowserEngine(self)
        self.driver = browser.open_browser(self)  # 读取浏览器类型
        driver = self.driver
        # 调用登录函数，默认username='peter',password='1234567'
        self.lg = login(driver)
        directory = DirectoryList(driver)

        # 考勤设置-考勤地点
        directory.two_level_select('考勤设置', '考勤地点')
        # 点击白金软件
        driver.find_element_by_xpath(
            '//section/main/div/div/div/div//span/span[contains(text(),"白金软件")]').click()
        sleep(0.2)
        # 零售公司
        driver.find_element_by_xpath(
            '//section/main/div/div/div/div//span/span[contains(text(),"零售公司")]').click()
        sleep(0.2)
        # 中国
        driver.find_element_by_xpath('//section/main/div/div/div/div//span/span[contains(text(),"中国")]').click()
        sleep(0.2)
        # 上海
        driver.find_element_by_xpath('//section/main/div/div/div/div//span/span[contains(text(),"上海")]').click()
        sleep(0.2)

        # 将滚动条拉到最底层
        js1 = "window.scrollTo(0,100)"
        driver.execute_script(js1)

    # 设置考勤地点
    @ddt.data(*sz)
    def test01_set(self, data):
        """设置考勤地点"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        attendance_site = AttendanceSiteList(driver)
        SZ = OperationMethod(driver)
        name = data['用例描述']
        store = data['店名'].split('-')
        am_st = data['考勤上午开始时间'].split('-')
        am_en = data['考勤上午结束时间'].split('-')
        pm_st = data['考勤下午开始时间'].split('-')
        pm_en = data['考勤下午结束时间'].split('-')
        Chinese = data['中文描述'].split('-')
        remark = data['备注'].split('-')
        trigger_btn = data['触发按钮']
        handle = data['操作']
        expect = data['预期结果']

        # 选取相应店
        attendance_site.select_data(store[1])

        def function_():
            # 基本信息
            # 中文描述
            SZ.input_(Chinese[0], Chinese[1])

            # 考勤上午开始时间
            SZ.input_(am_st[0], am_st[1])
            # 考勤上午结束时间
            SZ.input_(am_en[0], am_en[1])
            # 考勤下午开始时间
            SZ.input_(pm_st[0], pm_st[1])
            # 考勤下午结束时间
            SZ.input_(pm_en[0], pm_en[1])
            # # 备注
            SZ.textarea_(remark[0], remark[1])
            # driver.find_element_by_xpath('//form/div/div[6]/div[2]/div/div/div/textarea').clear()
            # driver.find_element_by_xpath('//form/div/div[6]/div[2]/div/div/div/textarea').send_keys('这是一条备注测试信息')
            sleep(5)
            # 保存
            attendance_site.save_btn(handle)
            sleep(5)

        if attendance_site.visibility():
            function_()

        else:
            # 点击设置考勤地点
            attendance_site.touch_btn(trigger_btn)
            # 提示框确定
            attendance_site.operation_btn('确定')
            function_()

        # 断言
        # 调用isElementExist方法，判断元素是否存在
        vis = attendance_site.visibility()
        try:
            # 使用断言 判断上面添加的编码是否在编码元素列表中
            self.assertEqual(vis, expect, msg=None)
            attendance_site.capture_screen(name + '成功')
            print(name + '成功')
        except Exception as e:
            attendance_site.error_screen(name + '失败')
            print(name + '失败')
            raise e
        print("-------------------考勤地点test_set运行完毕-------------------")

    # 取消考勤设置
    @ddt.data(*qx)
    def test02_abolish(self, data):
        """取消考勤地点"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        name = data['用例描述']
        attendance_site = AttendanceSiteList(driver)
        cancel = Cancel(driver)
        store = data['店名'].split('-')
        trigger_btn = data['触发按钮']
        handle = data['操作']
        expect = data['预期结果']

        # 选取相应店
        attendance_site.select_data(store[1])

        if attendance_site.visibility():
            # 点击取消考勤地点
            attendance_site.touch_btn(trigger_btn)
            # 提示框确定
            cancel.save_btn(handle)
            try:
                # 使用断言 判断上面添加的编码是否在编码元素列表中
                self.assertEqual(attendance_site.visibility(), expect, msg=None)
                attendance_site.capture_screen(name + '成功')
                print(name + '成功')
            except Exception as e:
                attendance_site.error_screen(name + '失败')
                print(name + '失败')
                raise e
        else:
            print('无考勤地点数据，无法取消')
        print("----------------------考勤地点test_abolish运行完毕------------------------")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
