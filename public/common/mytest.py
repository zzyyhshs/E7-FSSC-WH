#coding=utf-8
import unittest


from autoTestFrame import PySelenium
from public.common import publicfunction
from config import globalparam
from public.common.log import Log
from time import sleep
from time import strftime
import time
from public.MobileScript.Instrument import MobileSelenium


class MyTest(unittest.TestCase):
    """
    The base class is for all pc testcase.
    """
    def setUp(self):
        startTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.logger = Log(self._testMethodName)
        self.logger.info('############################### START ###############################')
        self.logger.info("测试用例开始执行："+self._testMethodName+"  "+startTime)
        self.dr = PySelenium(globalparam.browser,self.logger)
        sleep(2)
        self.dr.max_window()

    def tearDown(self):
        publicfunction.get_img(self.dr,strftime('%Y-%m-%d_%H_%M_%S')+"_用例执行结束" +".jpg")
        self.logger.info("测试用例执行结束：" + self._testMethodName)
        self.logger.info('###############################  End  ###############################')
        self.dr.quit()


class MyMobileTest(unittest.TestCase):
    """
    The base class is for all mobile testcase.
    """
    def setUp(self):
        startTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.logger = Log(self._testMethodName)
        self.logger.info('############################### START ###############################')
        self.logger.info("测试用例开始执行："+self._testMethodName+"  "+startTime)
        self.dr = MobileSelenium(globalparam.browser_mobile, self.logger)
        sleep(2)
        self.dr.max_window()
        # self.dr.driver.set_window_size(1200, 900)

    def tearDown(self):
        self.dr.print_img()
        self.logger.info("测试用例执行结束：" + self._testMethodName)
        self.logger.info('###############################  End  ###############################')
        self.dr.quit()
