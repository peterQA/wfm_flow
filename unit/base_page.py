# !/usr/bin/python
# -*- coding:utf-8 -*-

""""""
from selenium.webdriver import ActionChains

from config.Var import *
from unit.DirAndFile import createDir

"""
    二次封装 selenium 类,又称之为通用类。用于给页面类使用
"""

from logs.logger import Logger
from selenium.common.exceptions import NoSuchElementException
import time
import os

# 引用自定义日志文件
logger = Logger(logger="BasePage").getlog()


class BasePage(object):
    # 初始化 driver 对象
    def __init__(self, driver):
        self.driver = driver

    # quit browser and end testing 浏览器退出方法
    def quit_browser(self):
        self.driver.quit()

    # forward browser 浏览器前进方法
    def forward_browser(self):
        self.driver.forward()
        logger.info("Click forward on current page.")

    # back browser 浏览器后退方法
    def back_browser(self):
        self.driver.back()
        logger.info("Click back to current page.")

    # close_browser 关闭当前浏览器窗口
    def close_browser(self):
        try:
            self.driver.close()
            logger.info("Close and quit the browser")
        except NameError as e:
            logger.error("Failed to quit the browser with %s" % e)


    # find_element_**  元素定位方法  selector:元素位置
    def find_element(self, selector):
        """
        这个地方为什么是根据=>来切割字符串，请看页面里定位元素的方法
        submit_btn = "id=>su"
        login_lnk = "xpath => //*[@id='u1']/a[7]"
        如果采用等号，结果很多xpath表达式中包含一个=，这样会造成切割不准确，影响元素定位
        :param selector:
        :return:
        """
        element = ''
        if '=>' not in selector:
            return self.driver.find_element_by_id(selector)
        selector_by = selector.split('=>')[0]  # 元素名称
        selector_value = selector.split('=>')[1]  # 元素ID名称

        if selector_by == "i" or selector_by == "id":
            try:
                element = self.driver.find_element_by_id(selector_value)  # id 定位
                logger.info("Had find the element \' %s \' successful"
                            "by %s via value:%s" % (element.text, selector_by, selector_value))
            except NoSuchElementException as e:
                logger.error("NoSuchElementException:%s" % e)
                self.get_windows_img()
        elif selector_by == "n" or selector_by == "name":
            element = self.driver.find_element_by_name(selector_value)  # name 名称定位
        elif selector_by == "c" or selector_by == "class_name":
            element = self.driver.find_element_by_class_name(selector_value)  # css 样式名称定位
        elif selector_by == "l" or selector_by == "link_text":
            try:
                element = self.driver.find_element_by_link_text(selector_value)  # 文本超链接定位
                logger.info(("Had find the element \' %s \' successful"
                             "by %s via value:%s" % (element.text, selector_by, selector_value)))
            except NoSuchElementException as e:
                logger.error("NoSuchElementException:%s" % e)
                self.get_windows_img()
        elif selector_by == "p" or selector_by == "partial_link_text":
            element = self.driver.find_element_by_partial_link_text(selector_value)
        elif selector_by == "t" or selector_by == "tag_name":
            element = self.driver.find_element_by_tag_name(selector_value)
        elif selector_by == "x" or selector_by == "xpath":
            try:
                element = self.driver.find_element_by_xpath(selector_value)
                logger.info("Had find the element \' %s \' successful"
                            "by %s via value:%s" % (element.text, selector_by, selector_value))
            except NoSuchElementException as e:
                logger.error("NoSuchElementException:%s" % e)
                self.get_windows_img()
        elif selector_by == "s" or selector_by == "css_selector":
            element = self.driver.find_element_by_css_selector(selector_value)
        else:
            logger.error("Please enter a valid type of targeting elements.")
            raise NameError("Please enter a valid type of targeting elements.")

        return element

    # Text input 文本框输入
    def send_keys(self, selector, text):
        el = self.find_element(selector)  # 获取元素位置信息
        el.clear()  # 文本框清空
        try:
            el.send_keys(text)  # 输入文本信息
            time.sleep(0.2)
            logger.info("Had type \' %s \' in inputBox" % text)
        except NameError as e:
            logger.error("Failed to type in input box with %s" % e)
            self.get_windows_img()
        finally:
            time.sleep(0.5)

    # Text clear 文本框清空 selector:元素位置
    def clear(self, selector):
        el = self.find_element(selector)  # 获取元素位置信息
        try:
            el.clear()
            logger.info("Clear text in input box before type")
        except NameError as e:
            logger.error("Failed to type in input box with %s" % e)
            self.get_windows_img()

    # Text click 点击事件 selector:元素位置
    def click(self, selector):
        time.sleep(0.1)
        el = self.find_element(selector)  # 获取元素位置信息
        time.sleep(0.5)
        try:
            el.click()
            # print(el)
            logger.info("The emement was click")  # 并不是每个元素都存在 text 属性
        except NameError as e:
            logger.error("Failed to type in input box with %s" % e)
            self.get_windows_img()
        finally:
            time.sleep(0.2)

    # get_url_title 获取网页标题
    def get_url_title(self):
        logger.info("Current page title is %s" % self.driver.title)
        return self.driver.title

    # 拖放
    def drag_and_drop(self, start, stop):

        source = self.find_element(start)  # 源元素
        target = self.find_element(stop)   # 目标元素
        try:
            # 拖动
            Action = ActionChains(self.driver)
            Action.drag_and_drop(source, target).perform()
            logger.info("This is drag_and_drop")
        except NameError as e:
            logger.error("Failed drag_and_drop: %s" % e)
            self.get_windows_img()

    # 把元素拉倒可见的位置
    def get_element_out_to_can_see(self, selector):
        try:
            target = self.find_element(selector)
            self.driver.execute_script("arguments[0].scrollIntoView();", target)
            logger.info("The emement was click")
        except Exception as e:
            raise e

    # 滚动条到最下方
    def scroll_page_to_buttom(self):
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except Exception as e:
            raise e

    # 滚动条到最上方
    def scroll_page_to_top(self):
        try:
            self.driver.execute_script("window.scrollTo(0, 0);")
        except Exception as e:
            raise e

    # 保存图片
    def get_windows_img(self):
        file_path = os.path.dirname(os.path.abspath('.')) + '/screenshots/'
        isExists = os.path.exists(file_path)
        # 判断文件夹是否存在，如果不存在则创建。
        if not isExists:
            try:
                os.makedirs(file_path)
            except Exception as e:
                logger.error("Failed new bulid folder %s" % e)
        rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        screen_name = file_path + rq + '.png'
        try:
            self.driver.get_screenshot_as_file(screen_name)
            logger.info("Had take screenshot and save to folder : /screenshots")
        except NameError as e:
            logger.error("Failed to take screenshot! %s" % e)
            self.get_windows_img()

    # 更改前的状态文本
    def status_text1(self, selector):
        status1 = self.find_element(selector)
        return status1.text

    # 更改后的状态文本
    def status_text2(self, selector):
        status2 = self.find_element(selector)
        return status2.text

    # 获取正常截图
    def capture_screen(self, pictureName):
        dirPath = createDir(capture_screen_path, time.strftime("%Y-%m-%d"))
        os.chdir(dirPath)
        try:
            self.driver.get_screenshot_as_file(pictureName + time.strftime("%H_%M_%S") + '.png')
            logger.info("Had take screenshot and save to folder :  \ScreenPictures\CapturePictures")

        except Exception as e:
            logger.error("Failed to take screenshot! %s" % e)
            raise e

    # 获取异常截图
    def error_screen(self, pictureName):
        dirPath = createDir(error_screen_path, time.strftime("%Y-%m-%d"))
        os.chdir(dirPath)
        try:
            self.driver.get_screenshot_as_file(pictureName + time.strftime("%H_%M_%S") + '.png')
            logger.info("Had take screenshot and save to folder :  \ScreenPictures\ErrorPicture")

        except Exception as e:
            logger.error("Failed to take error screenshot! %s" % e)

            raise e

    # 悬浮
    def move_to_element(self, selector):
        setmenu_kqlist = self.find_element(selector)
        ActionChains(self.driver).move_to_element(setmenu_kqlist).perform()
        time.sleep(0.4)

    #   该方法用来确认元素是否存在，如果存在返回flag=true，否则返回false
    def isElementExist(self, element):
        flag = True
        driver = self.driver
        try:
            driver.find_element_by_xpath(element)
            logger.error("The {0} element exist".format(element))

            return flag

        except:

            flag = False
            logger.error("The {0} element does not exist".format(element))

            return flag



