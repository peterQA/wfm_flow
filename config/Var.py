# encoding=utf-8
import os
import time

from unit.config_parser import _ConfigParser
# 当前文件路径
file_path = __file__
# 工程路径
# os.path.dirname(__file__)当前文件所在路径
project_path = os.path.dirname(os.path.dirname(__file__))

# 读取配置文件
# config_parser = _ConfigParser()
path = project_path + '/config'
config_path = os.path.join(path, "config.ini")
print(config_path)
# 正常截图保存路径
capture_screen_path = project_path + r"/result/ScreenPictures/CapturePictures"
# 异常截图保存路径
error_screen_path = project_path + r"/result/ScreenPictures/ErrorPicture"
# log存放路径
log_path = project_path + r"/result/log/"
# 测试报告存放路径
testreport = project_path + '/result/test_report/'
# 登录测试数据存放
login_filename = project_path + '/test_excel/login_info.xlsx'
login_sheetname = 'Sheet1'
# 语言
# language = config_parser.get_value_from_config(config_path, 'Language', 'language')
