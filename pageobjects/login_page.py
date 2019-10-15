# !/usr/bin/python
# -*- coding:utf-8 -*-

""""""

from unit.base_page import BasePage

"""
 页面类，主要存放页面简单的操作函数.
 页面类主要是将页面操作写成函数，以供测试类使用
 集成 BasePage 二次封装通用类
 通常 1个页面为一个类
"""


# 登录页
class Login(BasePage):
    # TODO:登录页
    # --------------------------------------------------------
    # 用户名输入框
    username_box = 'xpath=>//form/div[1]/div[1]/input'
    password_box = 'xpath=>//form/div[1]/div[2]/input'
    login_button = 'xpath=>//form/div[2]/div/div/button'

    # --------------------------------------------------------

    # 用户名输入
    def username_input(self, text):
        self.send_keys(self.username_box,text)

    # 密码输入
    def password_input(self, text):
        self.send_keys(self.password_box, text)

    # 删除按钮
    def login_btn(self):
        self.click(self.login_button)



