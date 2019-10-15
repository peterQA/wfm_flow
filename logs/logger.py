# !/usr/bin/python
# -*- coding:utf-8 -*-

import logging
import os.path
import time

from config.Var import project_path, log_path


class Logger(object):
    def getlog(self):
        return self.logger

    # 初始化加载
    def __init__(self, logger):
        # 创建一个 logger 对象
        self.logger = logging.getLogger(logger)  # loggger 对象为被执行的对象类
        self.logger.setLevel(logging.DEBUG)  # 设置日志模式为调试模式

        # 创建一个 handler，用于写入日志文件
        rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))  # 设置日期格式
        # log_path = project_path + '/log/'

        # 判断 logs 文件夹是否创建，未创建则进行创建
        isExists = os.path.exists(log_path)
        if not isExists:
            try:
                os.makedirs(log_path)
            except Exception as e:
                print("创建文件夹失败", e)
        log_name = log_path + rq + '.log'
        fh = logging.FileHandler(log_name)
        fh.setLevel(logging.INFO)

        # 创建一个 handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # 定义 handler 输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s ')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger 添加 handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
