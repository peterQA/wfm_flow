
from unit.base_page import BasePage


class AttendancePeriodManagementList(BasePage):
    # TODO:考勤期段管理列表页
    # --------------------------------------------------------
    # 操作按钮
    confirm_button = "xpath=>//footer/div/div/div/button/span[contains(text(),'{0}')]"
    # 要操作的日期数据
    date_path = 'xpath=>//table/tbody/tr/td[2]/div[contains(text(),"{0}")]/../../td[3]/div[contains(text(),"{1}")]/../../td[4]/div'
    # 备注
    unit_path = "xpath=>//table/tbody/tr/td/div[contains(text(),'{0}')]/../../td[5]/div"
    # 过账前的状态
    text = "xpath=>//table/tbody/tr/td/div[contains(text(),'{0}')]/../../td[3]/div[contains(text(),'{1}')]/../../td[4]/div"
    # 状态排序
    _sort = 'xpath=>//table/thead/tr/th/div[contains(text(),"状态")]/span/i[1]'
    # --------------------------------------------------------

    # 点击操作按钮
    def operation_btn(self, text):
        self.click(self.confirm_button.format(text))

    # 选中要操作的数据
    def select_data(self, st_date, en_date):
        self.click(self.date_path.format(st_date, en_date))

    # 指定日期的备注
    def unit_data(self, date):
        text = self.status_text1(self.unit_path.format(date))
        return text

    # 过账前的状态
    def carry_to_status(self, st, en):
        x = self.text.format(st, en)
        print(x)
        text = self.status_text1(x)
        print(text)
        return text

    # 状态排序
    def sort(self):
        self.click(self._sort)


class Alter(BasePage):
    # TODO:考勤期段管理修改页
    # --------------------------------------------------------
    save_button = "xpath=>//div[3]/div/button/span[contains(text(),'{0}')]"
    # --------------------------------------------------------

    def save_btn(self, text):
        self.click(self.save_button.format(text))


class CarryTo(BasePage):
    # TODO:考勤期段管理考勤过账页
    # --------------------------------------------------------
    save_button = "xpath=>//div[3]/button/span[contains(text(),'{0}')]"
    # --------------------------------------------------------

    def save_btn(self, text):
        self.click(self.save_button.format(text))
