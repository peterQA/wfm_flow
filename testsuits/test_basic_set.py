# -*- coding: utf-8 -*-
import unittest
from time import sleep
import os

import ddt

from framework.browser_engine import BrowserEngine
from pageobjects.basic_setup_page import *
from pageobjects.catalog_page import DirectoryList
from unit.excel import ExcelUtils
from unit.login import login
from unit.operation_fun import OperationMethod

excel_utils = ExcelUtils("basic_set_info.xlsx", "Sheet1")
jb = excel_utils.dict_data()
excel_utils = ExcelUtils("basic_set_info.xlsx", "Sheet2")
tp = excel_utils.dict_data()
excel_utils = ExcelUtils("basic_set_info.xlsx", "Sheet3")
qt = excel_utils.dict_data()


# 基本设置
@ddt.ddt
class BasicSetup(unittest.TestCase):
    def setUp(self):
        browser = BrowserEngine(self)
        self.driver = browser.open_browser(self)  # 读取浏览器类型
        driver = self.driver
        # 调用登录函数，默认username='peter',password='1234567'
        self.lg = login(driver)
        directory = DirectoryList(driver)
        # print('当前页url是：',url)
        # 考勤处理-排班管理
        directory.two_level_select("系统管理", '基本设置')

    # 基本信息
    @ddt.data(*jb)
    def test01_basic_info(self, data):
        """基本设置-基本信息"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        control = OperationMethod(driver)
        basic = BasicInfo(driver)

        name = data['用例描述']
        operand = data['操作对象']
        identity_card = data['身份证']
        passport = data['护照']
        contains_characters = data['密码机制自定义包含字符'].split('-')
        password_mini = data['密码最小长度']
        lock_screen = data['未操作锁屏时长']
        gesture_password = data['手势密码']
        gps_scope = data['GPS定位有效范围']
        default_language = data['系统默认语言']
        week_st = data['每周开始时间']
        notice_max = data['公告最大附件']

        expect = data['预期结果']

        # 基本信息
        basic.title_btn(operand)
        # 初始密码
        control.input_number('身份证', identity_card)

        control.input_number('护照', passport)
        # control.checkbox("强制修改初始化密码")

        # 密码机制
        control.checkbox(contains_characters[0])
        control.checkbox(contains_characters[1])
        control.input_number('密码最小长度', password_mini)
        control.input_number('设置未操作', lock_screen)

        # 手势密码
        control.checkbox(gesture_password)

        # GPS
        control.input_number('GPS定位有效范围', gps_scope)

        # 域启用
        # control.checkbox('是否启用域')

        # 系统默认语言
        control.checkbox(default_language)

        # 每周开始日期
        control.checkbox(week_st)

        # 附件限制大小
        control.input_number('公告最大附件为', notice_max)

        # 保存
        basic.save_btn()
        sleep(0.4)
        # 获取初始密码身份证位数
        data2 = basic.modified_data('身份证')
        print("身份后aria-valuenow的值是：", expect)
        # 断言
        try:
            self.assertEqual(data2, expect)

            print('基本信息设置成功')

        except AssertionError as e:

            print('基本信息设置失败')
            raise e

        print("-------------------基本信息test01_basic_Info运行完毕-------------------")

    # 上传图片
    @ddt.data(*tp)
    def test02_image_upload(self, data):
        """基本设置-图片设置(上传)"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        basic = BasicInfo(driver)
        image = Image(driver)

        operand = data['操作对象']
        ratio = data['App登录图片:比例']
        expect = data['预期结果']

        # 图片设置
        basic.title_btn(operand)

        # 调用isElementExist方法，判断元素是否存在
        flag = image.judge_img(ratio)

        if not flag:
            # 点击+上传图片
            image.upload_btn(ratio)
            # 调用upfile.exe上传程序
            # "F:\web\upfile.exe F:\web\tu.png"前一个路径是AOTOit脚本所在路径，后一个是图片所在路径，要求全部使用绝对路径
            os.system(r"F:\wfm_flow\unit\up_picture.exe F:\wfm_flow\unit\tu.png")
            sleep(0.2)
            # 判断图片是否存在
            st = image.judge_img(ratio)

            try:
                self.assertEqual(str(st), expect)
                pass
            except Exception as e:
                print(e)
                print('图片上传失败')
                raise e
            else:
                print('图片上传成功')
        else:
            print('图片已存在')
        print("-------------------图片设置test02_image_upload运行完毕-------------------")

    # 删除图片
    @ddt.data(*tp)
    def test03_image_dele(self, data):
        """基本设置-图片设置(删除)"""
        driver = self.driver
        basic = BasicInfo(driver)
        image = Image(driver)

        operand = data['操作对象']
        ratio = data['App登录图片:比例']
        expect = data['预期结果']

        # 图片设置
        basic.title_btn(operand)
        # 获取图片

        # 调用isElementExist方法，判断元素是否存在i
        flag = image.judge_img(ratio)

        if flag:
            # 点击删除图片
            image.del_btn(ratio)
            sleep(0.4)
            # 判断图片是否存在
            st = image.judge_img(ratio)
            try:
                self.assertNotEqual(str(st), expect)
            except Exception as e:
                print(e)
                print('图片删除失败')
                raise e
            else:
                print('图片删除成功')
        else:
            print('图片不存在')

        print("-------------------图片设置test03_image_dele运行完毕-------------------")

    # 其他设置
    @ddt.data(*qt)
    def test04_other_setting(self, data):
        """其他设置"""
        if data["skip"] == 'True':
            self.skipTest("跳过示例")
        driver = self.driver
        control = OperationMethod(driver)
        basic = BasicInfo(driver)

        name = data['用例描述']
        operand = data['操作对象']
        take_out = data['年假抵充方式']
        month_man_hour = data['每月标准工时']
        enabled_shift = data['启用班次']
        gps_scope = data['优先使用休假类型']
        rest_indate = data['调休有效期最多']
        bargain_expire = data['合同到期提前']
        probation_expire = data['试用期到期提前']
        health_expire = data['健康证到期提前']
        expect = data['预期结果']

        # 其他设置
        basic.title_btn(operand)

        # 年假抵充方式
        control.checkbox(take_out)
        # 每月标准工时
        control.input_number('每月标准工时', month_man_hour)
        # 启用班次
        control.input_number('启用班次', enabled_shift)
        # 调休结余配置
        control.checkbox('可用调休假只统计历史数据')
        control.input_number('调休有效期最多', rest_indate)
        # 证件管理
        control.input_number('合同到期提前', bargain_expire)
        control.input_number('试用期到期提前', probation_expire)
        control.input_number('健康证到期提前', health_expire)

        # 保存
        driver.find_element_by_xpath("//*[@id='pane-7']/div/section/footer/div/button/span").click()
        sleep(0.4)
        # 获取每月标准工时
        data2 = basic.modified_data('标准工时')
        print("后标准工时aria-valuenow的值是：", data2)
        # 断言
        try:
            self.assertEqual(data2, expect)

            print('基本信息设置成功')

        except AssertionError as e:

            print('基本信息设置失败')
            raise e

        print("-------------------其他设置test04_other_setting运行完毕-------------------")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()

    # 构造测试集
    # suite = unittest.TestSuite()
    # print('添加前：', suite)
    # # suite.addTest(JiBenXinXi("test_chushimima"))
    # # suite.addTest(JiBenXinXi("test_mimajizhi"))
    # # suite.addTest(JiBenXinXi('test_shoushimima'))
    # suite.addTest(BasicSetup('test04_other_setting'))
    # #
    # print('添加后：', suite)
    #
    # # 执行测试
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
