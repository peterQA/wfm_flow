from time import sleep

import time

from unit.base_page import BasePage
from unit.isElementExist import isElementExist


class MyFlow(BasePage):
    # TODO:我的流程
    # --------------------------------------------------------

    # 要操作的流程
    flow = "xpath=>//section/div//div[2]/div/div[contains(text(),'{0}')]"
    # --------------------------------------------------------

    # 选择要操作的流程
    def select_flow(self, fw):
        self.click(self.flow.format(fw))


class EmploymentApplication(BasePage):
    # TODO:录用申请页
    # --------------------------------------------------------
    store = "xpath=>//section/div//div/span[contains(text(),'{0}')]"
    organization_button = 'xpath=>//header/div/div[2]//div/div[1]/div[contains(text(),"{0}")]/../..//button/i'
    # --------------------------------------------------------

    def organization_btn(self, organization):
        self.click(self.organization_button.format(organization))

    # 组织单元处理
    def store_select(self, codes):
        for code in codes:
            self.click(self.store.format(code))
            sleep(0.3)
        self.click('xpath=>//section/footer/div[2]/button/span')


class FlowCommon(BasePage):

    # --------------------------------------------------------
    submit_button = 'xpath=>//header/div//div/div[2]/button/span[contains(text(),"提交")]'
    confirm_button = "xpath=>//body/div/div/div[3]/button[2]/span[contains(text(),'确定')]"
    ok_button = "xpath=>//body/div/div/div[3]/button/span[contains(text(),'OK')]"
    st_date = "xpath=>//header/div/div//div[contains(text(),'{0}')]/../..//div/input[1]"
    en_date = "xpath=>//header/div/div//div[contains(text(),'{0}')]/../..//div/input[2]"
    employee_touch = "xpath=>//header/div/div/div/div[1]//div[contains(text(),'{0}')]/../..//button"
    employee = "xpath=>//table/tbody/tr/td/div[contains(text(),'{0}')]"
    store = "xpath=>//section/div//div/span[contains(text(),'{0}')]"
    # --------------------------------------------------------

    # 输入框
    def input_(self, name, codes):
        self.clear("xpath=>//header/div/div//div/div[1]/div[contains(text(),'{0}')]/../..//div[2]//div/input".format(name))
        sleep(0.1)
        self.send_keys("xpath=>//header/div/div//div/div[1]/div[contains(text(),'{0}')]/../..//div[2]//div/input".format(name), codes)
        self.click("xpath=>//header/div/div//div/div[1]/div[contains(text(),'{0}')]".format(name))

    # 选择框
    def input_select(self, name, select):
        self.click("xpath=>//header/div/div//div[2]/div/div[1]/div[contains(text(),'{0}')]/../..//span/span/i".format(name))
        self.click("xpath=>/html/body/div//ul/li/span[contains(text(),'{0}')]".format(select))
        self.click("xpath=>//header/div/div//div[2]/div/div[1]/div[contains(text(),'{0}')]".format(name))

    # 提交
    def submit_btn(self):
        self.click(self.submit_button)
        sleep(0.2)
        self.click(self.confirm_button)

    # ok
    def ok_btn(self):
        self.click(self.ok_button)

    # 时间输入框
    def input_date(self, name, date1, date2):
        self.clear(self.st_date.format(name))
        sleep(0.1)
        self.send_keys(self.st_date.format(name), date1)
        sleep(0.3)
        self.clear(self.en_date.format(name))
        sleep(0.1)
        self.send_keys(self.en_date.format(name), date2)
        self.click("xpath=>//body/div/div[2]/button[2]/span")

    # 员工触发
    def select_employee(self, employee, code):
        self.click(self.employee_touch.format(employee))
        self.click(self.employee.format(code))
        self.click("xpath=>//body//div/div[3]/div/button[1]/span[contains(text(),'确定')]")

    # 组织单元处理
    def store_select(self, codes):
        for code in codes:
            self.click(self.store.format(code))
            sleep(0.3)
        self.click('xpath=>//section/footer/div[2]/button/span')


class MyApply(BasePage):
    # TODO:我的申请
    # --------------------------------------------------------
    # 申请事项
    item_button = "xpath=>//main/div/div/div/div/div[1]//div[contains(text(),'{0}')]"
    # # 入职断言条件(姓名)
    # name = '//*[@id="pane-wfmonboard"]//main/div/div[3]/table/tbody/tr/td[5]/div/div'
    # # 离职断言条件(离职日期)
    # dimission_en_date = '//*[@id="pane-wftdimission"]//main/div/div[3]/table/tbody/tr/td[7]/div/div'
    # # 休假断言条件(离职日期)
    # leave_en_date = '//*[@id="pane-wfmleave"]//main/div/div[3]/table/tbody/tr/td[7]/div/div'
    # # 调店断言条件（开始时间）
    # st_date = '//*[@id="pane-wfmtransferstore"]//main/div/div[3]/table/tbody/tr/td[5]/div/div'
    # # 补打卡断言条件(日期)
    # fill_clock_date = '//*[@id="pane-wfmclock"]//main/div/div[3]/table/tbody/tr/td[5]/div/div'
    # 我的申请里的申请名
    application_name_path = "xpath=>//section/main/div//div//*[@id='{0}']"

    # --------------------------------------------------------

    def item_btn(self, item):
        self.click(self.item_button.format(item))

    # 数据名列表
    def application_name_list(self, x):
        name = ''
        if x == '门店销迟到早退':
            name = self.find_element(self.application_name_path.format('tab-wfmregisterlate')).text
        elif x == '门店补打卡':
            name = self.find_element(self.application_name_path.format('tab-wfmclock')).text
        elif x == '门店调店':
            name = self.find_element(self.application_name_path.format('tab-wfmtransferstore')).text
        elif x == '门店休假':
            name = self.find_element(self.application_name_path.format('tab-wfmleave')).text

        elif x == '门店离职':
            name = self.find_element(self.application_name_path.format('tab-wftdimission')).text
        elif x == '门店入职':
            name = self.find_element(self.application_name_path.format('tab-wfmonboard')).text
        elif x == '门店加班':
            name = self.find_element(self.application_name_path.format('tab-wfmovertime')).text

        return name




