# -*- coding: utf-8 -*-
import unittest
import ddt

from framework.browser_engine import BrowserEngine
from pageobjects.catalog_page import *
from pageobjects.workforce_management_page import *
from unit.excel import ExcelUtils
from unit.login import login
from logs.logger import Logger

logger = Logger(logger="WFMSearch").getlog()
excel_utils1 = ExcelUtils("workforceManagement_info.xlsx", "Sheet1")
excel_utils2 = ExcelUtils("workforceManagement_info.xlsx", "Sheet2")
excel_utils3 = ExcelUtils("workforceManagement_info.xlsx", "Sheet3")
excel_utils4 = ExcelUtils("workforceManagement_info.xlsx", "Sheet4")
excel_utils5 = ExcelUtils("workforceManagement_info.xlsx", "Sheet5")

select_group = excel_utils1.dict_data()
select_shift = excel_utils2.dict_data()
copy_others = excel_utils3.dict_data()
apply_others = excel_utils4.dict_data()
clear_shift = excel_utils5.dict_data()


# 排班管理
@ddt.ddt
class WorkforceManagement(unittest.TestCase):

    def setUp(self):
        self.module_name = '排班管理'
        browser = BrowserEngine(self)
        self.driver = browser.open_browser(self)  # 读取浏览器类型
        driver = self.driver
        # 调用登录函数，默认username='peter',password='1234567'
        self.lg = login(driver)
        directory = DirectoryList(driver)
        # print('当前页url是：',url)
        # 考勤处理-排班管理
        directory.two_level_select("考勤处理", '排班管理')

        # 选择考勤地点（港汇广场店）
        attendance_path = '//section/header/div[1]/div[3]/div/div/input'
        driver.find_element_by_xpath(attendance_path).click()
        sleep(0.2)
        # actions = ActionChains(driver)
        # actions.move_to_element(attendance_path + "/../..//span[contains(text(),'{0}')]".format('办公室')) .perform()

        # js1 = "document.getElementsByClassName('el-scrollbar').scrollTop=200"
        # driver.execute_script(js1)
        target = driver.find_element_by_xpath(attendance_path + "/../..//span[contains(text(),'{0}')]".format('港汇广场店'))

        driver.execute_script("arguments[0].scrollIntoView();", target)

        # sleep(5)
        driver.find_element_by_xpath(attendance_path + "/../..//span[contains(text(),'{0}')]".format('港汇广场店')).click()
        sleep(0.5)

        texts = []
        elements = driver.find_elements_by_xpath('//section/main/div/div[2]/table/thead/tr[3]/th/div')
        for element in elements:
            sleep(0.1)
            texts.append(element.text)
        print("haha", texts)
        # driver.find_element_by_xpath('//table/thead//button[1]/span').click()

        while '8-4' not in texts:
            sleep(0.2)
            driver.find_element_by_xpath('//table/thead//button[1]/span').click()
            sleep(0.2)
            elements1 = driver.find_elements_by_xpath('//section/main/div/div[2]/table/thead/tr[3]/th/div')
            for element in elements1:
                sleep(0.1)
                texts.append(element.text)
            continue

    def tearDown(self):
        self.driver.quit()

    @ddt.data(*select_group)
    # 选择分组
    def test01_select_group(self, data):
        """排班管理-选择分组"""
        if data["skip"] == 'True':
            self.skipTest("强制跳过示例")
        driver = self.driver
        listpage = ScheduleManagementList(driver)
        grouppage = ChooseGroup(driver)
        describe = data['用例描述']
        user_id = data['员工id']
        trigger_btn = data['触发按钮']
        group = data['分组']
        grouping_state1 = data['预期结果']

        print('data------', data)
        # 选择要操作的数据(WFM005)
        listpage.operate_line(user_id)
        # # 选择前的分组状态
        # grouping_state1 = Listpage.group_status1(user_id)
        # print("grouping_state1:", grouping_state1)

        # 选择分组(分组2)
        listpage.select_group_btn(trigger_btn)
        sleep(0.5)
        # 分组2
        grouppage.group_checkbox(group)
        # 确认
        grouppage.confirm_btn()
        sleep(0.5)
        # 选择后的分组状态
        grouping_state2 = listpage.group_status2(user_id)
        print("grouping_state2:", grouping_state2)

        sleep(2)
        # 断言
        try:
            self.assertEqual(grouping_state2, grouping_state1)
            logger.info(describe + '成功')
            logger.info("Test Pass")
            print(describe + '成功')
            # 截图
            listpage.capture_screen(describe + '成功')
        except AssertionError as e:
            listpage.error_screen(describe + '失败')
            logger.error(describe + '失败')
            logger.error("Test Fail:断言失败")
            print(describe + '失败')
            raise e
        else:
            print(describe + '成功')

        print("-------------------排班管理test01_select_group运行完毕-------------------")

    @ddt.data(*select_shift)
    # 选择班次
    def test02_select_shift(self, data):
        """排班管理-选择班次"""
        if data["skip"] == 'True':
            self.skipTest("强制跳过示例")
        driver = self.driver
        changeShift = ChangeShift(driver)
        listpage = ScheduleManagementList(driver)
        describe = data['用例描述']
        user_id = data['员工id']
        trigger_btn = data['触发按钮']
        shift = data['班次']
        state1 = data['预期结果']
        print('data=========', data)
        # 选择要操作的数据(WFM005)
        listpage.operate_line1(user_id)
        # 选择前的班次状态
        # state1 = listpage.shift_status1('WFM005')
        print("grouping_state1:", state1)

        # 选择班次
        listpage.select_shift_btn(trigger_btn)
        sleep(1)
        # 早
        changeShift.shift_checkbox(shift)

        # 确认
        changeShift.confirm_btn()
        sleep(1)
        # 选择后的班次状态
        state2 = listpage.shift_status2()
        print("grouping_state2:", state2)
        sleep(1)
        # 断言
        try:
            self.assertEqual(state2, state1)
            logger.info(describe + '成功')
            logger.info("Test Pass")
            print(describe + '成功')
            # 截图
            listpage.capture_screen(describe + '成功')
        except AssertionError as e:
            listpage.error_screen(describe + '失败')
            logger.error(describe + '失败')
            logger.error("Test Fail:断言失败")
            print(describe + '失败')
            raise e
        print("-------------------排班管理test02_select_shift运行完毕-------------------")

    @ddt.data(*copy_others)
    # 复制给其他人
    def test03_copy_others(self, data):
        """排班管理-复制给其他人"""
        if data["skip"] == 'True':
            self.skipTest("强制跳过示例")
        driver = self.driver
        Listpage = ScheduleManagementList(driver)
        Copypage = CopyTheOther(driver)
        describe = data['用例描述']
        user_id = data['员工id']
        trigger_btn = data['触发按钮']
        _other = data['复制班次给其他人']
        state1 = data['预期结果']
        # 清除复制前的班次状态(其他人)
        # other = "//tbody/tr[*]/td[1]/div/span/div/div[1][text()= '%s']" % 'WFM001'
        # driver.find_element_by_xpath(other + "/../../../../../td[3]").click()
        # driver.find_element_by_xpath("//header/div[3]/div/div/button[3]").click()
        # 选择要操作的数据(WFM005)
        Listpage.operate_line(user_id)
        # 复制给其他人
        Listpage.copy_other_btn(trigger_btn)
        sleep(1)
        # 勾选要复制的人
        Copypage.other_checkbox(_other)
        # 确认
        Copypage.confirm_btn1()
        sleep(1)
        # 复制后的班次状态(本人)
        # grouping_state1 = Listpage.oneself()
        # print("grouping_state1:", grouping_state1)
        # 复制后的班次状态(其他人)
        grouping_state2 = Listpage.oneother()
        print("grouping_state2:", grouping_state2)
        sleep(1)
        # 断言
        try:
            self.assertEqual(grouping_state2, state1)
            logger.info(describe + '成功')
            logger.info("Test Pass")
            print(describe + '成功')
            # 截图
            Listpage.capture_screen(describe + '成功')
        except AssertionError as e:
            Listpage.error_screen(describe + '失败')
            logger.error(describe + '失败')
            logger.error("Test Fail:断言失败")
            print(describe + '失败')
            raise e
        else:
            print(describe + '成功')

        print("-------------------排班管理test03_copy_others运行完毕-------------------")

    @ddt.data(*apply_others)
    # 应用到其他日期
    def test04_apply_others(self, data):
        """排班管理-应用到其他日期"""
        if data["skip"] == 'True':
            self.skipTest("强制跳过示例")
        driver = self.driver
        Listpage = ScheduleManagementList(driver)
        applypage = ApplyDate(driver)
        name = data['用例描述']
        user_id = data['员工id']
        trigger_btn = data['触发按钮']
        others_date = data['应用到其他日期']
        state = data['预期结果']

        # 选择要操作的数据(WFM005)
        Listpage.operate_line1(user_id)
        # 应用到其他日期
        Listpage.apply_date_btn(trigger_btn)
        # 开始日期
        applypage.start_date_input(others_date)
        applypage.input_quit()
        sleep(0.2)
        # 确认
        applypage.conf_btn()
        sleep(0.2)
        # 应用到其他日期后的班次状态
        state2_text = Listpage.use_shift_status2()

        # 断言
        try:
            self.assertEqual(state2_text, state)
            logger.info(name + '成功')
            logger.info("Test Pass")
            print(name + '成功')
            # 截图
            Listpage.capture_screen(name + '成功')
        except AssertionError as e:
            Listpage.error_screen(name + '失败')
            logger.error(name + '失败')
            logger.error("Test Fail:断言失败")
            print(name + '失败')
            raise e
        print("-------------------排班管理test04_apply_others运行完毕-------------------")

    @ddt.data(*clear_shift)
    # 清除班次
    def test05_clear_shift(self,data):
        """排班管理-清除班次"""
        if data["skip"] == 'True':
            self.skipTest("强制跳过示例")
        driver = self.driver
        user_id = data['员工id']

        name = data['用例描述']
        listpage = ScheduleManagementList(driver)

        # 选择要操作的数据(当前页的所有班次数据)
        sleep(0.2)
        listpage.clear_line()

        # 选择前的分组状态
        text1 = listpage.clear_shift_state1(user_id)
        print(text1)
        # 清除班次
        listpage.clear_shift_btn('清除班次')
        sleep(0.2)
        # 选择后的分组状态
        text2 = listpage.clear_shift_state2(user_id)
        print(text2)
        sleep(1)

        # 断言
        try:
            self.assertNotEqual(text2, text1)
            logger.info(name + '成功')
            logger.info("Test Pass")
            print(name + '成功')
            # 截图
            listpage.capture_screen(name + '成功')
        except AssertionError as e:
            listpage.error_screen(name + '失败')
            logger.error(name + '失败')
            logger.error("Test Fail:断言失败")
            print(name + '失败')
            raise e

        print("-------------------排班管理test05_clear_shift运行完毕-------------------")


if __name__ == "__main__":
    unittest.main()
    
    # 构造测试集
    # suite = unittest.TestSuite()
    # print('添加前：', suite)
    # suite.addTest(StaffPolicyAllocation("test01_create_correct"))
    # suite.addTest(StaffPolicyAllocation("test02_create_coding_null"))
    # suite.addTest(StaffPolicyAllocation("test03_alter_correct"))
    # suite.addTest(StaffPolicyAllocation("test05_del_correct"))
    # print('添加后：', suite)
    #
    # # 执行测试
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
