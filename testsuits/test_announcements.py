# -*- coding: utf-8 -*-
import unittest
from time import sleep

import ddt

from framework.browser_engine import BrowserEngine
from pageobjects.catalog_page import DirectoryList
from pageobjects.announcements_page import *
from unit.excel import ExcelUtils
from unit.login import login
from unit.operation_fun import OperationMethod

excel_utils = ExcelUtils("announcements_info.xlsx", "Sheet1")
xz = excel_utils.dict_data()
excel_utils = ExcelUtils("announcements_info.xlsx", "Sheet2")
xg = excel_utils.dict_data()
excel_utils = ExcelUtils("announcements_info.xlsx", "Sheet3")
fz = excel_utils.dict_data()
excel_utils = ExcelUtils("announcements_info.xlsx", "Sheet4")
sc = excel_utils.dict_data()


# 公告管理
@ddt.ddt
class Announcements(unittest.TestCase):
    def setUp(self):
        browser = BrowserEngine(self)
        self.driver = browser.open_browser(self)  # 读取浏览器类型
        driver = self.driver
        # 调用登录函数，默认username='peter',password='1234567'
        self.lg = login(driver)
        directory = DirectoryList(driver)
        # 考勤设置-考勤体系-新建考勤体系
        directory.two_level_select('系统管理', '公告管理')
        driver.implicitly_wait(10)

        # 将滚动条拉到最底层
        js1 = "window.scrollTo(0,100)"
        driver.execute_script(js1)

    # 新增
    @ddt.data(*xz)
    def test01_create(self, data):
        """公告管理新增"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        XZ = OperationMethod(driver)
        announce_ments = AnnouncementsList(driver)
        add = Add(driver)

        name = data['用例描述']
        code = data['标题'].split('-')
        operant = data['生效日'].split('=')
        content = data['内容']
        trigger_btn = data['触发按钮']
        handle = data['操作']
        expect = data['预期结果']

        # 筛选出所有编码元素
        if code[1] not in XZ.data_list():

            # 新增按钮
            announce_ments.operation_btn(trigger_btn)

            # 标题
            XZ.input_(code[0], code[1])
            # 内容
            add.mtext(content)
            # # 发送所有人
            XZ.checkbox1('发送所有人')
            # 封面
            add.upload('封面', r"F:\wfm_flow\unit\up_picture.exe F:\wfm_flow\unit\tu.png")
            # 生效日
            XZ.input_(operant[0], operant[1])
            # 保存并发布
            add.save_btn(handle)
            # 获取标题列表
            account_list2 = XZ.data_list()
            # 断言

            try:
                # 使用断言 判断上面添加的编码是否在编码元素列表中
                self.assertIn(expect, account_list2)
                announce_ments.capture_screen(name + '成功')
                print(name + '成功')

            except AssertionError as e:
                announce_ments.error_screen(name + '失败')
                print(name + '失败')
                raise e
        else:
            print("该账户已经存在")
        print("-------------------公告管理test01_create运行完毕-------------------")

    # 修改（正常）
    @ddt.data(*xg)
    def test02_alter(self, data):
        """公告管理修改"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        XG = OperationMethod(driver)
        announce_ments = AnnouncementsList(driver)
        alter = Alter(driver)

        name = data['用例描述']
        code = data['标题'].split('-')
        edit = data['修改项']
        trigger_btn = data['触发按钮']
        handle = data['操作']
        expect = data['预期结果']

        # 筛选出所有编码元素
        # 标题路径
        for text in XG.data_list():
            if text == code[1]:
                # 选中要操作的行
                announce_ments.select_data(code[1])
                sleep(0.3)
                break
        # 获取选中行置顶一栏信息
        # 点击修改按钮
        announce_ments.operation_btn(trigger_btn)

        # 置顶
        XG.checkbox1(edit)
        # 保存并发布
        alter.save_btn(handle)
        sleep(0.3)
        # 再次获取选中行置顶一栏信息
        stick2 = announce_ments.unit_data(code[1])
        print(stick2)

        # 断言
        try:
            self.assertEqual(stick2, expect)
            announce_ments.capture_screen(name + '成功')
            print(name + '成功')
        except AssertionError as e:
            announce_ments.error_screen(name + '失败')
            print(name + '失败')
            raise e

        print("-------------------加班政策test02_alter_correct运行完毕-------------------")

    # 复制
    @ddt.data(*fz)
    def test03_copy(self, data):
        """公告管理复制"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        FZ = OperationMethod(driver)
        announce_ments = AnnouncementsList(driver)
        cp = Copy(driver)

        name = data['用例描述']
        code = data['标题'].split('-')
        operant = data['生效日'].split('=')

        trigger_btn = data['触发按钮']
        handle = data['操作']
        # 筛选出所有编码元素
        elements1 = FZ.data_list()
        print(elements1)

        # 标题路径
        for element in FZ.data_list():
            if element == code[1]:
                # 选中要操作的行
                announce_ments.select_data(code[1])
                sleep(0.2)
                break
        # 点击修改按钮
        announce_ments.operation_btn(trigger_btn)
        # 标题
        FZ.input_(code[0], code[1]+'1')

        # 生效日期
        FZ.input_(operant[0], operant[1])

        # 选择提示框里的确定按钮
        cp.save_btn(handle)
        sleep(0.3)
        # 编码列表
        elements2 = FZ.data_list()
        print(elements2)

        try:
            # 断言
            self.assertNotEqual(elements2, elements1)
            announce_ments.capture_screen(name + '成功')
            print(name + '成功')
        except AssertionError as e:
            announce_ments.error_screen(name + '失败')
            print(name + '失败')
            raise e

    # 删除
    @ddt.data(*sc)
    def test04_del(self, data):
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        """公告管理删除"""
        driver = self.driver
        SC = OperationMethod(driver)
        announce_ments = AnnouncementsList(driver)
        alter = Alter(driver)
        dele = Del(driver)

        name = data['用例描述']
        code = data['标题'].split('-')
        trigger_btn = data['触发按钮']
        handle = data['操作']
        expect = data['预期结果']
        # 筛选出所有编码元素
        # 标题路径
        for element in SC.data_list():
            if element == code[1]:
                # 选中要操作的行
                announce_ments.select_data(code[1])
                sleep(0.2)
                break
        # 点击修改按钮
        announce_ments.operation_btn('修改')

        # 点击删除按钮
        alter.del_btn(trigger_btn)

        # 选择提示框里的确定按钮
        dele.save_btn(handle)
        sleep(0.3)
        # 编码列表
        elements1 = SC.data_list()

        try:
            # 断言
            self.assertNotIn(expect, elements1)
            announce_ments.capture_screen(name + '成功')
            print(name + '成功')
        except AssertionError as e:
            announce_ments.error_screen(name + '失败')
            print(name + '失败')
            raise e
        print("-------------------用户组管理test03_del_correct运行完毕-------------------")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
