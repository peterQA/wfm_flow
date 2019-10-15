# -*- coding=utf8 -*-
# import HTMLTestRunner
import HTMLTestRunner12
from unit import HTMLTestRunner
import configparser
import smtplib
import unittest
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.Var import *
from unit.DirAndFile import createDir


# --------------------------------------------------------
# 定义发送邮件
from unit.sqlserver import DataBase


def send_mail(new_file):
    # 定义正文
    f = open(new_file, 'rb')
    mail_body = f.read()
    f.close()

    # 发信邮箱
    sender = '17082580140@163.com'
    # 收信邮箱
    # mail_to = ['Peter.Zhang@Platinumchina.com', '17082580140@163.com', '1586612155@qq.com',
    #            'cherry.li@platinumchina.com']

    mail_to = ['Peter.Zhang@Platinumchina.com', '17082580140@163.com']

    # 发送邮箱服务器
    smtpserver = 'smtp.163.com'
    # 发送邮箱用户名/密码
    user = '17082580140@163.com'
    password = 'peter123'
    # 发送邮件的主题
    subject = 'WFM测试报告'
    # 编写正文yuans
    msg = MIMEMultipart('mixed')
    msg_html1 = MIMEText(mail_body, 'html', 'utf-8')
    msg.attach(msg_html1)
    # 添加附件
    msg_html = MIMEText(mail_body, 'html', 'utf-8')
    msg_html["Content-Disposition"] = 'attachment; filename="%s"' % new_file[12:-1]
    msg.attach(msg_html)
    # 定义标题
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = '17082580140@163.com'
    msg['To'] = ','.join(mail_to)
    # 定义发送时间（不定义的可能有的邮件客户端会不显示发送时间）
    msg['Date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')

    # 连接 SMTP 服务器，此处用的 163 的 SMTP 服务器
    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver, 25)
        # 用户名密码
        smtp.login(user, password)
        smtp.sendmail(sender, mail_to, msg.as_string())
        smtp.quit()
        print('邮件发送成功！')
    except smtplib.SMTPException:
        print('ERROR：无法发送邮件！')


# --------------------------------------------------------
# 查找测试报告目录，找到最新生成的测试报告文件
def send_report(test_report):
    result_dir = test_report
    lists = os.listdir(result_dir)
    lists.sort(key=lambda fn: os.path.getmtime(result_dir + "\\" + fn))
    # 找到最新生成的文件
    new_file = os.path.join(result_dir, lists[-1])
    print(new_file)
    # 调用发邮件模块
    send_mail(new_file)


# --------------------------------------------------------
caseList = []


# 外部读入需要运行的case
def set_case_list(caseListFile):
    fb = open(caseListFile, encoding='utf-8')
    for value in fb.readlines():
        data = str(value)
        if data != '' and not data.startswith("#"):
            caseList.append(data.replace("\n", ""))
    fb.close()


# 构建测试套件
def set_case_suite():
    # set_case_list('F:\wfm_flow\\config\caselist.txt')
    set_case_list(project_path + "/config/caselist.txt")
    test_suite = unittest.TestSuite()
    suite_model = []

    for case in caseList:
        case_file = os.path.join(project_path, "/wfm_flow/testsuits/")
        print(case_file)
        case_name = case.split("/")[-1]
        print(case_name + ".py")
        discover = unittest.defaultTestLoader.discover(case_file, pattern=case_name + '.py', top_level_dir=None)
        suite_model.append(discover)

    if len(suite_model) > 0:
        for _suite in suite_model:
            for test_name in _suite:
                test_suite.addTest(test_name)
    else:
        return None
    return test_suite


if __name__ == '__main__':
    # 数据库还原
    DataBase(1).database_restore()
    # 获取当前时间
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    dirPath = createDir(testreport, '')
    os.chdir(dirPath)
    # 定义报告存放路径
    filename = now + '_result.html'
    fp = open(filename, 'wb')
    # 定义测试报告
    # runner = HTMLTestRunner.HTMLTestRunner(
    #     stream=fp,
    #     title='WFM测试报告',
    #     description='用例执行情况：',
    #     tester='PLATINUM-QA',
    #     verbosity=1, retry=1, save_last_try=True)
    # runner = HTMLTestRunner12.HTMLTestRunner(
    #     title="WFM测试报告",
    #     description="用例执行情况：",
    #     stream=fp,
    #     verbosity=1, retry=1)

    # suite = create_suite()
    runner = HTMLTestRunner.HTMLTestReportCN(
        stream=fp,
        title='WFM测试报告',
        description='用例执行情况：',  # 不传默认为空
        tester="PLATINUM-QA",
        verbosity=2, retry=0, save_last_try=True)

    suite = set_case_suite()

    runner.run(suite)
    # 关闭生成的报告
    fp.close()
    # 发送报告
    send_report(testreport)
