import time

from unit.base_page import BasePage


class RuleList(BasePage):
    # TODO:规则列表页
    # --------------------------------------------------------
    # 所有list名
    list_name = "//main/div//div/span/span[1]"

    # 要操作的编码数据
    code_path = 'xpath=>//table/tbody/tr[*]/td[1]/div[text()="{0}"]'
    # 单位数据
    unit_path = "//table/tbody/tr/td[1]/div[text()='{0}']/../../td[3]/div/span"
    # 新建+
    add_button = 'xpath=>//main/div//div/span/span[1][contains(text(),"{0}")]/..//button[1]/span'
    # 删除
    dele_button = 'xpath=>//main/div//div/span/span[1][contains(text(),"{0}")]/..//button[4]/span'

    # --------------------------------------------------------

    # 获取规则列表名称操作
    def macro_list(self):
        lists = []
        elements = self.driver.find_elements_by_xpath(self.list_name)
        for element in elements:
            lists.append(element.text)
        return lists

    # 点击新建+
    def add_btn(self, code):
        self.click(self.add_button.format(code))

    # 点击删除
    def del_btn(self, code):
        self.click(self.dele_button.format(code))


class AddMacro (BasePage):
    # TODO:新建规则页
    # --------------------------------------------------------
    save_button = "xpath=>//div[3]/div/button/span[contains(text(),'{0}')]"
    # --------------------------------------------------------

    def save_btn(self, text):
        self.click(self.save_button.format(text))


class Alter(BasePage):
    # TODO:修改规则页
    # --------------------------------------------------------

    button_path = 'xpath=>//main/div//div/span/span[1][contains(text(),"{0}")]/..//button[2]/span'

    # --------------------------------------------------------

    # 宏顺序上移
    def move_up(self, num, data):
        for _ in range(num):
            time.sleep(0.5)
            self.click(self.button_path.format(data))


class Del(BasePage):
    # TODO:删除规则页
    # --------------------------------------------------------
    save_button = "xpath=>//div[3]/button/span[contains(text(),'{0}')]"
    # --------------------------------------------------------

    def save_btn(self, text):
        self.click(self.save_button.format(text))
