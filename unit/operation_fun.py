
"""
操作方法
"""
import time

from unit.base_page import BasePage


class OperationMethod(BasePage):

    # 输入框
    def input_(self, name, codes):
        self.clear("xpath=>//div/label[text()='{0}']/..//input".format(name))
        time.sleep(0.1)
        self.send_keys("xpath=>//div/label[text()='{0}']/..//input".format(name), codes)
        # self.click("xpath=>//div/label[text()='{0}']".format(name))

    # 选择框
    def input_select(self, name, select):
        self.click("xpath=>//div/label[text()='{0}']/../div/div/div/span/span/i".format(name))
        self.click("xpath=>//div/label[text()='{0}']/..//ul/li/span[contains(text(),'{1}')]".format(name, select))
        self.click("xpath=>//div/label[text()='{0}']".format(name))

    # 数据名列表
    def data_list(self):
        texts = []
        elements = self.driver.find_elements_by_xpath('//table/tbody/tr/td[1]/div')
        for element in elements:
            text = element.text
            time.sleep(0.2)
            texts.append(text)
            time.sleep(0.2)
        return texts

    # 输入框
    def textarea_(self, name, codes):
        self.clear("xpath=>//div/label[text()='{0}']/..//textarea".format(name))
        self.send_keys("xpath=>//div/label[text()='{0}']/..//textarea".format(name), codes)
        # self.click("xpath=>//div/label[text()='{0}']".format(name))

    # 系统管理-基本设置中，类似初始密码位数，输入控件
    def input_number(self, name, num):
        self.clear("xpath=>//section/main/div//div[contains(text(),'{0}')]/div/div/input".format(name))
        self.send_keys("xpath=>//section/main/div//div[contains(text(),'{0}')]/div/div/input".format(name), num)

    # 复选框(框在前)
    def checkbox(self, conten):
        s = self.find_element("xpath=>//section/main/div/div//div/label/span[contains(text(),'{0}')]/../span[1]/span/.."
                              .format(conten)).get_attribute("class")
        if "is-checked" not in s:
            self.click("xpath=>//section/main/div/div//div/label/span[contains(text(),'{0}')]/../span[1]/span".format(conten))

    # 复选框(框在后)
    def checkbox1(self, conten):
        s = self.find_element("xpath=>//form/div/label[contains(text(),'{0}')]/..//span/.."
                              .format(conten)).get_attribute("class")
        if "is-checked" not in s:
            self.click("xpath=>//form/div/label[contains(text(),'{0}')]/..//span".format(conten))
