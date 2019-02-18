# -*- coding=UTF-8 -*-
import unittest
import time
from BeautifulReport import BeautifulReport
#from public.common import sendmail


def run():
    test_dir = './testcase'
    suite = unittest.defaultTestLoader.discover(start_dir=test_dir, pattern='test_zq*.py')
    # suite = unittest.defaultTestLoader.discover(start_dir=test_dir, pattern='test_WBZ_SXSQD1.py')
    now = time.strftime('%Y-%m-%d_%H_%M_%S')
    reportName = 'TestResult_' + now + '.html'
    description = "E7 FSSC V7.0自动化测试报告"
    result = BeautifulReport(suite)
    result.report(filename=reportName, description=description, log_path='report')
    # time.sleep(3)
    # #发送邮件
    # mail = sendmail.SendMail()
    # mail.send()


if __name__ == '__main__':
    run()


