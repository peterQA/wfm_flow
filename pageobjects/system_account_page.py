
from unit.base_page import BasePage


class SystemAccountList(BasePage):
    # TODO:系统账号列表页
    # --------------------------------------------------------
    # 操作按钮
    confirm_button = "xpath=>//footer/div/../..//div/button/span[contains(text(),'{0}')]"
    # 要操作的编码数据
    code_path = 'xpath=>//table/tbody/tr[*]/td[1]/div[text()="{0}"]'
    # 休假政策描述
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
    # TODO:系统账号新增页
    # --------------------------------------------------------
    save_button = "xpath=>//div//div/div[3]/div/button[1]/span[contains(text(),'{0}')]"
    aria_checked = "xpath=>//form/div/label[contains(text(),'{0}')]/../div/div/span"
    # --------------------------------------------------------

    # 备注允许为空这类选择
    def checked(self, text):
        self.click(self.aria_checked.format(text))

    # 操作按钮
    def save_btn(self, text):
        self.click(self.save_button.format(text))


class Alter(BasePage):
    # TODO:系统账号修改页
    # --------------------------------------------------------
    save_button = "xpath=>//div[2]/button/span[contains(text(),'{0}')]"
    del_button = "xpath=>//div[3]/div/div/button/span[contains(text(),'{0}')]"
    # --------------------------------------------------------

    def save_btn(self, text):
        self.click(self.save_button.format(text))

    def del_btn(self, text):
        self.click(self.del_button.format(text))


class Del(BasePage):
    # TODO:系统账号删除页
    # --------------------------------------------------------
    save_button = "xpath=>//div[3]/button/span[contains(text(),'{0}')]"
    # --------------------------------------------------------

    def save_btn(self, text):
        self.click(self.save_button.format(text))
