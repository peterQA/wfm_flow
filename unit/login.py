#coding=utf-8
from time import sleep
from selenium.webdriver import ActionChains

#登录
from pageobjects.login_page import Login


def login(driver, username='peter', password='1234567'):
    lg = Login(driver)
    lg.username_input(username)  # 输入用户名
    lg.password_input(password)  # 输入密码
    lg.login_btn()  # 点击登录按钮
    sleep(0.5)
    return lg


#退出
def logout(self):
    driver = self.driver
    # 鼠标悬停在账户头像处
    setmenu = driver.find_element_by_class_name('Homepage_AccountPhoto')
    ActionChains(driver).move_to_element(setmenu).perform()
    sleep(10)
    # 退出登录
    driver.find_element_by_xpath("//li[5]/div").click()
    sleep(3)