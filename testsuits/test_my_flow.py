# -*- coding: utf-8 -*-
import unittest

import ddt

from framework.browser_engine import BrowserEngine
from pageobjects.my_flow_page import *
from pageobjects.catalog_page import DirectoryList
from unit.date_formatting import FormatTime
from unit.excel import ExcelUtils
from unit.login import login
from unit.sqlserver import DataBase

excel_utils = ExcelUtils("my_flow_info.xlsx", "Sheet1")
ly = excel_utils.dict_data()
excel_utils = ExcelUtils("my_flow_info.xlsx", "Sheet2")
lz = excel_utils.dict_data()
excel_utils = ExcelUtils("my_flow_info.xlsx", "Sheet3")
xj = excel_utils.dict_data()
excel_utils = ExcelUtils("my_flow_info.xlsx", "Sheet4")
dg = excel_utils.dict_data()
excel_utils = ExcelUtils("my_flow_info.xlsx", "Sheet5")
bdk = excel_utils.dict_data()
excel_utils = ExcelUtils("my_flow_info.xlsx", "Sheet6")
xcd = excel_utils.dict_data()
excel_utils = ExcelUtils("my_flow_info.xlsx", "Sheet7")
jb = excel_utils.dict_data()


# 录用申请
@ddt.ddt
class MYFlow(unittest.TestCase):

    def setUp(self):
        # 还原数据库
        # DataBase(1).database_restore()

        browser = BrowserEngine(self)
        self.driver = browser.open_browser(self)  # 读取浏览器类型
        driver = self.driver
        # 调用登录函数，默认username='peter',password='1234567'
        login(driver, username='wfm001', password='1234567')
        directory = DirectoryList(driver)
        # print('当前页url是：',url)
        # 流程-我的流程
        directory.two_level_select("流程", '我的流程')

    # 录用申请
    @ddt.data(*ly)
    def test01_employment_application(self, data):
        """流程-我的流程-录用申请"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        directory = DirectoryList(driver)
        my_flow = MyFlow(driver)
        my_apply = MyApply(driver)
        employment = EmploymentApplication(driver)
        common = FlowCommon(driver)
        ft = FormatTime()

        name = data['用例描述']
        flow = data['操作流程对象']
        pass_personnel = data['面试通过人员'].split('-')
        user = data['用户名'].split('-')
        cn_name = data['中文姓名'].split('-')
        hire_day = data['雇佣日'].split('->')
        system = data['考勤体系'].split('-')
        organization = data['组织单元'].split('-')
        post = data['职位'].split('-')
        group = data['用户组'].split('-')
        employee_type = data['员工类型'].split('-')
        verify_path = data['验证路径'].split('-')
        expect = data['预期结果']

        # 选择要操作的流程
        my_flow.select_flow(flow)
        # 从面试通过的人员中选取
        common.input_select(pass_personnel[0], pass_personnel[1])
        # 用户名
        common.input_(user[0], user[1])
        # 中文姓名
        common.input_(cn_name[0], cn_name[1])
        # 雇佣日
        common.input_(hire_day[0], ft.time_of_day())
        # 考勤体系
        common.input_select(system[0], system[1])
        # 组织单元
        employment.organization_btn(organization[0])
        employment.store_select([organization[1], organization[2], organization[3], organization[4], organization[5]])
        # 职位
        common.input_select(post[0], post[1])
        # 用户组
        common.input_select(group[0], group[1])
        # 员工类型
        common.input_select(employee_type[0], employee_type[1])
        # 提交
        common.submit_btn()
        sleep(0.2)
        # ok
        common.ok_btn()
        sleep(0.5)
        # 前往我的申请查看结果
        directory.two_select(verify_path[0], verify_path[1])
        sleep(1)
        # my_apply.item_btn(verify_path[2])
        # sleep(0.5)
        # element = my_apply.data_list(affirm)
        element = my_apply.application_name_list(verify_path[2])

        # 断言
        try:
            self.assertIn(expect, element)
            my_flow.capture_screen(name + '成功')
            print(name + '成功')

        except AssertionError as e:
            my_flow.error_screen(name + '失败')
            print(name + '失败')
            raise e
        print("-------------------录用申请test01_employment_application运行完毕-------------------")

    # 离职申请
    @ddt.data(*lz)
    def test02_dimission_application(self, data):
        """流程-我的流程-离职申请"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        directory = DirectoryList(driver)
        my_flow = MyFlow(driver)
        my_apply = MyApply(driver)
        common = FlowCommon(driver)
        ft = FormatTime()

        name = data['用例描述']
        flow = data['操作流程对象']
        dimission_type = data['离职类型'].split('-')
        dimission_cause = data['离职原因'].split('-')
        dimission_day = data['离职日期'].split('->')
        verify_path = data['验证路径'].split('-')
        expect = data['预期结果']

        # 选择要操作的流程
        my_flow.select_flow(flow)
        # 离职类型
        common.input_select(dimission_type[0], dimission_type[1])
        # 离职原因
        common.input_select(dimission_cause[0], dimission_cause[1])

        # 离职日期
        common.input_(dimission_day[0], ft.time_of_day())

        # 提交
        common.submit_btn()
        sleep(0.2)
        # ok
        common.ok_btn()
        sleep(0.5)
        # 前往我的申请查看结果
        directory.two_select(verify_path[0], verify_path[1])
        sleep(1)
        # my_apply.item_btn(verify_path[2])
        # sleep(0.5)
        # element = my_apply.data_list(affirm)
        element = my_apply.application_name_list(verify_path[2])

        # 断言
        try:
            self.assertIn(expect, element)
            my_flow.capture_screen(name + '成功')
            print(name + '成功')

        except AssertionError as e:
            my_flow.error_screen(name + '失败')
            print(name + '失败')
            raise e

        print("-------------------离职申请test01_employment_application运行完毕-------------------")

    # 休假申请
    @ddt.data(*xj)
    def test03_leave_application(self, data):
        """流程-我的流程-休假申请"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        directory = DirectoryList(driver)
        my_flow = MyFlow(driver)
        my_apply = MyApply(driver)
        common = FlowCommon(driver)
        ft = FormatTime()

        name = data['用例描述']
        flow = data['操作流程对象']
        leave_type = data['休假类型'].split('-')
        leave_cause = data['备注'].split('-')
        leave_day = data['期间'].split('->')
        verify_path = data['验证路径'].split('-')
        expect = data['预期结果']

        # 选择要操作的流程
        my_flow.select_flow(flow)
        # 休假类型
        common.input_select(leave_type[0], leave_type[1])
        # 期间
        common.input_date(leave_day[0], ft.time_of_day("09:00:00"), ft.next_of_day("09:00:00"))
        # 备注
        common.input_(leave_cause[0], leave_cause[1])

        # 提交
        common.submit_btn()
        sleep(0.2)
        # ok
        common.ok_btn()
        sleep(0.5)
        # 前往我的申请查看结果
        directory.two_select(verify_path[0], verify_path[1])
        sleep(1)
        # my_apply.item_btn(verify_path[2])
        # sleep(0.5)
        # element = my_apply.data_list(affirm)
        element = my_apply.application_name_list(verify_path[2])

        # 断言
        try:
            self.assertIn(expect, element)
            my_flow.capture_screen(name + '成功')
            print(name + '成功')

        except AssertionError as e:
            my_flow.error_screen(name + '失败')
            print(name + '失败')
            raise e
        print("-------------------录用申请test03_leave_application运行完毕-------------------")

    # 调岗申请
    @ddt.data(*dg)
    def test04_transfer_position_application(self, data):
        """流程-我的流程-调岗申请"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        directory = DirectoryList(driver)
        my_flow = MyFlow(driver)
        my_apply = MyApply(driver)
        employment = EmploymentApplication(driver)
        common = FlowCommon(driver)

        name = data['用例描述']
        flow = data['操作流程对象']
        personnel = data['员工'].split('-')
        st_date = data['开始日期'].split('->')
        organization = data['调往组织单元'].split('-')
        post = data['调往职位'].split('-')
        reason = data['理由'].split('-')
        verify_path = data['验证路径'].split('-')
        expect = data['预期结果']

        # 选择要操作的流程
        my_flow.select_flow(flow)
        # 选择员工
        common.select_employee(personnel[0], personnel[1])
        # 开始日期
        common.input_(st_date[0], time.strftime("%Y-%m-%d", time.localtime()))
        # 调往组织单元
        employment.organization_btn(organization[0])
        common.store_select([organization[1], organization[2], organization[3], organization[4], organization[5]])

        # 调往职位
        common.input_select(post[0], post[1])
        # 理由
        common.input_(reason[0], reason[1])
        # 提交
        common.submit_btn()
        sleep(0.2)
        # ok
        common.ok_btn()
        sleep(0.5)
        # 前往我的申请查看结果
        directory.two_select(verify_path[0], verify_path[1])
        sleep(1)
        # my_apply.item_btn(verify_path[2])
        # sleep(0.5)
        # element = my_apply.data_list(affirm)
        element = my_apply.application_name_list(verify_path[2])

        # 断言
        try:
            self.assertIn(expect, element)
            my_flow.capture_screen(name + '成功')
            print(name + '成功')

        except AssertionError as e:
            my_flow.error_screen(name + '失败')
            print(name + '失败')
            raise e
        print("-------------------调岗申请test04_transfer_position_application运行完毕-------------------")

    # 补打卡申请
    @ddt.data(*bdk)
    def test05_fill_clock_application(self, data):
        """流程-我的流程-补打卡申请"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        directory = DirectoryList(driver)
        my_flow = MyFlow(driver)
        my_apply = MyApply(driver)
        common = FlowCommon(driver)
        ft = FormatTime()

        name = data['用例描述']
        flow = data['操作流程对象']
        date = data['日期'].split('->')
        record = data['补打记录'].split('-')
        reason = data['理由'].split('-')
        verify_path = data['验证路径'].split('-')
        expect = data['预期结果']

        # 选择要操作的流程
        my_flow.select_flow(flow)
        # 日期
        common.input_(date[0], ft.time_of_day())
        # 补打记录
        driver.find_element_by_xpath("//header/div/div[2]/div//div[1]/div[contains(text(),'{0}')]"
                                     "/../../div[2]/div/button/span/i".format(record[0])).click()
        driver.find_element_by_xpath("//header/div/div[2]/div//div[1]/div[contains(text(),'{0}')]"
                                     "/../../..//div[4]/div/div[2]/div/div/span/span/i".format(record[0])).click()

        driver.find_elements_by_xpath("/html/body/div/div[1]/div[1]/ul/li[1]/span[contains(text(),'{0}')]"
                                      .format(record[1]))[0].click()

        driver.find_element_by_xpath("//header/div/div[2]/div//div[1]/div[contains(text(),'{0}')]"
                                     "/../../../div[4]/div/div[3]/div/input".format(record[0])).clear()
        driver.find_element_by_xpath("//header/div/div[2]/div//div[1]/div[contains(text(),'{0}')]"
                                     "/../../../div[4]/div/div[3]/div/input".format(record[0])).send_keys(record[2])

        # 理由
        common.input_(reason[0], reason[1])
        # 提交
        common.submit_btn()
        sleep(0.2)
        # ok
        common.ok_btn()
        sleep(0.5)

        # 前往我的申请查看结果
        directory.two_select(verify_path[0], verify_path[1])
        sleep(1)

        element = my_apply.application_name_list(verify_path[2])

        # 断言
        try:
            self.assertIn(expect, element)
            my_flow.capture_screen(name + '成功')
            print(name + '成功')

        except AssertionError as e:
            my_flow.error_screen(name + '失败')
            print(name + '失败')
            raise e
        print("-------------------调岗申请test05_fill_clock_application运行完毕-------------------")

    # 消迟到早退申请
    @ddt.data(*xcd)
    def test06_eliminate_lateness_and_early_departure_application(self, data):
        """流程-我的流程-消迟到早退申请"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        directory = DirectoryList(driver)
        my_flow = MyFlow(driver)
        my_apply = MyApply(driver)
        common = FlowCommon(driver)

        name = data['用例描述']
        flow = data['操作流程对象']

        reason = data['输入理由'].split('-')
        verify_path = data['验证路径'].split('-')
        expect = data['预期结果']
        # 数据库操作排班
        DataBase(2).execute_sql()

        directory.two_level_select('考勤处理', '考勤审查')
        # 点击审查按钮
        driver.find_element_by_xpath("//section/header/div[2]/div[3]/button/span[contains(text(),'审查')]").click()
        sleep(5)
        driver.find_element_by_xpath("//div/div[2]/div[1]/p/strong[contains(text(),'审查成功')]"
                                     "/../../../..//div[3]/button/span").click()
        sleep(2)
        directory.two_select('流程', '我的流程')

        # 选择要操作的流程
        my_flow.select_flow(flow)

        # 选取迟到信息
        driver.find_element_by_xpath('//section/header/div//label/span[1]/span').click()

        # 理由
        common.input_(reason[0], reason[1])
        # 提交
        common.submit_btn()
        sleep(0.2)
        # ok
        common.ok_btn()
        sleep(0.5)

        # 前往我的申请查看结果
        directory.two_select(verify_path[0], verify_path[1])
        sleep(1)
        element = my_apply.application_name_list(verify_path[2])

        # 断言
        try:
            self.assertIn(expect, element)
            my_flow.capture_screen(name + '成功')
            print(name + '成功')

        except AssertionError as e:
            my_flow.error_screen(name + '失败')
            print(name + '失败')
            raise e
        print("-------------------调岗申请test06_eliminate_lateness_and_early_departure_application运行完毕-------------------")

    # 加班申请
    @ddt.data(*jb)
    def test07_overtime_application(self, data):
        """流程-我的流程-加班申请"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        directory = DirectoryList(driver)
        my_flow = MyFlow(driver)
        my_apply = MyApply(driver)
        common = FlowCommon(driver)
        ft = FormatTime()

        name = data['用例描述']
        flow = data['操作流程对象']
        overtime_type = data['加班类型'].split('-')
        st_date = data['开始时间'].split('->')
        en_date = data['结束时间'].split('->')
        reason = data['备注'].split('-')
        verify_path = data['验证路径'].split('-')
        expect = data['预期结果']

        # 选择要操作的流程
        my_flow.select_flow(flow)

        # 选取加班类型
        common.input_select(overtime_type[0], overtime_type[1])
        # 开始时间
        common.input_(st_date[0], ft.time_of_day("18:00:00"))
        # 结束时间
        common.input_(en_date[0], ft.time_of_day("21:00:00"))
        # 备注
        common.input_(reason[0], reason[1])
        # 提交
        common.submit_btn()
        sleep(2)
        # ok
        common.ok_btn()
        sleep(0.2)

        # 前往我的申请查看结果
        directory.two_select(verify_path[0], verify_path[1])
        sleep(1)
        element = my_apply.application_name_list(verify_path[2])

        # 断言
        try:
            self.assertIn(expect, element)
            my_flow.capture_screen(name + '成功')
            print(name + '成功')

        except AssertionError as e:
            my_flow.error_screen(name + '失败')
            print(name + '失败')
            raise e
        print("-------------------调岗申请test07_overtime_application运行完毕-------------------")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()


