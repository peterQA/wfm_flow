from unit.excel import read_excel
from config.Var import *
from unit.excel import *


# encoding=utf-8
# login的测试数据
# test_login_info = [("user_null", '', "123", "用户名/密码不能为空"),
#                    ("pawd_null", "wfm001", '', "用户名/密码不能为空"),
#                    ("login_error", "error", "error", "用户名或者密码不正确!"),
#                    ("wfm001", "wfm001", "1234567", ''),
#                    ("peter", "peter", "1234567", '')]


# test_login_info = read_excel(filename=login_filename, sheetname=login_sheetname)
#
# print(test_login_info)
# 员工政策分配的测试数据
# test01_alter_correct_info = [('WFM5', 'WFM005', '考勤体系', '大陆门店考勤', '休假政策',
#                               "普通员工", '加班政策', "管理人员", '状态', '不排班,不考勤', '确认'),
#                              ('WFM4', 'WFM004', '考勤体系', '香港门店考勤', '休假政策',
#                               "管理人员", '加班政策', "普通员工", '状态', '不排班,不考勤', '取消')]
# excel_utils = ExcelUtils("login_info.xlsx", "Sheet2")
# test01_alter_correct_info = excel_utils.dict_data()
# print(test01_alter_correct_info[0]['分组'])

# if test01_alter_correct_info[1]['分组'] == '':
    # print(test01_alter_correct_info[1]['分组'])
    # print('hahh')
#
# proDir = os.path.split(os.path.realpath(__file__))[0]
# print(proDir)
