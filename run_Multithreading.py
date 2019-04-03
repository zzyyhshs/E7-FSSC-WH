      # coding=utf-8
import unittest
from BeautifulReport import BeautifulReport
from tomorrow import threads
import time
def add_case():
    '''加载所有的测试用例'''
    test_dir = './testcase'
    suite = unittest.defaultTestLoader.discover(start_dir=test_dir, pattern='test_zq*.py')
    return suite

now = time.strftime('%Y-%m-%d_%H_%M_%S')
reportName = 'TestResult_' + now + '.html'
@threads(3)
def run(test_suit):
    description = "E7 FSSC " \
                  ".0自动化测试报告"
    result = BeautifulReport(test_suit)
    result.report(filename=reportName, description=description, log_path='report')

if __name__ == "__main__":
    # 用例集合
    cases = add_case()
    for case in cases:
        run(case)