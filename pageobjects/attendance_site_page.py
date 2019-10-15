
from unit.base_page import BasePage


class AttendanceSiteList(BasePage):
    # TODO:考勤地点列表页
    # --------------------------------------------------------
    # 操作按钮
    confirm_button = "xpath=>//main/div[2]//button/span[contains(text(),'{0}')]"
    # 要操作的编码数据
    store_path = 'xpath=>//section/main/div/div/div/div//span/span[contains(text(),"{0}")]'
    operation_button = "xpath=>//div[3]/div/button/span[contains(text(),'{0}')]"
    save_button = "xpath=>//div[2]/div/div/div/div/button/span[contains(text(),'{0}')]/.."
    # 店名后的小人
    path2 = "//section/main/div/div/div/div//span/span[contains(text(),'{0}')]/../span[2]/img".format('中山公园')

    # --------------------------------------------------------

    # 点击操作按钮
    def touch_btn(self, text):
        self.click(self.confirm_button.format(text))

    # 选中要操作的数据
    def select_data(self, code):
        self.click(self.store_path.format(code))

    # 操作
    def operation_btn(self, text):
        self.click(self.operation_button.format(text))

    def save_btn(self, text):
        self.click(self.save_button.format(text))

    def visibility(self):
        flag = self.isElementExist(self.path2)

        return flag


class Cancel(BasePage):
    # TODO:休假类型删除页
    # --------------------------------------------------------
    save_button = "xpath=>//div[3]/button/span[contains(text(),'{0}')]"
    # --------------------------------------------------------

    def save_btn(self, text):
        self.click(self.save_button.format(text))
