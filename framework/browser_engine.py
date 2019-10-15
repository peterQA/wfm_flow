# !/usr/bin/python
# -*- coding:utf-8 -*-
import configparser

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config.Var import project_path
from logs.logger import Logger

logger = Logger(logger="BrowserEngine").getlog()


# 浏览器引擎类
class BrowserEngine(object):
    def __init__(self, driver):
        self.driver = driver

    # 打开浏览器，访问 url 地址
    def open_browser(self, driver):
        # 读取 config 配置文件
        config = configparser.ConfigParser()
        # file_path = os.path.dirname(os.path.abspath('.')) + '/config/config.ini'
        # file_path = os.path.abspath('.') + '/config/config.ini'
        file_path = project_path + '/config/config.ini'

        chrome_options = Options()
        chrome_options.add_argument("--headless")

        config.read(file_path)

        # 读取 config 配置文件内容
        browser = config.get("browserType", "browserName")
        logger.info("You had select %s browser." % browser)
        url = config.get("testServer", "URL")
        logger.info("The test server url is %s" % url)

        if browser == "Firefox":
            driver = webdriver.Firefox()
            logger.info("Starting firefox browser")
        elif browser == "Chrome":
            driver = webdriver.Chrome()
            logger.info("Starting Chorme browser")
        elif browser == "IE":
            driver = webdriver.Ie()
            logger.info("Starting IE browser")
        # elif browser == "PhantomJS":
        #     driver = webdriver.PhantomJS()
        #     logger.info("Starting PhantomJS browser")

        try:
            driver.get(url)  # 访问 url 地址
            logger.info("Open url %s" % url)
            driver.implicitly_wait(10)
            logger.info("Set implicit wait for 10 seconds")
            driver.maximize_window()
            logger.info("Set maximize window")
            return driver
        except Exception as e:
            logger.info(e)

    def quit_browser(self):
        logger.info("Now, close and exit the browser.")
        print(self.driver)
        self.driver.quit()
