
from unit.base_page import BasePage


class ExamineCustomList(BasePage):
    # TODO:审查自定义项列表页
    # --------------------------------------------------------
    # 操作按钮
    confirm_button = "xpath=>//div/button/span[contains(text(),'{0}')]"
    # 要操作的编码数据
    code_path = 'xpath=>//table/tbody/tr[*]/td[1]/div[text()="{0}"]'
    # 字段类型数据
    unit_path = "//table/tbody/tr/td[1]/div[text()='{0}']/../../td[2]/div"
    # --------------------------------------------------------

    # 点击操作按钮
    def operation_btn(self, text):
        self.click(self.confirm_button.format(text))

    # 选中要操作的数据
    def select_data(self, code):
        self.click(self.code_path.format(code))

    # 指定数据的单位
    def unit_data(self, code):
        text = self.driver.find_element_by_xpath(self.unit_path.format(code)).text
        return text


class Add(BasePage):
    # TODO:审查自定义项新增页
    # --------------------------------------------------------
    save_button = "xpath=>//div[3]/div/button/span[contains(text(),'{0}')]"
    # --------------------------------------------------------

    def save_btn(self, text):
        self.click(self.save_button.format(text))


class Alter(BasePage):
    # TODO:审查自定义项修改页
    # --------------------------------------------------------
    save_button = "xpath=>//div[3]/div/button/span[contains(text(),'{0}')]"
    del_button = "xpath=>//div[3]/div/div/button/span[contains(text(),'删除')]"
    # --------------------------------------------------------

    def save_btn(self, text):
        self.click(self.save_button.format(text))

    def del_btn(self):
        self.click(self.del_button)


class Del(BasePage):
    # TODO:审查自定义项删除页
    # --------------------------------------------------------
    save_button = "xpath=>//div[3]/button/span[contains(text(),'{0}')]"
    # --------------------------------------------------------

    def operation_btn(self, text):
        self.click(self.save_button.format(text))
