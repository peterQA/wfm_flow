# -*- coding: utf-8 -*-
import unittest
from time import sleep
from framework.browser_engine import BrowserEngine
from pageobjects.catalog_page import DirectoryList
from pageobjects.pretreatment_rule_page import *
from unit.login import login
from unit.operation_fun import OperationMethod


# 预处理规则
class PretreatmentRule(unittest.TestCase):
    def setUp(self):
        browser = BrowserEngine(self)
        self.driver = browser.open_browser(self)  # 读取浏览器类型
        driver = self.driver
        # 调用登录函数，默认username='peter',password='1234567'
        self.lg = login(driver)
        directory = DirectoryList(driver)

        # 考勤设置-考勤地点
        directory.two_level_select('系统管理', '预处理规则')

        # 将滚动条拉到最底层
        js1 = "window.scrollTo(0,100)"
        driver.execute_script(js1)

    # 新建宏（排班规则）
    def test01_new(self):
        """新建预处理规则"""
        driver = self.driver
        rule = RuleList(driver)
        method = OperationMethod(driver)
        add = AddMacro(driver)
        # 获取所有宏名
        names1 = rule.macro_list()
        print(rule.macro_list())
        # print(names1)

        # 点击排班规则 +
        rule.add_btn('排班规则')
        # 填写新建规则弹窗
        # 名称
        method.input_('名称', 'peter排班规则')
        # 执行存储过程
        method.input_('执行存储过程', '213432')
        # 保存
        add.save_btn('保存')
        sleep(0.5)
        # 再次获取所有宏名
        names2 = rule.macro_list()
        print(names2)

        # 断言
        try:
            self.assertNotEqual(names2, names1)

        except AssertionError:
            print('新建规则失败')
        else:
            print("新建规则成功")

        finally:
            print("-------------------预处理规则test01_new运行完毕-------------------")

    # 修改规则
    def test02_update(self):
        """修改规则"""
        driver = self.driver
        rule = RuleList(driver)
        alter = Alter(driver)
        names1 = rule.macro_list()
        print(names1)

        # 修改按钮路径(向上)
        alter.move_up(4, 'peter排班规则')
        sleep(0.2)
        names2 = rule.macro_list()
        print(names2)
        # 断言
        try:
            self.assertNotEqual(names2, names1)
        except AssertionError:
            print("修改规则失败")
        else:
            print("修改规则成功")
        finally:
            print("-------------------宏设置test02_update运行完毕-------------------")

    # 删除规则
    def test03_del(self):
        """删除规则"""
        driver = self.driver
        rule = RuleList(driver)

        dele = Del(driver)

        names1 = rule.macro_list()
        # print('删前', names1)
        rule.del_btn('peter排班规则')
        # driver.find_element_by_xpath('//main/div//div/span/span[1][contains(text(),"{0}")]/..//button[4]/span'.format('peter宏')).click()

        # 弹框确认
        dele.save_btn('确定')
        sleep(1)
        names2 = rule.macro_list()
        # print('删后', names2)

        try:
            self.assertNotEqual(names2, names1)
        except AssertionError:
            print("删除规则失败")
        else:
            print("删除规则成功")
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
