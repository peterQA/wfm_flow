# -*- coding: utf-8 -*-
import unittest
from time import sleep

import ddt

from framework.browser_engine import BrowserEngine
from pageobjects.catalog_page import DirectoryList
from pageobjects.time_set_page import *
from unit.login import login
from unit.operation_fun import OperationMethod
from unit.excel import ExcelUtils

excel_utils = ExcelUtils("time_set_info.xlsx", "Sheet1")
xz = excel_utils.dict_data()
excel_utils = ExcelUtils("time_set_info.xlsx", "Sheet2")
xg = excel_utils.dict_data()
excel_utils = ExcelUtils("time_set_info.xlsx", "Sheet3")
sc = excel_utils.dict_data()


# 工时设置
@ddt.ddt
class TimeSet(unittest.TestCase):
    def setUp(self):
        browser = BrowserEngine(self)
        self.driver = browser.open_browser(self)  # 读取浏览器类型
        driver = self.driver
        # 调用登录函数，默认username='peter',password='1234567'
        self.lg = login(driver)
        directory = DirectoryList(driver)
        # 考勤设置-考勤体系-工时设置
        directory.three_level_select("考勤设置", '考勤体系', '工时设置')
        # 选择考勤体系
        driver.find_element_by_xpath("//section/header/div/div/..//input").click()
        sleep(0.2)
        # 大陆门店考勤
        driver.find_element_by_xpath("//section/header/div/div/..//span[contains(text(),'大陆门店考勤')]").click()
        sleep(0.1)

    # 新增(正常)
    @ddt.data(*xz)
    def test01_create(self, data):
        """工时设置新增"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        timeset = TimeSetList(driver)
        XZ = OperationMethod(driver)
        add = Add(driver)

        name = data['用例描述']
        code = data['编码'].split('-')
        Chinese = data['中文描述'].split('-')
        shift_type = data['轮班类型'].split('-')
        trigger_btn = data['触发按钮']
        st = data['工作开始时间'].split('-')
        en = data['工作结束时间'].split('-')
        handle = data['操作']
        expect = data['预期结果']

        # 新增按钮
        timeset.operation_btn(trigger_btn)
        # 编码输入
        XZ.input_(code[0], code[1])
        # 中文描述
        XZ.input_(Chinese[0], Chinese[1])
        # 轮班类型-中班
        XZ.input_select(shift_type[0], shift_type[1])
        # 切换到详细信息
        driver.find_element_by_xpath(".//*[@id='tab-second']").click()
        # 工作开始时间
        XZ.input_(st[0], st[1])

        # 工作结束时间
        # 手动录入
        XZ.input_(en[0], en[1])

        # 确定
        add.save_btn(handle)
        sleep(0.2)
        # 断言
        texts = XZ.data_list()

        try:
            # 使用断言
            self.assertIn(expect, texts)
            timeset.capture_screen(name + '成功')
            print(name + '成功')

        except AssertionError as e:
            timeset.error_screen(name + '失败')
            print(name + '失败')
            raise e
        print("-------------------工时设置test_create运行完毕-------------------")

    # 修改（正常）
    @ddt.data(*xg)
    def test02_alter(self, data):
        """工时设置修改"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        timeset = TimeSetList(driver)
        XG = OperationMethod(driver)
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
                timeset.select_data(element)
                sleep(0.3)
                break
        # 点击修改按钮
        # driver.find_element_by_xpath('//section/footer/div/div/div/button[2]').click()
        timeset.operation_btn(trigger_btn)
        # 中文描述
        XG.input_(Chinese[0], Chinese[1])
        # 确定
        alter.save_btn(handle)
        # 断言依据获取
        text = timeset.unit_data(code[1])

        try:
            # 使用断言 判断上面添加的编码是否在编码元素列表中
            self.assertEqual(text, expect)
            timeset.capture_screen(name + '成功')
            print(name + '成功')
        except AssertionError as e:
            timeset.error_screen(name + '失败')
            print(name + '失败')
            raise e
        print("-------------------工时设置test_alter运行完毕-------------------")

    # 删除
    @ddt.data(*sc)
    def test03_del(self, data):
        """工时设置删除"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        time_set = TimeSetList(driver)
        SC = OperationMethod(driver)
        alter = Alter(driver)
        dele = Del(driver)

        name = data['用例描述']
        code = data['编码'].split('-')
        trigger_btn = data['触发按钮']
        handle = data['操作']

        # 筛选出所有编码元素
        # elements = driver.find_elements_by_xpath('//table/tbody/tr[*]/td[1]/div')
        elements = SC.data_list()
        print(elements)
        for element in elements:
            if element == code[1]:
                # 选中要操作的元素
                time_set.select_data(element)
                break
        # 点击修改按钮
        time_set.operation_btn('修改')
        # 删除
        alter.save_btn(trigger_btn)
        # 选择提示框里的确定按钮
        dele.save_btn(handle)
        # 编码列表
        elements1 = SC.data_list()
        try:
            # 断言
            self.assertNotIn(code[1], elements1)
            time_set.capture_screen(name + '成功')
            print(name + '成功')

        except AssertionError as e:
            time_set.error_screen(name + '失败')
            print(name + '失败')
            raise e
        print("-------------------工时设置test03_del运行完毕-------------------")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
    # # 构造测试集
    # suite = unittest.TestSuite()
    # print('添加前：', suite)
    # suite.addTest(XiuJiaKaoQinTiXi("test01_xinzeng_correct"))
    # suite.addTest(XiuJiaKaoQinTiXi("test03_xinzeng_coding_null"))
    # suite.addTest(XiuJiaKaoQinTiXi("test02_xiugai_correct"))
    # suite.addTest(XiuJiaKaoQinTiXi("test04_del_correct"))
    # print('添加后：', suite)
    #
    # # 执行测试
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
