
from unit.base_page import BasePage


class ShiftTypeList(BasePage):
    # TODO:休假类型列表页
    # --------------------------------------------------------
    # 操作按钮
    confirm_button = "xpath=>//footer/div/button/span[contains(text(),'{0}')]"
    # 要操作的编码数据
    code_path = 'xpath=>//table/tbody/tr[*]/td[1]/div[text()="{0}"]'
    # 描述信息数据
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
    # TODO:休假类型新增页
    # --------------------------------------------------------
    save_button = "xpath=>//div[3]/div/button/span[contains(text(),'{0}')]"
    # --------------------------------------------------------

    def save_btn(self, text):
        self.click(self.save_button.format(text))


class Alter(BasePage):
    # TODO:休假类型修改页
    # --------------------------------------------------------
    save_button = "xpath=>//div[3]/div/button/span[contains(text(),'{0}')]"
    # --------------------------------------------------------

    def save_btn(self, text):
        self.click(self.save_button.format(text))


class Del(BasePage):
    # TODO:休假类型删除页
    # --------------------------------------------------------
    save_button = "xpath=>//div[3]/button/span[contains(text(),'{0}')]"
    # --------------------------------------------------------

    def save_btn(self, text):
        self.click(self.save_button.format(text))
