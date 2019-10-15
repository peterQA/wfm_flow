# -*- coding: utf-8 -*-
import unittest
from time import sleep
from framework.browser_engine import BrowserEngine
from pageobjects.catalog_page import DirectoryList
from pageobjects.macro_set_page import *
from unit.login import login


# 宏设置
from unit.operation_fun import OperationMethod


class MacroSet(unittest.TestCase):
    def setUp(self):
        browser = BrowserEngine(self)
        self.driver = browser.open_browser(self)  # 读取浏览器类型
        driver = self.driver
        # 调用登录函数，默认username='peter',password='1234567'
        self.lg = login(driver)
        directory = DirectoryList(driver)

        # 考勤设置-考勤地点
        directory.two_level_select('系统管理', '宏设置')

        # 将滚动条拉到最底层
        js1 = "window.scrollTo(0,100)"
        driver.execute_script(js1)

    # 新建宏（考勤审查后）
    def test01_new(self):
        """新建宏（考勤审查前）macro"""
        driver = self.driver
        macros = MacroList(driver)
        method = OperationMethod(driver)
        add = AddMacro(driver)
        # 获取所有宏名
        names1 = macros.macro_list()
        print(macros.macro_list())
        # print(names1)

        # 点击考勤审查前 +
        macros.add_btn('考勤审查后')
        # 填写新建宏弹窗
        # 名称
        method.input_('名称', 'peter宏')
        # 执行存储过程
        method.input_('执行存储过程', '213432')
        # 保存
        add.save_btn('保存')
        sleep(0.5)
        # 再次获取所有宏名
        names2 = macros.macro_list()
        print(names2)

        # 断言
        try:
            self.assertNotEqual(names2, names1)

        except AssertionError:
            print('新建宏失败')
        else:
            print("新建宏成功")

        finally:
            print("-------------------宏设置test01_xinjian运行完毕-------------------")

    # 修改宏
    def test02_update(self):
        """修改宏"""
        driver = self.driver
        macros = MacroList(driver)
        alter = Alter(driver)
        names1 = macros.macro_list()
        print(names1)

        # 修改按钮路径(向上)
        alter.move_up(4, 'peter宏')
        sleep(0.2)
        names2 = macros.macro_list()
        print(names2)
        # 断言
        try:
            self.assertNotEqual(names2, names1)
        except AssertionError:
            print("修改宏失败")
        else:
            print("修改宏成功")
        finally:
            print("-------------------宏设置test02_update运行完毕-------------------")

    # 删除宏
    def test03_del(self):
        """删除宏"""
        driver = self.driver
        macros = MacroList(driver)

        dele = Del(driver)

        names1 = macros.macro_list()
        # print('删前', names1)
        macros.del_btn('peter宏')
        # driver.find_element_by_xpath('//main/div//div/span/span[1][contains(text(),"{0}")]/..//button[4]/span'.format('peter宏')).click()

        # 弹框确认
        dele.save_btn('确定')
        sleep(1)
        names2 = macros.macro_list()
        # print('删后', names2)

        try:
            self.assertNotEqual(names2, names1)
        except AssertionError:
            print("删除宏失败")
        else:
            print("删除宏成功")
        finally:
            print("-------------------宏设置test03_del运行完毕-------------------")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
    # # 构造测试集
    # suite = unittest.TestSuite()
    # print('添加前：', suite)
    # suite.addTest(HongSheZhi("test01_xinjian"))
    # suite.addTest(HongSheZhi('test02_update'))
    # suite.addTest(HongSheZhi("test03_del"))
    # print('添加后：', suite)
    #
    # # 执行测试
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
