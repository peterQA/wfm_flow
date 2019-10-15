
from unit.base_page import BasePage
from unit.isElementExist import isElementExist


class BasicInfo(BasePage):
    # TODO:基本信息页
    # --------------------------------------------------------
    # 要操作的标题
    title_button = "xpath=>//main/div/div//div/div[contains(text(),'{0}')]"
    save_button = "xpath=>//section/footer/div/button/span[contains(text(),'')]"
    modified = "xpath=>//section/main/div//div[contains(text(),'{0}')]/div/div/input"

    # --------------------------------------------------------

    # 点击操作的标题
    def title_btn(self, title):
        self.click(self.title_button.format(title))

    # 保存
    def save_btn(self):
        self.click(self.save_button)

    # 修改后的数据
    def modified_data(self, tit):
        return self.find_element(self.modified.format(tit)).get_attribute("aria-valuenow")


class Image(BasePage):
    # TODO:图片设置页
    # --------------------------------------------------------
    # 获取图片
    img_path = "//main/div/div//div[contains(text(),'{0}')]/div/div/img"
    # 点击+上传图片
    up_button = "xpath=>//main/div/div//div[contains(text(),'{0}')]/div/div/i"
    # 点击删除图片
    del_button = "xpath=>//main/div/div//div[contains(text(),'{0}')]/button/i"
    # --------------------------------------------------------

    # 调用isElementExist方法，判断元素是否存在
    def judge_img(self, ratio):
        flag = isElementExist(self, self.img_path.format(ratio))
        return flag

    # 上传图片按钮
    def upload_btn(self, ratio):
        self.click(self.up_button.format(ratio))

    # 删除图片按钮
    def del_btn(self, ratio):
        self.click(self.del_button.format(ratio))



