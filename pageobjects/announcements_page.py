import os

from unit.base_page import BasePage


class AnnouncementsList(BasePage):
    # TODO:公告管理列表页
    # --------------------------------------------------------
    # 操作按钮
    confirm_button = "xpath=>//footer/div/../..//div/button/span[contains(text(),'{0}')]"
    # 要操作的编码数据
    code_path = 'xpath=>//table/tbody/tr[*]/td[1]/div[text()="{0}"]'
    # 休假政策描述
    unit_path = "//table/tbody/tr/td[1]/div[contains(text(),'{0}')]/../../td[4]/div"

    # --------------------------------------------------------
    # 点击操作按钮
    def operation_btn(self, text):
        self.click(self.confirm_button.format(text))

    # 选中要操作的数据
    def select_data(self, code):
        self.click(self.code_path.format(code))

    # 指定数据的置顶情况
    def unit_data(self, code):
        text = self.driver.find_element_by_xpath(self.unit_path.format(code)).text
        return text


class Add(BasePage):
    # TODO:公告管理新增页
    # --------------------------------------------------------
    save_button = "xpath=>//div/div[3]//div/button[1]/span[contains(text(),'{0}')]"
    aria_checked = "xpath=>//form/div/label[contains(text(),'{0}')]/../div/div/span"
    # 内容
    con_element = 'xpath=>//form//div[2]/div/p'
    # 封面
    cover = "xpath=>//form/div/label[contains(text(),'{0}')]/..//span"

    # --------------------------------------------------------
    # 封面
    def upload(self, tit, path):
        self.click(self.cover.format(tit))
        os.system(path)

    def mtext(self, content):
        search = self.find_element(self.con_element)
        self.driver.execute_script("arguments[0].innerHTML='{0}';".format(content), search)

    # 备注允许为空这类选择
    def checked(self, text):
        self.click(self.aria_checked.format(text))

    # 操作按钮
    def save_btn(self, text):
        self.click(self.save_button.format(text))


class Alter(BasePage):
    # TODO:公告管理修改页
    # --------------------------------------------------------
    save_button = "xpath=>//div/div[3]//div/button[1]/span[contains(text(),'{0}')]"
    del_button = "xpath=>//div[2]/button/span[contains(text(),'{0}')]"
    # --------------------------------------------------------

    def save_btn(self, text):
        self.click(self.save_button.format(text))

    def del_btn(self, text):
        self.click(self.del_button.format(text))


class Del(BasePage):
    # TODO:公告管理删除页
    # --------------------------------------------------------
    save_button = "xpath=>//div[3]/button/span[contains(text(),'{0}')]"
    # --------------------------------------------------------

    def save_btn(self, text):
        self.click(self.save_button.format(text))


class Copy(BasePage):
    # TODO:公告管理删除页
    # --------------------------------------------------------
    save_button = "xpath=>//div/div[3]//div/button/span[contains(text(),'{0}')]"
    # --------------------------------------------------------

    def save_btn(self, text):
        self.click(self.save_button.format(text))
