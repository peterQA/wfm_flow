# encoding=utf-8
from HTMLTestRunner import HTMLTestRunner
import unittest
from time import sleep
from webbrowser import browser

import ddt
from parameterized import parameterized

from Test_data.test_data import *
from framework.browser_engine import BrowserEngine
from pageobjects.login_page import Login
from unit.excel import *
from unit.login import *

excel_utils = ExcelUtils("login_info.xlsx", "登录测试数据")
login_data = excel_utils.dict_data()


@ddt.ddt
class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        driver = BrowserEngine(cls)
        cls.driver = driver.open_browser(cls)  # 读取浏览器类型

    @ddt.data(*login_data)
    def test_login(self, data):
        if data["skip"] == 'True':
            self.skipTest("强制跳过示例")
        self._testMethodDoc = data["id"] + "_" + data["case_desc"]
        name = data['name']
        # username = data["username"]
        username = data["username"]

        password = data["password"]
        assert_text = data['expected']
        driver = self.driver
        # 刷新页面
        driver.refresh()
        sleep(1)
        # 调用登陆函数，返回登陆前的url
        login_url = driver.current_url
        lg = login(driver, username, password)
        if name == 'peter' or name == 'wfm001':
            sleep(1)
            # 获取登陆后的url
            url = self.driver.current_url
            print("login_url", login_url)
            print('url1', url)

            try:
                self.assertNotEqual(url, login_url)
                lg.capture_screen(name + '测试登录成功')
                print(name+'测试登录成功')

            except AssertionError as e:
                lg.error_screen(name+'测试登录失败')
                print(name+'测试登录失败')

                raise e
        else:
            sleep(1)
            tips = self.driver.find_element_by_xpath('/html/body/div[2]/div').text[3:-2].strip('\n')
            try:
                self.assertEqual(tips, assert_text)
                lg.capture_screen(name + '测试成功')
                print(name+'测试成功')
            except AssertionError as e:
                lg.error_screen(name+'测试失败')
                print(name+'测试失败')
                raise e

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    # def tearDown(self):
    #     self.driver.quit()


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestLogin('test_login'))
    with open('HTMLForLogin.html', 'w')as fp:
        runner = HTMLTestRunner(stream=fp, title='login report', description='report', verbosity=2)
        runner.run(suite)
